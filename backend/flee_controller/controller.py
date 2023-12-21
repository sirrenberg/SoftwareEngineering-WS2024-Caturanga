from pymongo import MongoClient
from bson.objectid import ObjectId as ObjectID
from dotenv import load_dotenv
from flee_adapter.adapter import Adapter
import os
import yaml



class Controller:

    def __init__(self):
        self.adapter = Adapter()
        load_dotenv()
        self.MONGODB_URI = os.environ.get('MONGO_URI')
        self.client = MongoClient(self.MONGODB_URI)
        self.db = self.client.get_database("Caturanga")


    def run_simulation(self):
        sim = self.adapter.run_simulation()
        self.store_simulation(sim)
        return sim

    async def run_simulation_simsettings(self, simsettings_id: str):

        simsettings = await self.get_simsetting(simsettings_id)
        filename = simsettings_id + ".yml"
        path = os.path.join("flee", "stored_simsettings", filename)

        if not os.path.exists(path):
            try:
                with open(path, 'w') as simsettings_file:
                    yaml.dump(simsettings, simsettings_file, default_flow_style=False)
            except Exception as e:
                return "Error creating Yaml file"

        sim = self.adapter.run_simulation(path)
        self.store_simulation(sim)
        return sim



    def store_simulation(self, result):

        load_dotenv()
        MONGODB_URI = os.environ.get('MONGO_URI')
        client = MongoClient(MONGODB_URI)
        db = client.Caturanga
        simulations_collection = db.simulations_results

        new_simulation = {}
        new_simulation["data"] = result
        simulations_collection.insert_one(new_simulation)

        client.close()

    
    async def get_all_simulation_results(self):
        """
        Retrieves all simulation results from the database.

        Returns:
            list: A list of simulation results, where each result is a dictionary.
        """
        simulations_results_collection = self.db.get_collection("simulations_results")
        simulations_results = simulations_results_collection.find({})
        rl = []
        for simulation in simulations_results:
            simulation["_id"] = str(simulation["_id"])
            rl.append(simulation)
        return rl


    async def get_simulation_result(self, simulation_result_id: str):
        """
        Retrieves a simulation results from the database based on its ID.

        Returns:
            list: A list of simulation results, where each result is a dictionary.
        """
        simulations_results_collection = self.db.get_collection("simulations_results")
        simulation_results = simulations_results_collection.find_one({"_id": ObjectID(simulation_result_id)})
        if simulation_results is not None:
            simulation_results["_id"] = str(simulation_results["_id"])
            return simulation_results
    

    async def get_all_simulations(self):
        """
        Return the data of all simulations.
        """
        """
        results = db.get_collection("simulations")
        results = results.find({

        })
        """
        simulations_collection = self.db.get_collection("simulations")
        simulations = simulations_collection.find({})
        rl = []
        for simulation in simulations:
            simulation["_id"] = str(simulation["_id"])
            rl.append(simulation)
        return rl

    async def get_simulation(self, simulation_id: str):
        """
        Return the data of a simulation based on its ID.

        Example:
            get_simulation("65691061651825804b76fae0")
        """
        simulations_collection = self.db.get_collection("simulations")
        simulation = simulations_collection.find_one({"_id": ObjectID(simulation_id)})
        if simulation is not None:
            simulation["_id"] = str(simulation["_id"])
            return simulation

    async def post_simsettings(self, simsetting):
        simsettings_collection = self.db.simsettings
        simsettings_collection.insert_one(dict(simsetting))
        return 1

    async def get_all_simsettings(self):
        simsettings = self.db.get_collection("simsettings").find({})
        rl = []
        for simsetting in simsettings:
            simsetting["_id"] = str(simsetting["_id"])
            rl.append(simsetting)
        return rl

    async def get_simsetting(self, simsetting_id: str):
        simsetting = self.db.get_collection("simsettings").find_one(
            {"_id": ObjectID(simsetting_id)}
        )
        print(simsetting)
        if simsetting is not None:
            simsetting["_id"] = str(simsetting["_id"])
            return simsetting

    async def delete_simsetting(self, simsetting_id: str):
        return self.db.get_collection("simsettings").delete_one(
            {"_id": ObjectID(simsetting_id)}
        )
