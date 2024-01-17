import os
from bson import ObjectId
from dotenv import load_dotenv
from pymongo import MongoClient


class DatabaseHandler:

    def __init__(self, default_input_id, default_setting_id):
        self.default_input_id = default_input_id
        self.default_setting_id = default_setting_id

    def connect_db(self):
        """
        Connects to the database.

        Returns:
            tuple: A tuple containing the MongoClient object and
                   the database object.
        """
        load_dotenv()
        MONGODB_URI = os.environ.get('MONGO_URI')
        client = MongoClient(MONGODB_URI)
        db = client.Caturanga
        return client, db

    async def get(self,
                  collection_name: str,
                  object_id: str):
        """
        Returns a document in a collection.

        Parameters:
        - collection_name (str): The name of the collection.
        - object_id (str): The ID of the document.

        Returns:
        - dict: The document.
        """
        client, db = self.connect_db()
        collection = db.get_collection(collection_name)
        result = collection.find_one({"_id": ObjectId(object_id)})
        client.close()

        if result is not None:
            result["_id"] = str(result["_id"])
            return result
        else:
            return None

    async def get_all(self, collection_name: str):
        """
        Returns all documents in a collection.

        Parameters:
        - collection_name (str): The name of the collection.

        Returns:
        - list: A list containing all documents in the collection.
        """
        client, db = self.connect_db()
        collection = db[collection_name]
        objects = collection.find({})

        result = []
        for object in objects:
            object["_id"] = str(object["_id"])
            result.append(object)

        client.close()

        return result

    async def get_summaries(self, collection_name: str):
        """
        Retrieves summaries from the specified collection in the database.
        A summary contains ID and name of the objects. In the case of
        simulations, the summary also contains the locations and routes,
        which is needed for the map view.

        Parameters:
        - collection (str):
          The name of the collection to retrieve summaries from.

        Returns:
        - list: A list of summaries, where each summary
                is a dictionary with "_id" and "name" fields.
        """
        client, db = self.connect_db()

        collection = db.get_collection(collection_name)
        if collection_name == "simulations":
            summaries = collection.find({}, {
                "_id": 1,
                "name": 1,
                "locations": 1,
                "routes": 1,
                "data_sources": 1})

        elif collection_name == "simulations_results":
            summaries = collection.find({}, {
                "_id": 1,
                "name": 1,
                "simulation_id": 1,
                "status": 1
            })
        else:
            summaries = collection.find({}, {"_id": 1, "name": 1})

        result = []
        for summary in summaries:
            summary["_id"] = str(summary["_id"])
            result.append(summary)

        client.close()

        return result

    async def post(self, data, collection_name, basic_data):
        """
        Posts a new data (input or simsetting) to the database.
        More precisely, this function retrieves the "basic" data (the default,
        which is not modifiable) from the database, uses it as a baseline,
        updates the part that has been manipulated by the user and
        saves the newly created data to the database.
        This is because parts of the data have implications on
        logging or the required files and format, thus are not relevant to the
        user or might break the simulation (with the current setup),
        and are therefore not shown to the user.

        Parameters:
        - data (dict): The new simulation data to be posted.
        - data_id (str, optional): The ID of the "basic" data to be used as
          baseline.

        Returns:
        - str: The ID of the inserted simulation data.
        """

        client, db = self.connect_db()

        try:
            del basic_data["_id"]
            del data["_id"]
        except Exception as e:
            return f"Exception while removing _id key from data: {e}"

        try:
            for key in data:
                basic_data[key] = data[key]
        except Exception as e:
            return f"Exception while updating basic \
                    data with new data: {e}"

        collection = db[collection_name]
        result = collection.insert_one(dict(basic_data))

        client.close()

        return str(result.inserted_id)

    async def delete(self, collection_name: str, object_id: str):
        """
        Deletes a document from the specified collection in the database.

        Parameters:
        - collection_name (str): The name of the collection.
        - object_id (str): The ID of the document to be deleted.

        Returns:
        - dict: A dictionary containing the status of the deletion.
        """
        client, db = self.connect_db()
        collection = db.get_collection(collection_name)
        deleted = collection.delete_one({"_id": ObjectId(object_id)})
        client.close()

        if deleted.deleted_count == 1:
            return {"status": "success"}
        else:
            return {"status": "error"}

    async def delete_simulation_and_associated_results(self,
                                                       simulation_id: str):
        """
        Deletes a simulation from the database. Deletes all simulation results
        associated with the input.

        Parameters:
        - simulation_id (str): The ID of the simulation to be deleted.
        """
        client, db = self.connect_db()
        collection = db.get_collection("simulations_results")
        collection.delete_many({"simulation_id": simulation_id})
        client.close()

        return self.delete("simulations", simulation_id)

    def store_simulation(
            self,
            result,
            object_id: str,
            simulation_id: str = None,
            simsettings_id: str = None,
            name: str = "undefined"):
        """
        Stores a simulation result in the database.

        Parameters:
        - result (dict): The result of the simulation.
        - object_id (str): The ID of the dummy simulation result.
        - simulation_id (str): The ID of the simulation input.
        - simsettings_id (str): The ID of the simulation settings.
        - name (str): The name of the simulation result.
          Defaults to "undefined".
        """
        if simulation_id is None:
            simulation_id = self.default_input_id
        if simsettings_id is None:
            simsettings_id = self.default_setting_id

        client, db = self.connect_db()
        simulations_collection = db.simulations_results
        new_simulation = {}
        new_simulation = {
            "name": name,
            "simulation_id": simulation_id,
            "simsettings_id": simsettings_id
        }
        if "error" in result:
            new_simulation["status"] = "error"
        else:
            new_simulation["status"] = "done"
            new_simulation["data"] = result

        simulations_collection.replace_one(
            {"_id": ObjectId(object_id)},
            new_simulation)
        client.close()

    async def store_dummy_simulation(
            self,
            simulation_id: str = None,
            simsettings_id: str = None,
            name: str = "undefined"):
        """
        Stores a dummy simulation in the database so that the user can see
        that the simulation is started.

        Parameters:
        - simulation_id (str): The ID of the simulation input.
        - simsettings_id (str): The ID of the simulation settings.
        - name (str): The name of the simulation result.
          Defaults to "undefined".

        Returns:
        - str: The ID of the inserted dummy simulation.
        """
        if simulation_id is None:
            simulation_id = self.default_input_id
        if simsettings_id is None:
            simsettings_id = self.default_setting_id

        client, db = self.connect_db()
        collection = db.simulations_results
        dummy_simulation = {}
        dummy_simulation = {
            "name": name,
            "simulation_id": simulation_id,
            "simsettings_id": simsettings_id,
            "status": "running"
        }
        result = collection.insert_one(dummy_simulation)
        client.close()

        return result.inserted_id
