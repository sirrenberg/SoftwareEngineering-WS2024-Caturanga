import os
import csv
from pymongo import MongoClient
from bson.objectid import ObjectId as ObjectID
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path


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

def csv_to_list_camps(file_path):
    """ 
    This function is used to convert the csv files for the camps into a list of dictionaries.
    The csv files have no header, therefore we add date and refugee_numbers as headers.
    Parameters:
        file_path (str): Path to the CSV file
    Returns:
        tranposed_data (list): List of dictionaries
    """
    # the csv have no header. I want to add date and refugee_numbers 
    with open (file_path, 'r') as file:
        csv_reader = csv.reader(file)
        rows = list(csv_reader)
    tranposed_data = []
    for row in rows:
        tranposed_data.append({'date': row[0], 'refugee_numbers': int(row[1])})
    return tranposed_data


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
        name_key = '#name' if '#name' in row else '#"name"' # 
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
        length = int(row['length'])

        transformed_data.append({
            'date': date,
            'length': length,
        })
    return transformed_data


def transform_val_refugees_data(validation_refugee_data):
    '''
    Transform the refugees data to match the MongoDB schema.
        Parameters:
            validation_refugee_data (list): List of dictionaries
        Returns:
            transformed_data (list): List of dictionaries
    '''
    transformed_data = []
    for row in validation_refugee_data:
        transformed_data.append({
            'date': datetime.strptime(row['Date'], '%Y-%m-%d'),  # datetime object
            'refugee_numbers': int(row['Refugee_numbers']),
        })
    return transformed_data



def transform_val_data_layout_data(validation_data_layout_data):
    '''
    Transform the data_layout data to match the MongoDB schema.
        Parameters:
            validation_data_layout_data (list): List of dictionaries
        Returns:
            transformed_data (list): List of dictionaries
    '''
    transformed_data = []
    for row in validation_data_layout_data:
        # original headers according to FLEE. changed here for storage in DB with meaningful names
        transformed_data.append({
            'camp_name': row['total'],
            'file_name': row['refugees.csv'],
        })
    return transformed_data


def transform_val_camp_data(validation_camp_data):
    '''
    Transform the camp data to match the MongoDB schema.
        Parameters:
            validation_camp_data (list): List of dictionaries
        Returns:
            transformed_data (list): List of dictionaries
    '''
    transformed_data = []
    for row in validation_camp_data:
        transformed_data.append({
            'date': datetime.strptime(row['date'], '%Y-%m-%d'),  # datetime object
            'refugee_numbers': row['refugee_numbers'],
        })
    return transformed_data



