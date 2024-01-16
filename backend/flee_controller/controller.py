from pymongo import MongoClient
from dotenv import load_dotenv
from flee_adapter.adapter import Adapter
from flee_controller.csvtransformer import CsvTransformer
import yaml
from bson.objectid import ObjectId as ObjectID
from pathlib import Path
import os


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
        self.client, self.db = self.connect_db()
        self.csvTransformer = CsvTransformer(self.db)

        self.default_input_id = "65a6a042619bb91dd9091165"
        self.default_setting_id = "6599846eeb8f8c36cce8307a"

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
            {"_id": ObjectID(object_id)},
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
            await self.csvTransformer.convert_simulation_to_csv(simulation_id)
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

    async def post_simulation(
                self,
                simulation,
                simulation_id: str = None):
        """
        Posts a new simulation input to the database.

        Parameters:
        - simulation (dict): The new simulation input to be posted.
        - simulation_id (str, optional): The ID of the "basic" input
          to be used as baseline.

        Returns:
        - str: The ID of the inserted simulation input.
        """
        if simulation_id is None:
            simulation_id = self.default_input_id

        return await self.post_data(simulation, "simulations", simulation_id)

# Manage simsettings in DB: ---------------------------------------------------

    async def post_data(
                self,
                data,
                collection_name,
                data_id):
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
        if collection_name == "simulations":
            basic_data = await self.get_simulation(data_id)
        else:
            basic_data = await self.get_simsetting(data_id)

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

    async def post_simsettings(
                self,
                simsetting,
                simsetting_id: str = None):
        """
        Posts a new simulation setting to the database.

        Parameters:
        - simsetting (dict): The new simulation setting to be posted.
        - simsetting_id (str, optional): The ID of the "basic" simsetting
          to be used as baseline.

        Returns:
        - str: The ID of the inserted simulation setting.
        """
        if simsetting_id is None:
            simsetting_id = self.default_setting_id

        return await self.post_data(simsetting, "simsettings", simsetting_id)

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

    # Delete specfici simsettings by simsetting_id:
    async def delete_simsetting(self, simsetting_id: str):
        client, db = self.connect_db()
        db.get_collection("simsettings").delete_one(
            {"_id": ObjectID(simsetting_id)}
        )
        client.close()
        return
