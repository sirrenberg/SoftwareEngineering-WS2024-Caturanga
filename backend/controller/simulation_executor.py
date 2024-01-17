from flee_adapter.adapter import Adapter
from controller.handler.filesystem_handler import FileSystemHandler


class SimulationExecutor:
    """
    The SimulationExecutor class is responsible for initializing and running
    simulations. It interacts with the FleeAdapter to execute the simulations.
    """

    def __init__(self, database_handler):
        self.database_handler = database_handler
        self.flee_adapter = Adapter()
        self.file_system_handler = FileSystemHandler()

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

        objectid = await self.database_handler.store_dummy_simulation(
            simulation_id,
            simsettings_id,
            name)

        simsetting = await self.database_handler.get("simsettings",
                                                     simsettings_id)
        simsettings_filename = \
            await self.file_system_handler.store_simsettings_to_filesystem(
                simsetting
                )

        simulation = await self.database_handler.get("simulations",
                                                     simulation_id)

        simulation_dir = \
            await self.file_system_handler.store_simulation_to_filesystem(
                simulation
                )

        validation_dir = \
            await self.file_system_handler.store_validation_to_filesystem()

        return {"name": name,
                "simulation_id": simulation_id,
                "simsettings_id": simsettings_id,
                "objectid": objectid,
                "simsettings_filename": simsettings_filename,
                "simulation_dir": simulation_dir,
                "validation_dir": validation_dir}

    def run_simulation(
            self,
            name: str,
            simulation_id: str,
            simsettings_id: str,
            object_id: str,
            simsettings_filename: str,
            simulation_dir: str,
            validation_dir: str):

        """
        Runs a simulation with custom simsettings and input stored in the
        database using the provided simsettings_id and simulation_id.
        Stores the simulation results in the database associated with the
        simsettings_id and the simulation_id.

        :param simulation_id: String of location name e.g. 'burundi'
        :param simsettings_id: Simulation Settings ID in DB
        :return: Returns simulation results
        """

        sim = self.flee_adapter.run_simulation_config(
            simulation_dir,
            simsettings_filename,
            validation_dir)

        self.database_handler.store_simulation(
            sim,
            object_id=object_id,
            simulation_id=simulation_id,
            simsettings_id=simsettings_id,
            name=name)
