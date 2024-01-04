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

    # Setup of MongoDB DB Connection: ----------------------------------------------------------------------------------
    def __init__(self):
        self.adapter = Adapter()
        load_dotenv()
        self.MONGODB_URI = os.environ.get('MONGO_URI')
        self.client = MongoClient(self.MONGODB_URI)
        self.db = self.client.get_database("Caturanga")

# Run simulations: -------------------------------------------------------------------------------------------------

    # Run default simulation (burundi, default simsettings) and store result:
    def run_simulation(self):
        sim = self.adapter.run_simulation()
        self.store_simulation(sim)
        return sim

    # Run default simulation (burundi) with custom simsettings and store result:
    async def run_simulation_simsettings(self, simsettings_id: str):

        """
        Runs a simulation with custom simsettings, whcih are stored in the DB with simsettings_id.
        Running a custom simulation
        Storing simulation results in DB in connection with Simsettings_id and default location 'burundi'

        :param simsettings_id: Simulation Settings ID in DB
        :return: Simulation results
        """

        ### Store simsettings in filesystem:
        # Get Simsettings from DB:
        try:
            simsettings = await self.get_simsetting(simsettings_id)
        except Exception as e:
            return f"No simsettings with ID {simsettings_id} stored in DB"

        # Get current working drectory:
        backend_root_dir = Path(__file__).resolve().parent

        # Total path to simsettings-file:
        simsettings_dir = backend_root_dir / "flee_stored_files" / "simsettings"
        filename = simsettings_id + ".yml"
        simsettings_filename = simsettings_dir / filename

        # Create simsettings-file:
        if not simsettings_dir.exists():
            simsettings_dir.mkdir(parents=True)

        # Create simsettings-file:
        try:
            with open(simsettings_filename, 'w') as yml_file:
                yaml.dump(simsettings, yml_file, default_flow_style=False, sort_keys=False)
        except Exception as e:
            return "Exception while storing the simsettings.yml file: {e}"

        ### Execute simulation with location data in location_dir and simsettings in simsettings_path:
        sim = self.adapter.run_simulation_ss(simsettings_filename)

        # Store simulation results together with simsettings_id and location string:
        self.store_simulation_config(sim, 'burundi', simsettings_id)

        return sim

    # Run simulation with provided simulation_id and simsettings_id and store results in DB:
    async def run_simulation_config(self, simulation_id: str, simsettings_id: str):

        """
        Runs a simulation with custom simsettings, whcih are stored in the DB with simsettings_id.
        Running a custom simulation
        Storing simulation results in DB in connection with Simsettings_id and custom location name

        :param simulation_id: String of location name e.g. 'burundi'
        :param simsettings_id: Simulation Settings ID in DB
        :return: Returns simulation results
        """

        ### Store simsettings in filesystem:
        # Get Simsettings from DB:
        try:
            simsettings = await self.get_simsetting(simsettings_id)
        except Exception as e:
            return f"No simsettings with ID {simsettings_id} stored in DB"

        # Get current working drectory:
        backend_root_dir = Path(__file__).resolve().parent

        # Total path to simsettings-file:
        simsettings_dir = backend_root_dir / "flee_stored_files" / "simsettings"
        filename = simsettings_id + ".yml"
        simsettings_filename = simsettings_dir / filename

        # Create simsettings-directory:
        if not simsettings_dir.exists():
            simsettings_dir.mkdir(parents=True)

        # Create simsettings-file:
        try:
            with open(simsettings_filename, 'w') as yml_file:
                yaml.dump(simsettings, yml_file, default_flow_style=False, sort_keys=False)
        except Exception as e:
            return "Exception while storing the simsettings.yml file: {e}"

        ### Store location / simulation data in filesystem:
        try:
            await self.convert_simulations_to_csv(simulation_id)
        except Exception as e:
            return f"No simulation with ID {simulation_id} stored in DB"

        # Path to simulation directory (.csv - FLEE files of simulation):
        simulation_dir = backend_root_dir / "flee_stored_files" / "conflict_input" / simulation_id

        # Create simulations-directory:
        if not simulation_dir.exists():
            simulation_dir.mkdir(parents=True)

        ### Execute simulation with location data in location_dir and simsettings in simsettings_path:
        sim = self.adapter.run_simulation_config(simulation_dir, simsettings_filename)

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

    # Store custom simulation with simulation_id and simsettings_id:
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


# Helper functions - Storing .csv-files for given data and path: -------------------------------------------------------

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

                print("1")

                # Cretae csv files using helper function export-csv (filename, data, fieldnames):
                # Closures.csv file:
                self.export_closures_csv(os.path.join(simulation_dir, "closures.csv"), simulation["closures"])
                print("2")
                # conflicts.csv file:
                self.export_csv(os.path.join(simulation_dir, "conflicts.csv"), simulation["conflicts"],
                                simulation["conflicts"][
                                    0].keys())  # In DB hinten null-objekt: :null -> Daher hier ein Komma hinten angehängt
                self.remove_trailing_commas(os.path.join(simulation_dir, "conflicts.csv"))
                print("3")
                # locations.csv file:
                self.export_locations_csv(os.path.join(simulation_dir, "locations.csv"), simulation["locations"],
                                          ["name", "region", "country", "latitude", "longitude", "location_type",
                                           "conflict_date",
                                           "population"])
                print("4")
                # registration_corrections.csv file:
                self.export_registration_corrections_csv(os.path.join(simulation_dir, "registration_corrections.csv"),
                                                         simulation["registration_corrections"])
                print("5")
                # routes.csv file:
                self.export_routes_csv(os.path.join(simulation_dir, "routes.csv"), simulation["routes"],
                                       ["from", "to", "distance",
                                        "forced_redirection"])  # null werte ignoriert -> Freie kommas hinten
                print("6")
                # sim_period.csv file (values are single data points, not directories themselves -> unnested function):
                self.export_csv_sim_period(os.path.join(simulation_dir, "sim_period.csv"), simulation["sim_period"])
                print("7")
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
    def export_registration_corrections_csv(self, file_name, data):

        """
        :param file_name: New path of file incl. filename
        :param data: Row data
        :return: Returns nothin, only creates and stores files
        """

        try:
            with open(file_name, mode='w', newline='') as csv_file:
                writer = csv.writer(csv_file)

                # Write data
                for row in data:
                    name = row['name']
                    date_str = row['date'].strftime('%Y-%m-%d')
                    writer.writerow([name, date_str])

                return "File created succesfully"

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
