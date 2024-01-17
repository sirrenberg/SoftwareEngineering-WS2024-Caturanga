import yaml
from pathlib import Path
from controller.handler.csv_transformer import CsvTransformer


class FileSystemHandler:

    def __init__(self):
        self.backend_root_dir = Path(__file__).resolve().parent.parent.parent
        self.csv_transformer = CsvTransformer(self.backend_root_dir)

    async def store_simsettings_to_filesystem(
            self,
            simsettings):

        # Total path to simsettings-file:
        simsettings_dir = \
            self.backend_root_dir / "flee_stored_files" / "simsettings"
        filename = simsettings["_id"] + ".yml"
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
            simulation):

        try:
            await self.csv_transformer.convert_simulation_to_csv(simulation)
        except Exception as e:
            return f"Failed converting simulation to csv {e}"

        # Path to simulation directory (.csv - FLEE files of simulation):
        simulation_dir = \
            self.backend_root_dir / "flee_stored_files" / "conflict_input" / \
            simulation["_id"]

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
