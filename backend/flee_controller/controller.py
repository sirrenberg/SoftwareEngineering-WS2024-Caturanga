import csv

from pymongo import MongoClient
from bson.objectid import ObjectId as ObjectID
from dotenv import load_dotenv
from flee_adapter.adapter import Adapter
from pathlib import Path
import yaml
import os


class Controller:

    # Setup of MongoDB DB Connection: ----------------------------------------------------------------------------------
    def __init__(self):
        self.adapter = Adapter()
        load_dotenv()
        self.MONGODB_URI = os.environ.get('MONGO_URI')
        self.client = MongoClient(self.MONGODB_URI)
        self.db = self.client.get_database("Caturanga")


    # Run simulations: -------------------------------------------------------------------------------------------------

    # Run default simulation and store result:
    def run_simulation(self):
        sim = self.adapter.run_simulation()
        self.store_simulation(sim)
        return sim

    # Run default (burundi) simulatino with custom simsettings and store result:
    async def run_simulation_simsettings(self, simsettings_id: str):

        """

        Runs a simulation with custom simsettings, whcih are stored in the DB with simsettings_id.
        Running a custom simulation
        Storing simulation results in DB in connection with Simsettings_id and default location 'burundi'

        :param simsettings_id: Simulation Settings ID in DB
        :return: Simulation results

        """

        simsettings = await self.get_simsetting(simsettings_id)

        backend_root_dir = Path(__file__).resolve().parent
        simsettings_dir = backend_root_dir / "flee_stored_files" / "simsettings"
        filename = simsettings_id + ".yml"
        simsettings_filename = simsettings_dir / filename

        if not simsettings_dir.exists():
            simsettings_dir.mkdir(parents=True)

        try:
            with open(simsettings_filename, 'w') as yml_file:
                yaml.dump(simsettings, yml_file, default_flow_style=False, sort_keys=False)

        except Exception as e:
            return "Exception while storing the simsettings.yml file: {e}"

        sim = self.adapter.run_simulation_ss(simsettings_filename)
        self.store_simulation(sim)
        self.store_simulation_config(sim, 'burundi', simsettings_id)

        return sim



    # Run simulation with provided simsettings-ID and location name:
    async def run_simulation_config(self, simulation_id: str, simsettings_id: str):

        '''

        Runs a simulation with custom simsettings, whcih are stored in the DB with simsettings_id.
        Running a custom simulation
        Storing simulation results in DB in connection with Simsettings_id and custom location name

        :param location: String of location name e.g. 'burundi'
        :param simsettings_id: Simulation Settings ID in DB
        :return: Returns simulation results

        '''

        # Get Simsettings from DB:
        simsettings = await self.get_simsetting(simsettings_id)

        # Get current working drectory:
        backend_root_dir = Path(__file__).resolve().parent

        # Total path to simsettings-file:
        simsettings_dir = backend_root_dir / "flee_stored_files" / "simsettings"
        filename = simsettings_id + ".yml"
        simsettings_filename = simsettings_dir / filename

        #Create simsettings-file:
        if not simsettings_dir.exists():
            simsettings_dir.mkdir(parents=True)

        try:
            with open(simsettings_filename, 'w') as yml_file:
                yaml.dump(simsettings, yml_file, default_flow_style=False, sort_keys=False)
        except Exception as e:
            return "Exception while storing the simsettings.yml file: {e}"

        # Get Path to location data from location directory:
        self.convert_simulations_to_csv(simulation_id)

        # Path to simulation directory (.csv - FLEE files of simulation):
        simulation_dir = backend_root_dir / "flee_stored_files" / "conflict_input" / simulation_id

        # Run simulation with location data in location_dir and simsettings in simsettings_path:
        sim = self.adapter.run_simulation(simulation_dir, simsettings_filename)
        self.store_simulation(sim)

        # Store simulation results together with simsettings_id and location string:
        self.store_simulation_config(sim, simulation_id, simsettings_id)

        return sim


    # Return simulation values from DB: --------------------------------------------------------------------------------

    # Return all simulsation Results:
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

    # Return specific simulation by simulation_results_id:
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

    # Get all simulations (not simulation results):
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

    # Get specific simulation by simulation_id:
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


    # Manage simsettings in DB: ----------------------------------------------------------------------------------------

    # Store dict of simsettings in DB:
    async def post_simsettings(self, simsetting):
        simsettings_collection = self.db.simsettings
        simsettings_collection.insert_one(dict(simsetting))
        return 1

    # Return all stored simsettings of DB:
    async def get_all_simsettings(self):
        simsettings = self.db.get_collection("simsettings").find({})
        rl = []
        for simsetting in simsettings:
            simsetting["_id"] = str(simsetting["_id"])
            rl.append(simsetting)
        return rl

    # Get specific simsettings by simsetting_id:
    async def get_simsetting(self, simsetting_id: str):
        simsetting = self.db.get_collection("simsettings").find_one(
            {"_id": ObjectID(simsetting_id)}
        )
        print(simsetting)
        if simsetting is not None:
            simsetting["_id"] = str(simsetting["_id"])
            return simsetting

    async def get_simsetting_dict(self, simsetting_id: str):
        simsetting = self.db.get_collection("simsettings").find_one(
            {"_id": ObjectID(simsetting_id)}
        )
        print(type(simsetting), simsetting)

        if simsetting is not None:
            # Convert the MongoDB document to a dictionary
            simsetting_dict = dict(simsetting)
            simsetting_dict["_id"] = str(simsetting_dict["_id"])
            return simsetting_dict


    # Delete specfici simsettings by simsetting_id:
    async def delete_simsetting(self, simsetting_id: str):
        return self.db.get_collection("simsettings").delete_one(
            {"_id": ObjectID(simsetting_id)}
        )


    # Store simulation results: ----------------------------------------------------------------------------------------

    # Store default simulation without custom location and simsettings:
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

    # Store custom simulation with location and simsettings:
    def store_simulation_config(self, result, simulation_id, simsettings_id):

        load_dotenv()
        MONGODB_URI = os.environ.get('MONGO_URI')
        client = MongoClient(MONGODB_URI)
        db = client.Caturanga
        simulations_collection = db.simulations_results

        new_simulation = {}
        new_simulation = {
            "simulation_id": simulation_id,
            "simsettings_id": simsettings_id,  # Add the relevant simsettings_ID to the dictionary
            "data": result
        }

        simulations_collection.insert_one(new_simulation)
        client.close()

    # Store simulation data from DB in csv files for FLEE execution: ---------------------------------------------------

    # Convert location data into .csv files (for FLEE simulation execution) - Returns location of simulation-data dir:
    async def convert_simulations_to_csv(self, simulation_id: str):

        '''
        Read all data from simulation-collection in DB
        Convert Data into .csv files, which are required by FLEE (closures, conflicts, locations,
        registration_corrections, routes, sim_period)
        
        :param simulation_id:
        :return:
        '''

        # Fetch simulation data from DB by simulation_id:
        simulations_collection = self.db.get_collection("simulations")
        simulation = simulations_collection.find_one({"_id": ObjectID(simulation_id)})

        # Create all .csv files for simulation:
        if simulation is not None:

            # Create directory for simulation:
            backend_root_dir = Path(__file__).resolve().parent
            simulation_dir = backend_root_dir / "flee_stored_files" / "conflict_input" / simulation_id
            os.makedirs(simulation_dir, exist_ok=True)

            # Cretae csv files using helper function export-csv (filename, data, fieldnames):
            self.export_csv(os.path.join(simulation_dir, "closures.csv"), simulation["closures"],
                            ["closure_type", "name1", "name2", "closure_start", "closure_end"])

            self.export_csv(os.path.join(simulation_dir, "conflicts.csv"), simulation["conflicts"],
                            simulation["conflicts"][0].keys())

            self.export_csv(os.path.join(simulation_dir, "locations.csv"), simulation["locations"],
                            ["name", "region", "country", "latitude", "longitude", "location_type", "conflict_date",
                             "population"])

            self.export_csv(os.path.join(simulation_dir, "registration_corrections.csv"),
                            simulation["registration_corrections"], ["name", "date"])

            self.export_csv(os.path.join(simulation_dir, "routes.csv"), simulation["routes"],
                            ["from", "to", "distance", "forced_redirection"])       # Kommas hinten dran

            self.export_csv(os.path.join(simulation_dir, "sim_period.csv"), simulation["sim_period"],
                            ["date", "length"])     # TBD Hier fehlen Werte für date und length


            return "All files created"

        else:
            return "No simulations in Database"



    # Helper Function to create csv-file from filename, data and fieldnames:
    def export_csv(self, file_name, data, fieldnames):

        '''

        :param file_name: New path of file incl. filename
        :param data: Row data
        :param fieldnames: Name of columns in .csv files
        :return: Returns nothin, only creates and stores files

        '''

        try:
            with open(file_name, mode='w', newline='') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

                # Write header:
                writer.writeheader()

                # Write data:
                writer.writerows(data)

                return "File created succesfully"

        except Exception as e:
            return e





# ----------------------------------------------------------------------------------------------------------------------
    def testread_ss(self):
        """
        Read a dummy simulation result from the database.
        """
        from pathlib import Path

        filename = "6570f624987cdd647c68bc7d" + ".yml"
        backend_root_dir = Path(__file__).resolve().parent
        simsettings_dir = backend_root_dir / "flee_stored_files" / "simsettings"
        simsettings_filename = simsettings_dir / "6570f624987cdd647c68bc7d.yml"

        try:
            with open(simsettings_filename, 'r') as f:
                return f.read()
        except Exception as e:
                return "File nicht vorhanden"

    # ---------------------------------------
    def testread_csv(self):

        from pathlib import Path

        backend_root_dir = Path(__file__).resolve().parent
        sim_dir = backend_root_dir / "flee_stored_files" / "conflict_input" / "658dec24819bd1bc1ff738cd"
        sim_filename = sim_dir / "sim_period.csv"

        try:
            with open(sim_filename, 'r') as f:
                return f.read()
        except Exception as e:
            return "File nicht vorhanden"