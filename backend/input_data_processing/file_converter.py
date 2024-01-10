import os
import csv
from pymongo import MongoClient
from bson.objectid import ObjectId as ObjectID
from datetime import datetime
from dotenv import load_dotenv


def csv_to_list(file_path):
    '''
    Function to convert generic CSV to lists of dictionaries
        Parameters:
            file_path (str): Path to the CSV file
        Returns:
            data (list): List of dictionaries
    '''
    with open(file_path, 'r', newline='', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',', quotechar='"')
        data = list(csv_reader)
    return data

def csv_to_list_reg_corr(file_path):
    '''
    Function to convert registration_corrections.csv to lists of dictionaries. No header in the CSV file.
        Parameters:
            file_path (str): Path to the CSV file
        Returns:
            data (list): List with dictionary
    '''
    data = []

    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)
        
        for row in csv_reader:
            if(len(row) == 0):
                continue
            else:
                name, date = row[0], row[1]
                data.append({'name': name, 'date': date})

    return data

def csv_to_list_sim_period(file_path):
    '''
    Convert the simulation period CSV file to a dictionary.
    The rows and columns must be transposed.
        Parameters:
            file_path (str): Path to the CSV file
        Returns:
            data (list): List with dictionary
    '''
    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)
        rows = list(csv_reader)

    transposed_data = {'date': rows[0][1], 'length': rows[1][1]}
    transposed_data_list = [transposed_data] # convert to list of dicts for consistency with other functions
    return transposed_data_list


def transform_location_data(location_data):
    '''
    Transform the location data to match the MongoDB schema.
        Parameters:
            location_data (list): List of dictionaries
        Returns:
            transformed_data (list): List of dictionaries
    '''
    transformed_data = []
    for row in location_data:
        name_key = '#name' if '#name' in row else '#"name"'
        lat_key = 'latitude' if 'latitude' in row else 'lat'
        lon_key = 'longitude' if 'longitude' in row else 'lon'
        transformed_data.append({
            'name': row[name_key],
            'region': row['region'],
            'country': row['country'],
            'latitude': float(row[lat_key]),
            'longitude': float(row[lon_key]),
            'location_type': row['location_type'],
            'conflict_date': int(row['conflict_date']) if row['conflict_date'] else None,
            'population': int(row['population']) if row['population'] else None
        })
    return transformed_data


def transform_routes_data(routes_data):
    '''
    Transform the routes data to match the MongoDB schema.
        Parameters:
            routes_data (list): List of dictionaries
        Returns:
            transformed_data (list): List of dictionaries
    '''
    transformed_data = []
    for row in routes_data:
        name1_key = 'name1'
        if 'name1' not in row:
            name1_key = '#name1' if '#name1' in row else '#"name1"'
        transformed_data.append({
            'from': row[name1_key],
            'to': row['name2'],
            'distance': float(row['distance']),
            'forced_redirection': float(row['forced_redirection']) if row['forced_redirection'] else None
        })
    return transformed_data


def transform_closure_data(closure_data):
    '''
    Transform the closure data to match the MongoDB schema.
        Parameters:
            closure_data (list): List of dictionaries
        Returns:
            transformed_data (list): List of dictionaries
    '''
    transformed_data = []
    for row in closure_data:
        transformed_data.append({
            'closure_type': row['#closure_type'],
            'name1': row['name1'],
            'name2': row['name2'],
            'closure_start': int(row['closure_start']),
            'closure_end': int(row['closure_end'])
        })
    return transformed_data


def transform_conflicts_data(conflicts_data):
    '''
    Transform the conflicts data to match the MongoDB schema.
        Parameters:
            conflicts_data (list): List of dictionaries
        Returns:
            transformed_data (list): List of dictionaries
    '''
    transformed_data = []

    for row in conflicts_data:
        transformed_row = {}

        for field, value in row.items():
            key = field.strip('#')  # Remove '#' from the field name
            key = key.strip()  # Remove whitespace from the field name
            value = int(value) if value else None  # Convert to int if not None
            transformed_row[key] = value

        transformed_data.append(transformed_row)
    return transformed_data


def transform_reg_corr_data(reg_corr_data):
    '''
    Transform the registration corrections data to match the MongoDB schema.
        Parameters:
            reg_corr_data (list): List of dictionaries
        Returns:
            transformed_data (list): List of dictionaries
    '''
    transformed_data = []
    for row in reg_corr_data:
        name = row['name']
        date_str = row['date']
        date_obj = datetime.strptime(date_str, '%Y-%m-%d') # additionally takes the time

        transformed_data.append({
            'name': name,
            'date': date_obj,
        })
    return transformed_data


def transform_sim_period_data(sim_period_data):
    '''
    Transform the simulation period data to match the MongoDB schema.
        Parameters:
            sim_period_data (list): List of dictionaries
        Returns:
            transformed_data (list): List of dictionaries
    '''
    transformed_data = []
    for row in sim_period_data:
        date = row['date']
        date = datetime.strptime(date, '%Y-%m-%d') # additionally takes the time
        print(date)
        length = int(row['length'])

        transformed_data.append({
            'date': date,
            'length': length,
        })
    return transformed_data



