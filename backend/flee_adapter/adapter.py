import subprocess
import os
import pandas as pd
from runscripts.runner import Simulation
from dotenv import load_dotenv
from pymongo import MongoClient

class Adapter:
    def __init__(self):
        # This method is intentionally left empty
        pass
    
    def run_simulation(self):
        sim = Simulation("flee/conflict_input/burundi", "flee/conflict_validation/burundi2015", 0, "flee/test_data/simsetting.yml")
        result = sim.run()
        self.store_simulation(result)
        
        return result
    
    # TODO: This method should be moved to the flee controller
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