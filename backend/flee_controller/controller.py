from datetime import datetime
from pymongo import MongoClient
from bson.objectid import ObjectId as ObjectID
from dotenv import load_dotenv
from flee_adapter.adapter import Adapter
from pathlib import Path
import yaml
import os
import csv


class Controller:
    """
    The Controller class handles the interaction with the database and the
    execution of simulations.
    """

# Setup of MongoDB DB Connection: ---------------------------------------------

    def __init__(self):
        """
        Initializes the Controller object.
        """
        self.adapter = Adapter()
        self.backend_root_dir = Path(__file__).resolve().parent
        load_dotenv()
        self.MONGODB_URI = os.environ.get('MONGO_URI')
        self.client = MongoClient(self.MONGODB_URI)
        self.db = self.client.get_database("Caturanga")

# Run simulations: ------------------------------------------------------------

    async def initialize_simulation(
            self,
            simulation_id: str = "658dec24819bd1bc1ff738cd",
            simsettings_id: str = "6570f624987cdd647c68bc7d"):
        """
        Initializes a simulation by storing the input directory, simsettings,
        validation directory to the filesystem, and returns the object ID,
        simsettings filename, simulation directory, and validation directory.

        Args:
            simulation_id (str): The ID of the simulation. 
            Defaults to "658dec24819bd1bc1ff738cd".(Burundi)
            simsettings_id (str): The ID of the simulation settings.
            Defaults to "6570f624987cdd647c68bc7d".(default)

        Returns:
            dict: A dictionary containing the object ID, simsettings filename,
            simulation directory, and validation directory.
        """

        objectid = await self.store_dummy_simulation(
            simulation_id,
            simsettings_id)

        simsettings_filename = await self.store_simsettings_to_filesystem(
            simsettings_id)

        simulation_dir = await self.store_simulation_to_filesystem(
            simulation_id)

        validation_dir = await self.store_validation_to_filesystem()

        return {"objectid": objectid,
                "simsettings_filename": simsettings_filename,
                "simulation_dir": simulation_dir,
                "validation_dir": validation_dir}

    def run_simulation(self, object_id: str):
        """
        Runs a simulation and stores the result in the database.

        Parameter:
        - simulation_id (str): The object ID of the dummy simulation.
        """
        sim = self.adapter.run_simulation()
        self.store_simulation(sim, object_id)

    # Run default simulation (burundi) with custom simsettings and store result:
    def run_simulation_simsettings(
            self,
            simsettings_id: str,
            object_id: str,
            simsettings_filename: str):
        """
        Runs a simulation with custom simsettings stored in the database
        using the provided simsettings_id.
        Stores the simulation results in the database associated with the
        simsettings_id and the default location 'burundi'.

        Patameter:
        - simsettings_id (str): The ID of the simulation settings in the 
          database.
        - object_id (str): The object ID of the dummy simulation.

        Returns:
        - The simulation results.
        """

        sim = self.adapter.run_simulation_ss(simsettings_filename)

        self.store_simulation(
            sim,
            object_id=object_id,
            simsettings_id=simsettings_id)

    # Run simulation with provided simulation_id and simsettings_id and store results in DB:
    def run_simulation_config(
            self,
            simulation_id: str,
            simsettings_id: str,
            object_id: str,
            simsettings_filename: str,
            simulation_dir: str,
            validation_dir: str):

        """
        Runs a simulation with custom simsettings and input stored in the database
        using the provided simsettings_id and simulation_id.
        Stores the simulation results in the database associated with the
        simsettings_id and the simulation_id.

        :param simulation_id: String of location name e.g. 'burundi'
        :param simsettings_id: Simulation Settings ID in DB
        :return: Returns simulation results
        """

        sim = self.adapter.run_simulation_config(
            simulation_dir,
            simsettings_filename,
            validation_dir)

        self.store_simulation(
            sim,
            object_id=object_id,
            simulation_id=simulation_id,
            simsettings_id=simsettings_id)

