from pymongo import MongoClient
from bson.objectid import ObjectId as ObjectID
from dotenv import load_dotenv
from flee_adapter.adapter import Adapter
import os
import logging
import boto3
from fastapi import FastAPI, Path, Request
import boto3
from botocore.exceptions import ClientError
import json


logging.basicConfig(level=logging.DEBUG)


class Controller:
    """
    The Controller class handles the interaction with the database and the execution of simulations.
    """

    def __init__(self):
        """
        Initializes the Controller object.
        """
        self.adapter = Adapter()
        secret = self.get_secret("caturanga-db-user-and-pw")
        self.username = secret["username"] # store username and password in environment variables, so that they don't have to be fetched from the AWS Secrets Manager every time, which is expensive
        self.password = secret["password"]

    def run_simulation(self, simulation_id: str):
        """
        Runs a simulation and stores the result in the database.

        Args:
            simulation_id (str): The object ID of the dummy simulation.
        """
        sim = self.adapter.run_simulation()
        self.store_simulation(sim, simulation_id)


    def store_simulation(self, result, object_id: str):
        """
        Stores a simulation result in the database.

        Args:
            result: The result of the simulation.
            object_id (str): The ID of the dummy simulation result.
        """
        client, db = self.connect_db()
        simulations_collection = db.simulations_results
        new_simulation = {}
        new_simulation["data"] = result
        simulations_collection.replace_one({"_id": ObjectID(object_id)}, new_simulation)
        client.close()


    async def store_dummy_simulation(self):
        """
        Stores a dummy simulation in the database so that the user can see that the simulation is started.

        Returns:
            str: The ID of the inserted dummy simulation, so that object can be overwritten.
        """
        client, db = self.connect_db()
        collection = db.simulations_results
        dummy_simulation = {}
        dummy_simulation["data"] = {}
        result = collection.insert_one(dummy_simulation)
        client.close()

        return result.inserted_id


    async def get_all_simulation_results(self):
        """
        Retrieves all simulation results from the database.

        Returns:
            list: A list of simulation results, where each result is a dictionary.
        """
        client, db = self.connect_db()
        simulations_results_collection = db.get_collection("simulations_results")
        simulations_results = simulations_results_collection.find({})
        rl = []
        for simulation in simulations_results:
            simulation["_id"] = str(simulation["_id"])
            rl.append(simulation)

        client.close()
        return rl


    async def get_simulation_result(self, simulation_result_id: str):
        """
        Retrieves a simulation result from the database based on its ID.

        Args:
            simulation_result_id (str): The ID of the simulation result.

        Returns:
            dict: The simulation result.
        """
        client, db = self.connect_db()
        simulations_results_collection = db.get_collection("simulations_results")
        simulation_results = simulations_results_collection.find_one({"_id": ObjectID(simulation_result_id)})
        if simulation_results is not None:
            simulation_results["_id"] = str(simulation_results["_id"])
            client.close()
            return simulation_results
        else:
            client.close()
            return None
    
    
    async def get_all_simulations(self):
        """
        Retrieves all simulations from the database.

        Returns:
            list: A list of simulations, where each simulation is a dictionary.
        """
        client, db = self.connect_db()
        simulations_collection = db.get_collection("simulations")
        simulations = simulations_collection.find({})
        rl = []
        for simulation in simulations:
            simulation["_id"] = str(simulation["_id"])
            rl.append(simulation)
        client.close()
        return rl

    async def get_simulation(self, simulation_id: str):
        """
        Retrieves a simulation from the database based on its ID.

        Args:
            simulation_id (str): The ID of the simulation.

        Returns:
            dict: The simulation.
        """
        client, db = self.connect_db()
        simulations_collection = db.get_collection("simulations")
        simulation = simulations_collection.find_one({"_id": ObjectID(simulation_id)})
        if simulation is not None:
            simulation["_id"] = str(simulation["_id"])
            client.close()
            return simulation
        else:
            client.close()
            return None

    async def post_simsettings(self, simsetting):
        client, db = self.connect_db()
        simsettings_collection = db.simsettings
        simsettings_collection.insert_one(dict(simsetting))
        client.close()
        return 1

    async def get_all_simsettings(self):
        client, db = self.connect_db()
        simsettings = db.get_collection("simsettings").find({})
        rl = []
        for simsetting in simsettings:
            simsetting["_id"] = str(simsetting["_id"])
            rl.append(simsetting)
        client.close()
        return rl

    async def get_simsetting(self, simsetting_id: str):
        client, db = self.connect_db()
        simsetting = db.get_collection("simsettings").find_one(
            {"_id": ObjectID(simsetting_id)}
        )
        print(simsetting)
        if simsetting is not None:
            simsetting["_id"] = str(simsetting["_id"])
            client.close()
            return simsetting
        else:
            client.close()
            return None

    async def delete_simsetting(self, simsetting_id: str):
        client, db = self.connect_db()
        db.get_collection("simsettings").delete_one(
            {"_id": ObjectID(simsetting_id)}
        )
        client.close()
        return 
    
    def get_secret(self, secret_name):
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

    def connect_db(self):
        """
        Connects to the database.

        Returns:
            tuple: A tuple containing the MongoClient object and the database object.
        """
        load_dotenv()
        MONGODB_URI = f"mongodb://{self.username}:{self.password}@caturanga-2023-12-08-16-18-00.cluster-cqhcnfxitkih.eu-west-1.docdb.amazonaws.com:27017/?tls=true&tlsCAFile=global-bundle.pem&replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false"
        client = MongoClient(MONGODB_URI)
        db = client.Caturanga
        return client, db
    