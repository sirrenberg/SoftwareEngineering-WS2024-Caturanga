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
            simulation_config):
        """
        Initializes a simulation by storing the input directory, simsettings,
        validation directory to the filesystem, and returns the object ID,
        simsettings filename, simulation directory, and validation directory.

        Parameters:
        simulation_config (JSONStructure, optional) containing:
        - input_id (str): The ID of the simulation input.
        - input_name (str): The name of the simulation input.
        - simsettings_id (str): The ID of the simulation settings.
        - simsettings_name (str): The name of the simulation settings.

        Returns:
            dict: A dictionary containing the name of the result,
            the IDs mentioned above, the mongodb object ID, simsettings
            filename, simulation directory, and validation directory.
        """
        simulation_id = simulation_config["input"]["input_id"]
        simsettings_id = simulation_config["settings"]["simsettings_id"]

        name = \
            simulation_config["input"]["input_name"] + "(" + \
            simulation_config["settings"]["simsettings_name"] + ")"

        objectid = await self.store_dummy_simulation(
            simulation_id,
            simsettings_id,
            name)

        simsettings_filename = await self.store_simsettings_to_filesystem(
            simsettings_id)

        simulation_dir = await self.store_simulation_to_filesystem(
            simulation_id)

        validation_dir = await self.store_validation_to_filesystem()

        return {"name": name,
                "simulation_id": simulation_id,
                "simsettings_id": simsettings_id,
                "objectid": objectid,
                "simsettings_filename": simsettings_filename,
                "simulation_dir": simulation_dir,
                "validation_dir": validation_dir}

    # Run simulation with provided simulation_id and simsettings_id and store results in DB:
    def run_simulation_config(
            self,
            name: str,
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
            simsettings_id=simsettings_id,
            name=name)

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
            simsettings_id: str = "6570f624987cdd647c68bc7d",
            name: str = "undefined"):
        """
        Stores a simulation result in the database.

        Parameters:
        - result (dict): The result of the simulation.
        - object_id (str): The ID of the dummy simulation result.
        - simulation_id (str): The ID of the simulation input.
          Defaults to "658dec24819bd1bc1ff738cd" (Burundi).
        - simsettings_id (str): The ID of the simulation settings.
          Defaults to "6570f624987cdd647c68bc7d" (Test simsettings).
        - name (str): The name of the simulation result.
          Defaults to "undefined".
        """
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
            {"_id": ObjectID(object_id)},
            new_simulation)
        client.close()

    async def store_dummy_simulation(
                self,
                simulation_id: str = "658dec24819bd1bc1ff738cd",
                simsettings_id: str = "6570f624987cdd647c68bc7d",
                name: str = "undefined"):
        """
        Stores a dummy simulation in the database so that the user can see
        that the simulation is started.

        Parameters:
        - simulation_id (str): The ID of the simulation input.
          Defaults to "658dec24819bd1bc1ff738cd" (Burundi).
        - simsettings_id (str): The ID of the simulation settings.
          Defaults to "6570f624987cdd647c68bc7d" (Test simsettings).
        - name (str): The name of the simulation result.
          Defaults to "undefined".

        Returns:
        - str: The ID of the inserted dummy simulation.
        """
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

    async def get_all_simulation_result_summaries(self):
        """
        Retrieves all simulation result summaries.

        Returns:
        - list of simulation result summaries.
        """
        return await self.get_summaries("simulations_results")

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

    async def get_all_simulation_summaries(self):
        """
        Retrieves all simulation summaries.

        Returns:
        - list of simulation summaries.
        """
        return await self.get_summaries("simulations")

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
            summaries = collection.find({}, {"_id": 1,
                                             "name": 1,
                                             "locations": 1,
                                             "routes": 1})
        else:
            summaries = collection.find({}, {"_id": 1, "name": 1})

        result = []
        for summary in summaries:
            summary["_id"] = str(summary["_id"])
            result.append(summary)

        client.close()

        return result
    
    async def delete_simulation(self, simulation_id: str):
        """
        Deletes a simulation from the database.

        Parameters:
        - simulation_id (str): The ID of the simulation to be deleted.
        """
        return self.delete_document("simulations", simulation_id)


# Manage simsettings in DB: ---------------------------------------------------

    async def post_simsettings(
                self,
                simsetting,
                simsetting_id: str = "6599846eeb8f8c36cce8307a"):
        """
        Posts a new simulation setting to the database.
        More precisely, this function retrieves the "basic" simsetting from the
        database, uses it as a baseline, updates the part that has been
        manipulated by the user and saves the newly created setting to the
        database. This is because parts of the simsetting have implications on
        logging or the required files and format, thus are not relevant to the
        user or might break the simulation (with the current setup),
        and are therefore not shown to the user.

        Parameters:
        - simsetting (dict): The new simulation setting to be posted.
        - simsetting_id (str, optional): The ID of the "basic" simsetting
          to be used as baseline. Defaults to "6599846eeb8f8c36cce8307a".

        Returns:
        - str: The ID of the inserted simulation setting.
        """
        basic_simsetting = await self.get_simsetting(simsetting_id)

        client, db = self.connect_db()

        # remove id to create a NEW simsetting
        try:
            del basic_simsetting["_id"]
            del simsetting["_id"]
        except Exception as e:
            return f"Exception while removing _id key from simsetting: {e}"

        # Update parts of basic simsetting manipulated by the user
        try:
            for key in simsetting:
                basic_simsetting[key] = simsetting[key]
        except Exception as e:
            return f"Exception while updating basic \
                    simsetting with new simsetting: {e}"

        simsettings_collection = db.simsettings
        result = simsettings_collection.insert_one(dict(basic_simsetting))

        client.close()

        return str(result.inserted_id)

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

    async def get_all_simsetting_summaries(self):
        """
        Retrieves all simsetting summaries.

        Returns:
        - list of simsetting summaries.
        """
        return await self.get_summaries("simsettings")

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

    # Delete specific simsettings by simsetting_id:
    async def delete_simsetting(self, simsetting_id: str):
        return self.delete_document("simsettings", simsetting_id)


# Helper functions - Database: ------------------------------------------------


    def delete_document(self, collection_name: str, document_id: str):
        """
        Deletes a document from the specified collection in the database.

        Parameters:
        - collection_name (str): The name of the collection.
        - document_id (str): The ID of the document to be deleted.
        """
        client, db = self.connect_db()
        collection = db.get_collection(collection_name)
        collection.delete_one({"_id": ObjectID(document_id)})
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