def insert_data_into_DB(country, current_dir, folder_name, acled_source_list=[], population_source_list = [], camp_source_list = [], val_source_list = []):
    '''
    Insert the data into the MongoDB.
        Parameters:
            country (str): Name of the country
            current_dir (str): Current directory of caller
            folder_path (str): Path to the folder containing the CSV files
            acled_source_list (list): List containing the ACLED data source and latest available date
            population_source_list (list): List containing the population data source and latest available date
            camps_source_list (list): List containing the camps data source and latest available date
            val_source_list (list): List containing the validation data source and latest available date
    '''

    # Connect to the MongoDB
    # root_dir = Path(__file__).resolve().parent
    # env_path = os.path.join(root_dir, ".env")
    # load_dotenv(env_path)
    load_dotenv()
    MONGODB_URI = os.environ.get('MONGO_URI')
    client = MongoClient(MONGODB_URI)
    db = client.get_database("Caturanga")
    simulations_collection = db.get_collection("simulations")

    # Get the data directory and validation data directory
    folder_path = os.path.join(current_dir, folder_name)
    data_dir = folder_path
    # docker path
    data_dir_validation = os.path.join(current_dir, "input_data_processing", "conflict_validation", folder_name)
    # data_dir_validation = os.path.join(current_dir, "conflict_validation", folder_name)

    # input data
    location_csv_path = os.path.join(data_dir, 'locations.csv')
    routes_csv_path = os.path.join(data_dir, 'routes.csv')
    conflicts_csv_path = os.path.join(data_dir, 'conflicts.csv')
    closures_csv_path = os.path.join(data_dir, 'closures.csv')
    reg_corrections_csv_path = os.path.join(data_dir, 'registration_corrections.csv')
    sim_period_csv_path = os.path.join(data_dir, 'sim_period.csv')

    # validation data
    refugees_csv_path = os.path.join(data_dir_validation, 'refugees.csv')
    data_layout_csv_path = os.path.join(data_dir_validation, 'data_layout.csv')
    # camps_csvs are all csv files except refugees.csv and data_layout.csv
    camps_csv_paths = [os.path.join(data_dir_validation, file) for file in os.listdir(data_dir_validation) if file.endswith(".csv") and file != "refugees.csv" and file != "data_layout.csv"]



    # Convert CSV to lists of dictionaries
    location_data = csv_to_list(location_csv_path)
    routes_data = csv_to_list(routes_csv_path)
    conflicts_data = csv_to_list(conflicts_csv_path)
    closures_data = csv_to_list(closures_csv_path)
    reg_corr_data = csv_to_list_reg_corr(reg_corrections_csv_path)
    sim_period_data = csv_to_list_sim_period(sim_period_csv_path)
    validation_refugee_data = csv_to_list(refugees_csv_path)
    validation_data_layout_data = csv_to_list(data_layout_csv_path)
    validation_camps_data = [csv_to_list_camps(camp_csv_path) for camp_csv_path in camps_csv_paths] # list of lists of dicts


    # Transform CSV data to match MongoDB schema
    locations = transform_location_data(location_data)
    routes = transform_routes_data(routes_data)
    conflicts = transform_conflicts_data(conflicts_data)
    closures = transform_closure_data(closures_data)
    reg_corr = transform_reg_corr_data(reg_corr_data)
    sim_period = transform_sim_period_data(sim_period_data)
    validation_refugees = transform_val_refugees_data(validation_refugee_data)
    validation_data_layout = transform_val_data_layout_data(validation_data_layout_data)

    # convert each camp_path to the camp_name
    for i in range(len(camps_csv_paths)):
        camp_path = camps_csv_paths[i]
        # just get the last component of the path
        camp_name = os.path.basename(camp_path)
        # without the extension
        camp_name = os.path.splitext(camp_name)[0]
        camps_csv_paths[i] = camp_name

    # Create the JSON object to be inserted into the MongoDB which stores data in BSON format
    mongo_document = {
        'name': folder_name,
        'region': country,
        'closures': closures,
        'conflicts': conflicts,
        'locations': locations,
        'registration_corrections': reg_corr,
        'routes': routes,
        'sim_period': sim_period[0] if sim_period else None,  # Use the first element or None if the list is empty
        'validation': {
            'refugees': validation_refugees,
            'data_layout': validation_data_layout,
            # dict with filename (last component of path) as key and transformed data as value
            'camps': {camp_path: transform_val_camp_data(camp_data) for camp_path, camp_data in zip(camps_csv_paths, validation_camps_data)}
        },
        'data_sources': {
            'acled': {
                'url': acled_source_list[0],
                'retrieval_date': datetime.strptime(acled_source_list[1], '%Y-%m-%d %H:%M:%S'),
                'last_update': datetime.strptime(acled_source_list[2], '%Y-%m-%d %H:%M:%S'),
                'user_start_date': datetime.strptime(acled_source_list[3], '%Y-%m-%d'),
                'user_end_date': datetime.strptime(acled_source_list[4], '%Y-%m-%d'),
                'oldest_event_date': datetime.strptime(acled_source_list[5], '%Y-%m-%d'),
                'latest_event_date': datetime.strptime(acled_source_list[6], '%Y-%m-%d')
            },
            'population': {
                'url': population_source_list[0],
                'retrieval_date': datetime.strptime(population_source_list[1], '%Y-%m-%d %H:%M:%S'),
                'latest_population_date': datetime.strptime(population_source_list[2], '%Y-%m-%d')
            },
            'camps': {
                'url_from_last_update': camp_source_list[0],
                'retrieval_date': datetime.strptime(camp_source_list[1],'%Y-%m-%d %H:%M:%S'),
                'last_update': datetime.strptime(camp_source_list[2], '%Y-%m-%d'),
                'latest_survey_date': camp_source_list[5],
                'user_start_date': datetime.strptime(camp_source_list[3], '%Y-%m-%d'),
                'user_end_date': datetime.strptime(camp_source_list[4], '%Y-%m-%d'),
            },
            'validation': {
                'url_covered_from': val_source_list[5],
                'url_covered_to': val_source_list[6],
                'retrieval_date': datetime.strptime(val_source_list[0],'%Y-%m-%d %H:%M:%S'),
                'period_covered_from': datetime.strptime(val_source_list[3], '%Y-%m-%d'),
                'period_covered_to': datetime.strptime(val_source_list[4], '%Y-%m-%d'),
                'user_start_date': datetime.strptime(val_source_list[1], '%Y-%m-%d'),
                'user_end_date': datetime.strptime(val_source_list[2], '%Y-%m-%d'),
            }    
            }    
    }

    # insert data into the database
    result = simulations_collection.insert_one(mongo_document)

    # check if successfull 
    if result.acknowledged:
        print(f"Data for {country} successfully inserted into MongoDB")
    else:
        print(f"Data for {country} not inserted into MongoDB")
    
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


# delete  data from the database
"""
delete_ids = ["65a1bfd59dee96171d22019b", "65a1bb68da12cf8b0eadb400", "65a1b3656d8fe4812f76a3e6", "65a1b2ddc7029e006eee6a96", "65a1b236e70523d1f27acc1d", "65abc250f8327531d2990956", "659fc14ffc4a648f45e8c76d", "659ec9ca6b84f57fe76a2521", "659ec951ec0e72e9910d9b9f", "659ec05513b421fda1b5a37f", "659eb0782792d61730ff058d"] # , "659e7977d14212c850a018e0", "658e103c51b9a2ed5ae66fcb", "658dec29819bd1bc1ff738d1", "658dec28819bd1bc1ff738d0", "658dec27819bd1bc1ff738cf", "658dec26819bd1bc1ff738ce", "658dec24819bd1bc1ff738cd"]
for ids in delete_ids:
    delete_data_from_DB(ids)
"""