# Store results in database: ----------------------------------------------

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

    def store_simulation(
            self,
            result,
            object_id: str,
            simulation_id: str = "658dec24819bd1bc1ff738cd",
            simsettings_id: str = "6570f624987cdd647c68bc7d"):
        """
        Stores a simulation result in the database.

        Parameters:
        - result (dict): The result of the simulation.
        - object_id (str): The ID of the dummy simulation result.
        - simulation_id (str): The ID of the simulation input.
          Defaults to "658dec24819bd1bc1ff738cd" (Burundi).
        - simsettings_id (str): The ID of the simulation settings.
          Defaults to "6570f624987cdd647c68bc7d" (Test simsettings).
        """
        client, db = self.connect_db()
        simulations_collection = db.simulations_results
        new_simulation = {}
        new_simulation = {
            "simulation_id": simulation_id,
            "simsettings_id": simsettings_id,
            "data": result
        }
        simulations_collection.replace_one(
            {"_id": ObjectID(object_id)},
            new_simulation)
        client.close()

    async def store_dummy_simulation(
                self,
                simulation_id: str = "658dec24819bd1bc1ff738cd",
                simsettings_id: str = "6570f624987cdd647c68bc7d"):
        """
        Stores a dummy simulation in the database so that the user can see
        that the simulation is started.

        Parameters:
        - simulation_id (str): The ID of the simulation input.
          Defaults to "658dec24819bd1bc1ff738cd" (Burundi).
        - simsettings_id (str): The ID of the simulation settings.
          Defaults to "6570f624987cdd647c68bc7d" (Test simsettings).

        Returns:
        - str: The ID of the inserted dummy simulation.
        """
        client, db = self.connect_db()
        collection = db.simulations_results
        dummy_simulation = {}
        dummy_simulation = {
            "simulation_id": simulation_id,
            "simsettings_id": simsettings_id,
            "data": {"status": "running"}
        }
        result = collection.insert_one(dummy_simulation)
        client.close()

        return result.inserted_id

# Store results in file system: -------------------------------------------

    async def store_simsettings_to_filesystem(
            self,
            simsettings_id: str):

        # Get Simsettings from DB:
        try:
            simsettings = await self.get_simsetting(simsettings_id)
        except Exception as e:
            return f"No simsettings with ID {simsettings_id} stored in DB: {e}"

        # Total path to simsettings-file:
        simsettings_dir = \
            self.backend_root_dir / "flee_stored_files" / "simsettings"
        filename = simsettings_id + ".yml"
        simsettings_filename = simsettings_dir / filename

        # Create simsettings-directory:
        if not simsettings_dir.exists():
            simsettings_dir.mkdir(parents=True)

        # Create simsettings-file:
        try:
            with open(simsettings_filename, 'w') as yml_file:
                yaml.dump(simsettings, yml_file,
                          default_flow_style=False,
                          sort_keys=False)
        except Exception as e:
            return f"Exception while storing the simsettings.yml file: {e}"

        return simsettings_filename

    async def store_simulation_to_filesystem(
            self,
            simulation_id: str):

        try:
            await self.convert_simulations_to_csv(simulation_id)
        except Exception as e:
            return f"No simulation with ID {simulation_id} stored in DB: {e}"

        # Path to simulation directory (.csv - FLEE files of simulation):
        simulation_dir = \
            self.backend_root_dir / "flee_stored_files" / "conflict_input" / \
            simulation_id

        # Create simulations-directory:
        if not simulation_dir.exists():
            simulation_dir.mkdir(parents=True)

        return simulation_dir

    async def store_validation_to_filesystem(self):

        validation_dir = \
            self.backend_root_dir / "flee_stored_files" / "conflict_validation"
        data_layout = validation_dir / "data_layout.csv"

        if not validation_dir.exists():
            validation_dir.mkdir(parents=True)

        # create an empty csv file
        try:
            open(data_layout, 'w').close()
        except Exception as e:
            return f"Exception while creating data_layout.csv: {e}"

        return validation_dir


# Simulations and Simulation Results: -----------------------------------------

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

    # Return specific simulation by simulation_results_id:
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

    # Get specific simulation by simulation_id:
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


# Manage simsettings in DB: ---------------------------------------------------

    # Store dict of simsettings in DB:
    async def post_simsettings(self, simsetting):
        client, db = self.connect_db()
        simsettings_collection = db.simsettings
        simsettings_collection.insert_one(dict(simsetting))
        client.close()
        return 1

    # Return all stored simsettings of DB:
    async def get_all_simsettings(self):
        client, db = self.connect_db()
        simsettings = db.get_collection("simsettings").find({})
        rl = []
        for simsetting in simsettings:
            simsetting["_id"] = str(simsetting["_id"])
            rl.append(simsetting)
        client.close()
        return rl

    # Get specific simsettings by simsetting_id:
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

    # Get specific simsettings by simsetting_id and return as dict:
    async def get_simsetting_dict(self, simsetting_id: str):
        simsetting = self.db.get_collection("simsettings").find_one(
            {"_id": ObjectID(simsetting_id)}
        )

        if simsetting is not None:
            # Convert the MongoDB document to a dictionary
            simsetting_dict = dict(simsetting)
            simsetting_dict["_id"] = str(simsetting_dict["_id"])
            return simsetting_dict

    # Delete specfici simsettings by simsetting_id:
    async def delete_simsetting(self, simsetting_id: str):
        client, db = self.connect_db()
        db.get_collection("simsettings").delete_one(
            {"_id": ObjectID(simsetting_id)}
        )
        client.close()
        return


