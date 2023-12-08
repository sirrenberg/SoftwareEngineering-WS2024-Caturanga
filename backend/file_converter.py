import os
import csv
from pymongo import MongoClient
from bson.objectid import ObjectId as ObjectID
from datetime import datetime
from dotenv import load_dotenv

# TODO: create a function for DB access
# TODO: create API endpoints for DB access

load_dotenv()
MONGODB_URI = os.environ.get('MONGO_URI')

client = MongoClient(MONGODB_URI)
db = client.get_database("Caturanga")
simulations_collection = db.get_collection("simulations")

# Function to convert CSV to lists of dictionaries
def csv_to_list(file_path):
    with open(file_path, 'r', newline='', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',', quotechar='"')
        data = list(csv_reader)
    return data

def csv_to_list_reg_corr(file_path):
    '''
    In the header of the CSV file, no header is given. Therefore we add the header manually.
    '''
    data = []

    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)
        
        for row in csv_reader:
            name, date = row
            data.append({'name': name, 'date': date})

    return data

def csv_to_list_sim_period(file_path):
    '''
    Convert the simulation period CSV file to a dictionary.
    The rows and columns must be transposed.
    '''
    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)
        rows = list(csv_reader)

    transposed_data = {'date': rows[0][1], 'length': rows[1][1]}
    transposed_data_list = [transposed_data] # convert to list of dicts for consistency with other functions
    return transposed_data_list


# Function to transform location data
def transform_location_data(location_data):
    transformed_data = []
    for row in location_data:
        transformed_data.append({
            'name': row['#name'],
            'region': row['region'],
            'country': row['country'],
            'latitude': float(row['latitude']),
            'longitude': float(row['longitude']),
            'location_type': row['location_type'],
            'conflict_date': int(row['conflict_date']) if row['conflict_date'] else None,
            'population': int(row['population']) if row['population'] else None
        })
    return transformed_data

# Function to transform routes data
def transform_routes_data(routes_data):
    transformed_data = []
    for row in routes_data:
        transformed_data.append({
            'from': row['#name1'],
            'to': row['name2'],
            'distance': float(row['distance']),
            'forced_redirection': float(row['forced_redirection']) if row['forced_redirection'] else None
        })
    return transformed_data

def transform_closure_data(closure_data):
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


# Specify the names of your CSV files
country = 'burundi'

script_dir = os.path.dirname(__file__)
data_dir = os.path.join(script_dir, f'..\\frontend\\src\\test-data\\{country}')

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


# Create the JSON object to be inserted into the MongoDB
mongo_document = {
    'region': country,
    'closures': closures,
    'conflicts': conflicts,
    'locations': locations,
    'registration_corrections': reg_corr,
    'routes': routes,
    'sim_period': sim_period
}



# insert test data into the database
# result = simulations_collection.insert_one(mongo_document)


# delete document from collection
# result = simulations_collection.delete_many({"_id": ObjectID("65690fe42c4979a9ede0b9d0")})

client.close()

