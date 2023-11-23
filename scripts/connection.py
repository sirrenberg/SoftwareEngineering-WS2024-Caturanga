import os
import csv

from dotenv import load_dotenv
from pymongo import MongoClient

def csv_to_list_of_dicts(csv_file_path):
    data_list = []

    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.DictReader(csvfile)

        for row in csv_reader:
            data_list.append(dict(row))

    return data_list


# Load environment variables
load_dotenv()
MONGODB_URI = os.environ.get('MONGODB_URI')

client = MongoClient(MONGODB_URI)

db = client.Caturanga

simulations_collection = db.simulations

regions = ["burundi", "cameroon", "drc", "kenya", "nigeria", "rwanda", "tanzania", "uganda"]
file_names = ["closures.csv", "conflicts.csv", "locations.csv", "registration_corrections.csv", "routes.csv", "sim_period.csv"]


# for region in regions:

#   new_simulation = {}
#   new_simulation["region"] = region

#   for file_name in file_names:
#       file_path = os.path.join(os.path.dirname(__file__), "conflict_input", "burundi", file_name)
#       data_list = csv_to_list_of_dicts(file_path)
#       new_simulation[file_name[:-4]] = data_list

#   result = simulations_collection.insert_one(new_simulation)

cursor = simulations_collection.find()

for document in cursor:
    print(document["closures"])
    break


client.close()