# Helper functions - Storing .csv-files for given data and path: --------------

    # Store simulation data from DB in csv files for FLEE execution:
    async def convert_simulations_to_csv(self, simulation_id: str):

        """
        Convert location data into .csv files (for FLEE simulation execution) - Returns location of simulation-data dir:
        Read all data from simulation-collection in DB
        Convert Data into .csv files, which are required by FLEE (closures, conflicts, locations,
        registration_corrections, routes, sim_period)

        :param simulation_id:
        :return:
        """

        # Fetch simulation data from DB by simulation_id:
        try:
            simulations_collection = self.db.get_collection("simulations")
            simulation = simulations_collection.find_one({"_id": ObjectID(simulation_id)})

            # Create all .csv files for simulation:
            if simulation is not None:

                # Create directory for simulation:
                backend_root_dir = Path(__file__).resolve().parent
                simulation_dir = backend_root_dir / "flee_stored_files" / "conflict_input" / simulation_id
                os.makedirs(simulation_dir, exist_ok=True)

                # Cretae csv files using helper function export-csv (filename, data, fieldnames):
                # Closures.csv file:
                self.export_closures_csv(os.path.join(simulation_dir, "closures.csv"), simulation["closures"])
                
                # conflicts.csv file:
                self.export_csv(os.path.join(simulation_dir, "conflicts.csv"), simulation["conflicts"],
                                simulation["conflicts"][
                                    0].keys())  # In DB hinten null-objekt: :null -> Daher hier ein Komma hinten angehängt
                self.remove_trailing_commas(os.path.join(simulation_dir, "conflicts.csv"))
                
                # locations.csv file:
                self.export_locations_csv(os.path.join(simulation_dir, "locations.csv"), simulation["locations"],
                                          ["name", "region", "country", "latitude", "longitude", "location_type",
                                           "conflict_date",
                                           "population"])
                
                # routes.csv file:
                self.export_routes_csv(os.path.join(simulation_dir, "routes.csv"), simulation["routes"],
                                       ["from", "to", "distance",
                                        "forced_redirection"])  # null werte ignoriert -> Freie kommas hinten
                
                # sim_period.csv file (values are single data points, not directories themselves -> unnested function):
                self.export_csv_sim_period(os.path.join(simulation_dir, "sim_period.csv"), simulation["sim_period"])
                
                return "All files written"

            else:
                raise SimulationNotFoundError(f"Simulation with ID {simulation_id} not found")

        except Exception as e:
            raise e


    # Helper Function to create csv-file from filename, data and fieldnames:
    def export_closures_csv(self, file_name, data):

        """
        :param file_name: New path of file incl. filename
        :param data: Row data
        :return: Returns nothin, only creates and stores files
        """

        try:
            with open(file_name, mode='w', newline='') as csv_file:
                fieldnames = ['#closure_type', 'name1', 'name2', 'closure_start', 'closure_end']
                writer = csv.writer(csv_file)

                # Write header:
                writer.writerow(fieldnames)

                # Write data & Skip rows with empty keys
                for row in data:
                    writer.writerow([
                        int(value) if value and isinstance(value, (int, float)) else value
                        for value in row.values()
                    ])

                return "File created succesfully"

        except Exception as e:
            return e

    # Helper Function to create csv-file from filename, data and fieldnames:
    def export_csv(self, file_name, data, fieldnames):

        """
        :param file_name: New path of file incl. filename
        :param data: Row data
        :param fieldnames: Name of columns in .csv files
        :return: Returns nothin, only creates and stores files
        """

        try:
            with open(file_name, mode='w', newline='') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

                # Write header:
                writer.writeheader()

                # Write data & Skip rows with empty keys
                for row in data:
                    if any(value == '' for value in row.values()):
                        continue
                    writer.writerow(row)

                return "File created succesfully"

        except Exception as e:
            return e

    # Helper Function to create csv-file from filename, data and fieldnames:
    def export_locations_csv(self, file_name, data, fieldnames):

        """
        :param file_name: New path of file incl. filename
        :param data: Row data
        :param fieldnames: Name of columns in .csv files
        :return: Returns nothin, only creates and stores files
        """

        try:
            with open(file_name, mode='w', newline='', encoding='utf-8') as csv_file:
                writer = csv.writer(csv_file, quoting=csv.QUOTE_NONNUMERIC)

                # Write header:
                writer.writerow(['#' + field if field == 'name' else field for field in fieldnames])

                # Write data & Skip rows with empty keys
                for row in data:
                    if any(value == '' for value in row.values()):
                        continue
                    writer.writerow(
                        [str(value) if value and not isinstance(value, (int, float)) else value for value in
                         row.values()])

                return "File created successfully"

        except Exception as e:
            return e

    # Helper Function to create csv-file from filename, data and fieldnames:
    def export_routes_csv(self, file_name, data, fieldnames):

        """
        :param file_name: New path of file incl. filename
        :param data: Row data
        :param fieldnames: Name of columns in .csv files
        :return: Returns nothin, only creates and stores files
        """

        try:
            with open(file_name, mode='w', newline='') as csv_file:
                fieldnames = ['#name1', 'name2', 'distance', 'forced_redirection']
                writer = csv.writer(csv_file)

                # Write header:
                writer.writerow(fieldnames)

                # Write data & Skip rows with empty keys
                for row in data:
                    writer.writerow([
                        int(value) if value and isinstance(value, (int, float)) and value != '0.0'
                        else value if not (value == 0.0 or value == '0.0')
                        else None
                        for value in row.values()
                    ])

        except Exception as e:
            return e

    # Helper function for single value pairs, where values don´t represent own dictionaries themselves (sim_period)
    def export_csv_sim_period(self, file_name, data):

        """
        :param file_name: New path of file incl. filename
        :param data: Row data
        :param fieldnames: Name of columns in .csv files
        :return: Returns nothin, only creates and stores files
        """

        print(data)

        try:
            with open(file_name, mode='w', newline='') as csv_file:
                writer = csv.writer(csv_file)

                # Write data:
                for key, value in data.items():
                    if isinstance(value, datetime):
                        formatted_date = value.strftime('%Y-%m-%d')
                        writer.writerow(["StartDate", formatted_date])
                    else:
                        writer.writerow([key, value])

                return "File created successfully"

        except Exception as e:
            return str(e)

    # Function to remove trailing commas from .csv file (conflicts.csv):
    def remove_trailing_commas(self, file_name):

        input_file_path = file_name
        output_file_path = file_name

        # Read data from the input file
        with open(input_file_path, 'r') as input_file:
            reader = csv.reader(input_file)
            rows = list(reader)

        # Remove trailing commas:
        processed_rows = [row[:-1] if row[-1] == '' else row for row in rows]

        # Write the processed data back to the same file
        with open(output_file_path, 'w', newline='') as file:
            # Write the processed rows back to the CSV file
            writer = csv.writer(file)
            writer.writerows(processed_rows)


