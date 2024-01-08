from fastapi import FastAPI, Path, Request
import logging
import boto3
from botocore.exceptions import ClientError
import json
from pymongo import MongoClient
from bson.objectid import ObjectId as ObjectID
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

logging.basicConfig(level=logging.DEBUG)
app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,  # allow cookies
    allow_methods=["*"],  # allow all methods
    allow_headers=["*"],  # allow all headers
)

@app.get("/")
def read_root():
    return {"data": "Welcome to the DB migration!"}


@app.get("/username")
def read_user():
    logging.debug("Trying to invoke get_secret() from main.py...")
    username = get_secret("caturanga-db-user-and-pw")
    logging.debug(
        "get_secret() invoked from main(). Username is of type: " + str(type(username))
    )
    return {"username": get_secret("caturanga-db-user-and-pw")["username"]}

@app.get("/simsettings")
def get_all_simsettings():
    client, db = connect_db()
    simsettings = db.get_collection("simsettings").find({})
    rl = []
    for simsetting in simsettings:
        simsetting["_id"] = str(simsetting["_id"])
        rl.append(simsetting)
    client.close()
    return rl

@app.get("/simulations")
def get_all_simulations():
    client, db = connect_db()
    simulations = db.get_collection("simulations").find({})
    rl = []
    for simulation in simulations:
        simulation["_id"] = str(simulation["_id"])
        rl.append(simulation)
    client.close()
    return rl

@app.get("/simulationresults")
async def get_all_simulation_results():
    """
    Retrieves all simulation results from the database.

    Returns:
        list: A list of simulation results, where each result is a dictionary.
    """
    client, db = connect_db()
    simulations_results_collection = db.get_collection("simulations_results")
    simulations_results = simulations_results_collection.find({})
    rl = []
    for simulation in simulations_results:
        simulation["_id"] = str(simulation["_id"])
        rl.append(simulation)

    client.close()
    return rl

def get_secret(secret_name):
    """
    Retrieves the secret value that contains the username and password for the documentDB database from the AWS Secrets Manager.
    """
    logging.basicConfig(level=logging.DEBUG)
    region_name = "eu-west-1"

    # Create a Secrets Manager client
    logging.debug("Creating a boto3 session...")
    session = boto3.session.Session()
    logging.debug("Session created. Session is of type: " + str(type(session)))
    logging.debug("Creating a boto3 client...")
    client = session.client(service_name="secretsmanager", region_name=region_name)
    logging.debug("Client created. Client is of type: " + str(type(client)))

    try:
        logging.debug("Trying to get secret value...")
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        logging.debug(
            "Secret value retrieved. Secret value is of type: "
            + str(type(get_secret_value_response))
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        return e

    logging.debug("Trying to parse secret value...")
    secret = get_secret_value_response["SecretString"]
    logging.debug("Secret value parsed. Secret value is of type: " + str(type(secret)))

    json_secret = json.loads(secret)
    print("Type of json_secret:" + str(type(json_secret)))

    logging.debug("Trying to parse secret value as JSON...")
    username = json_secret["username"]
    print("Username is " + str(username))
    logging.debug(
        "Secret value parsed as JSON. Username is of type: " + str(type(username))
    )

    return json.loads(secret)

def connect_db():
    """
    Connects to the database.

    Returns:
        tuple: A tuple containing the MongoClient object and the database object.
    """
    load_dotenv()
    secret = get_secret("caturanga-db-user-and-pw")
    username = secret["username"]
    password = secret["password"]
    MONGODB_URI = f"mongodb://{username}:{password}@caturanga-2023-12-08-16-18-00.cluster-cqhcnfxitkih.eu-west-1.docdb.amazonaws.com:27017/?tls=true&tlsCAFile=global-bundle.pem&replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false"
    client = MongoClient(MONGODB_URI)
    db = client.Caturanga
    return client, db

def connect_atlas_db():
    """
    Connects to the database.

    Returns:
        tuple: A tuple containing the MongoClient object and the database object.
    """
    load_dotenv()
    secret = get_secret("password-for-atlas")
    username = secret["username"]
    password = secret["password"]
    MONGODB_URI = f"mongodb+srv://{username}:{password}@caturanga.o94xzij.mongodb.net/?retryWrites=true&w=majority"
    atlas_client = MongoClient(MONGODB_URI)
    atlas_db = atlas_client.Caturanga
    return atlas_client, atlas_db

@app.get("/migrate")
def migrate_from_atlas():
    """
    Insert all data from the Atlas database into the Amazon DocumentDB database.
    """
    atlas_client, atlas_db = connect_atlas_db()
    atlas_collection_names = atlas_db.list_collection_names()
    for collection_name in atlas_collection_names:
        atlas_collection = atlas_db.get_collection(collection_name)
        atlas_documents = atlas_collection.find({})
        for document in atlas_documents:
            aws_ddb_client, aws_ddb_db = connect_db()
            aws_ddb_db.get_collection(collection_name).insert_one(document)
            aws_ddb_client.close()

    atlas_client.close()
    return "Migration successful."

@app.get("/delete_all_in_document_db")
def delete_all_in_document_db():
    """
    Insert all data from the Atlas database into the Amazon DocumentDB database.
    """
    aws_ddb_client, aws_ddb_db = connect_db()
    collection_names = aws_ddb_db.list_collection_names()
    for collection_name in collection_names:
        aws_ddb_db[collection_name].drop()
    aws_ddb_client.close()
    return "Deletion successful."

@app.get("/documents")
def atlas_documents():
    """
    Insert all data from the Atlas database into the Amazon DocumentDB database.
    """
    atlas_client, atlas_db = connect_atlas_db()
    atlas_collection_names = atlas_db.list_collection_names()
    docs = []
    for collection_name in atlas_collection_names:
        atlas_collection = atlas_db.get_collection(collection_name)
        atlas_documents = atlas_collection.find({})
        for document in atlas_documents:
            docs.append(document)

    atlas_client.close()
    return docs

@app.get("/dsimsettings/{simsetting_id}")
async def delete_simsetting(simsetting_id: str):
    client, db = connect_db()
    db.get_collection("simsettings").delete_one(
        {"_id": ObjectID(simsetting_id)}
    )
    client.close()
    return 

@app.get("/dsimulationresults/{results_id}")
async def delete_simulationresults(results_id: str):
    client, db = connect_db()
    db.get_collection("simulations_results").delete_one(
        {"_id": ObjectID(results_id)}
    )
    client.close()
    return 

@app.get("/dsimulations/{sim_id}")
async def delete_simulations(sim_id: str):
    client, db = connect_db()
    db.get_collection("simulations").delete_one(
        {"_id": ObjectID(sim_id)}
    )
    client.close()
    return 