def insert_data_into_DB(country_list, folder_path, acled_source_list=[], population_source_list = [], is_test_data=False):
    '''
    Insert the data into the MongoDB.
        Parameters:
            country_list (list): List of country names
            folder_path (str): Path to the folder containing the CSV files
            acled_source_list (list): List containing the ACLED data source and latest available date
            population_source_list (list): List containing the population data source and latest available date
            is_test_data (bool): Whether the data is test data or not
    '''
    load_dotenv()
    MONGODB_URI = os.environ.get('MONGO_URI')

    client = MongoClient(MONGODB_URI)
    db = client.get_database("Caturanga")
    simulations_collection = db.get_collection("simulations")

    for country in country_list:
        if is_test_data:
            # Get the current directory of file_converter.py
            current_directory = os.path.dirname(os.path.realpath(__file__))
            # Navigate to the locations.csv file using relative paths
            data_dir = os.path.join(current_directory, folder_path, country)
        else: 
            data_dir = folder_path

        location_csv_path = os.path.join(data_dir, 'locations.csv')
        routes_csv_path = os.path.join(data_dir, 'routes.csv')
        conflicts_csv_path = os.path.join(data_dir, 'conflicts.csv')
        closures_csv_path = os.path.join(data_dir, 'closures.csv')
        reg_corrections_csv_path = os.path.join(data_dir, 'registration_corrections.csv')
        sim_period_csv_path = os.path.join(data_dir, 'sim_period.csv')

        # Convert CSV to lists of dictionaries
        location_data = csv_to_list(location_csv_path)
        routes_data = csv_to_list(routes_csv_path)
        conflicts_data = csv_to_list(conflicts_csv_path)
        closures_data = csv_to_list(closures_csv_path)
        reg_corr_data = csv_to_list_reg_corr(reg_corrections_csv_path)
        sim_period_data = csv_to_list_sim_period(sim_period_csv_path)

        # Transform CSV data to match MongoDB schema
        locations = transform_location_data(location_data)
        routes = transform_routes_data(routes_data)
        conflicts = transform_conflicts_data(conflicts_data)
        closures = transform_closure_data(closures_data)
        reg_corr = transform_reg_corr_data(reg_corr_data)
        sim_period = transform_sim_period_data(sim_period_data)

        print(acled_source_list)
        print(population_source_list)

        # Create the JSON object to be inserted into the MongoDB
        mongo_document = {
            'region': country,
            'closures': closures,
            'conflicts': conflicts,
            'locations': locations,
            'registration_corrections': reg_corr,
            'routes': routes,
            'sim_period': sim_period[0] if sim_period else None,  # Use the first element or None if the list is empty
            'data_sources': {
                'acled': {
                    'url': acled_source_list[0],
                    'retrieval_date': datetime.strptime(acled_source_list[1], '%Y-%m-%d %H:%M:%S'),
                    'user_start_date': datetime.strptime(acled_source_list[2], '%Y-%m-%d'),
                    'user_end_date': datetime.strptime(acled_source_list[3], '%Y-%m-%d'),
                    'oldest_event_date': datetime.strptime(acled_source_list[4], '%Y-%m-%d'),
                    'latest_event_date': datetime.strptime(acled_source_list[5], '%Y-%m-%d')
                },
                'population': {
                    'url': population_source_list[0],
                    'retrieval_date': datetime.strptime(population_source_list[1], '%Y-%m-%d %H:%M:%S'),
                    'latest_population_date': datetime.strptime(population_source_list[2], '%Y-%m-%d')
                }
             }
        }

        # insert test data into the database
        result = simulations_collection.insert_one(mongo_document)

    client.close()


def delete_data_from_DB(id):
    '''
    Delete the data from the MongoDB.
        Parameters:
            id (str): ID of the document to be deleted
    '''
    load_dotenv()
    MONGODB_URI = os.environ.get('MONGO_URI')

    client = MongoClient(MONGODB_URI)
    db = client.get_database("Caturanga")
    simulations_collection = db.get_collection("simulations")

    # delete document from collection
    result = simulations_collection.delete_many({"_id": ObjectID(id)})

    client.close()


# insert test data from frontend folder into the database
"""
countries = ['burundi' , 'car', 'ethiopia', 'mali', 'ssudan']
folder_path = "..\\flee\\conflict_input\\"
# add acled and population information with test values
acled_source_list = ["test_url", "2024-01-10 11:48:58", "2023-07-01", "2023-11-15", "2023-07-02", "2023-11-15"]
population_source_list = ["test_url", "2024-01-10 11:48:58", "2021-05-17"]

insert_data_into_DB(countries, folder_path, acled_source_list, population_source_list, is_test_data=True)
"""

# delete  data from the database
"""
delete_ids = ["659e7398a4e932c57153caae"]
for ids in delete_ids:
    delete_data_from_DB(ids)
"""