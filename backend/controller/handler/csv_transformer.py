import csv
from datetime import datetime
from io import StringIO
import os


class CsvTransformer:

    """
    CsvTransformer class for transforming and storing data to CSV files.
    CSV Files are needed for FLEE execution
    """

    def __init__(self, backend_root_dir):
        self.backend_root_dir = backend_root_dir

    # Store simulation data from DB in csv files for FLEE execution:
    async def convert_simulation_to_csv(self, simulation):

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
            simulation_dir = self.backend_root_dir / "flee_stored_files" / "conflict_input" / simulation["_id"]
            os.makedirs(simulation_dir, exist_ok=True)

            # Cretae csv files using helper function export-csv (filename, data, fieldnames):
            # Closures.csv file:
            self.export_closures_csv(os.path.join(simulation_dir, "closures.csv"),
                                                    simulation["closures"])

            # conflicts.csv file:
            self.export_conflicts_csv(os.path.join(simulation_dir, "conflicts.csv"),
                                                        simulation["conflicts"],
                                                        simulation["conflicts"][
                                                            0].keys())

            # locations.csv file:
            self.export_locations_csv(os.path.join(simulation_dir, "locations.csv"),
                                                        simulation["locations"],
                                                        ["name", "region", "country", "latitude", "longitude",
                                                        "location_type",
                                                        "conflict_date",
                                                        "population"])

            # routes.csv file:
            self.export_routes_csv(os.path.join(simulation_dir, "routes.csv"),
                                                    simulation["routes"],
                                                    ["from", "to", "distance",
                                                    "forced_redirection"])

            # sim_period.csv file (values are single data points, not directories themselves -> unnested function):
            self.export_sim_period_csv(os.path.join(simulation_dir, "sim_period.csv"),
                                                        simulation["sim_period"])

            return "All files written with csvTransformer"
        except Exception as e:
            raise e

    # Helper Function to create closures.csv file from filename, data and fieldnames:
    def export_closures_csv(self, file_name, data):

        """
        :param file_name: New path of file incl. filename
        :param data: Row data
        :return: Returns nothing, only creates and stores files
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

    # Helper function to create and export the conflicts.csv file
    def export_conflicts_csv(self, file_name, data, fieldnames):
        """
        This function exports data to a CSV file and removes trailing commas.
        :param file_name: New path of file incl. filename
        :param data: Row data
        :param fieldnames: Name of columns in .csv files
        :return: Returns a message indicating success or an error message
        """

        try:
            # Use an in-memory buffer for writing
            csv_buffer = StringIO()
            writer = csv.DictWriter(csv_buffer, fieldnames=fieldnames)

            # Write header:
            writer.writeheader()

            # Adjust data & Skip rows with empty keys and remove trailing commas
            processed_rows = []
            for row in data:
                adjusted_row = {key: value if value != '' else None for key, value in row.items()}
                processed_rows.append(adjusted_row)
                writer.writerow(adjusted_row)

            # Write the processed data back to the file without trailing commas
            with open(file_name, 'w', newline='') as file:
                file.write(csv_buffer.getvalue().strip())

            return "File created and trailing commas removed successfully"

        except Exception as e:
            return str(e)

    # Helper Function to create the locations.csv file from filename, data and fieldnames:
    def export_locations_csv(self, file_name, data, fieldnames):

        """
        :param file_name: New path of file incl. filename
        :param data: Row data
        :param fieldnames: Name of columns in .csv files
        :return: Returns nothing, only creates and stores files
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

    # Helper Function to create the registration_corrections.csv file from filename, data and fieldnames:
    def export_registration_corrections_csv(self, file_name, data):

        """
        :param file_name: New path of file incl. filename
        :param data: Row data
        :return: Returns nothing, only creates and stores files
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

    # Helper Function to create the routes.csv file from filename, data and fieldnames:
    def export_routes_csv(self, file_name, data, fieldnames):

        """
        :param file_name: New path of file incl. filename
        :param data: Row data
        :param fieldnames: Name of columns in .csv files
        :return: Returns nothing, only creates and stores files
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
    def export_sim_period_csv(self, file_name, data):

        """
        :param file_name: New path of file incl. filename
        :param data: Row data
        :return: Returns nothing, only creates and stores files
        """

        print(data)

        try:
            with open(file_name, mode='w', newline='') as csv_file:
                writer = csv.writer(csv_file)

                # Write data:
                for key, value in data.items():
                    if key == "date":
                        if isinstance(value, datetime):
                            formatted_date = value.strftime('%Y-%m-%d')
                            writer.writerow(["StartDate", formatted_date])
                        elif isinstance(value, str):
                            writer.writerow(["StartDate", value[:10]])
                        else:
                            writer.writerow(["StartDate", value])
                    else:
                        writer.writerow([key, value])

                return "File created successfully"

        except Exception as e:
            return str(e)


# Define a custom exception for simulation not found
class SimulationNotFoundError(Exception):
    pass