# Helper functions - reading files: ------------------------------------------------------------------------------------

    # Read .yml file for given simsettings:
    def testread_ss(self, simsettings_id: str):
        """
        Read a dummy simulation result from the database.
        """

        filename = simsettings_id + ".yml"
        backend_root_dir = Path(__file__).resolve().parent
        simsettings_dir = backend_root_dir / "flee_stored_files" / "simsettings"
        simsettings_filename = simsettings_dir / filename

        try:
            with open(simsettings_filename, 'r') as f:
                return f.read()
        except Exception as e:
                return "File nicht vorhanden"

    # Read all .csv files for given simulation:
    def testread_csv(self, simulation_id):

        backend_root_dir = Path(__file__).resolve().parent
        sim_dir = backend_root_dir / "flee_stored_files" / "conflict_input" / simulation_id
        sim_filename1 = sim_dir / "closures.csv"
        sim_filename2 = sim_dir / "conflicts.csv"
        sim_filename3 = sim_dir / "locations.csv"
        sim_filename4 = sim_dir / "registration_corrections.csv"
        sim_filename5 = sim_dir / "routes.csv"
        sim_filename6 = sim_dir / "sim_period.csv"

        try:
            with open(sim_filename1, 'r') as f:
                f1 = f.read()
        except Exception as e:
            return "File1 nicht vorhanden"
        try:
            with open(sim_filename2, 'r') as f:
                f2 = f.read()
        except Exception as e:
            return "File2 nicht vorhanden"
        try:
            with open(sim_filename3, 'r') as f:
                f3 = f.read()
        except Exception as e:
            return "File3 nicht vorhanden"
        try:
            with open(sim_filename4, 'r') as f:
                f4 = f.read()
        except Exception as e:
            return "File4 nicht vorhanden"
        try:
            with open(sim_filename5, 'r') as f:
                f5 = f.read()
        except Exception as e:
            return "File5 nicht vorhanden"
        try:
            with open(sim_filename6, 'r') as f:
                f6 = f.read()
        except Exception as e:
            return "File6 nicht vorhanden"
        return f1, f2, f3, f4, f5, f6


# Define a custom exception for simulation not found
class SimulationNotFoundError(Exception):
    pass

