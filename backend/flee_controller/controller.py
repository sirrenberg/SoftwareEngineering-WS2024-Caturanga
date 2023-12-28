from pymongo import MongoClient
from bson.objectid import ObjectId as ObjectID
from dotenv import load_dotenv
from flee_adapter.adapter import Adapter
import os


class Controller:
    """
    The Controller class handles the interaction with the database and the execution of simulations.
    """

    def __init__(self):
        """
        Initializes the Controller object.
        """
        self.adapter = Adapter()

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
        result = simsettings_collection.insert_one(dict(simsetting))
        client.close()
        return result

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
        simsetting = db.get_collection("simsettings").delete_one(
            {"_id": ObjectID(simsetting_id)}
        )
        client.close()
        if simsetting.deleted_count == 1:
            return {"ID": simsetting_id, "deleted": True}
        else:
            return {"ID": simsetting_id, "deleted": False}

    def connect_db(self):
        """
        Connects to the database.

        Returns:
            tuple: A tuple containing the MongoClient object and the database object.
        """
        load_dotenv()
        MONGODB_URI = os.environ.get('MONGO_URI')
        client = MongoClient(MONGODB_URI)
        db = client.Caturanga
        return client, db