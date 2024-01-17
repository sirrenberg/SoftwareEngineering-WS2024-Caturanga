from input_data_processing.helper_functions import date_format
import subprocess


class DataExtractor:

    def run_data_extraction(self,
                            country_name,
                            start_date,
                            end_date,
                            max_simulation_end_date):
        try:
            # check invalid dates
            if date_format(start_date) > date_format(end_date):
                return \
                    {"success": False,
                     "error": "Start date is after the end date of fetching."}
            elif date_format(start_date) > date_format(
                    max_simulation_end_date):
                return {"success": False,
                        "error": "Start date is after simulation end date."}

            # Command to execute the run_data_extraction.py script
            script_path = "input_data_processing/run_data_extraction.py"
            result = subprocess.run(
                ["python",
                 script_path,
                 country_name,
                 start_date,
                 end_date,
                 max_simulation_end_date],
                capture_output=True,
                text=True,
                check=True
            )

            # If the script runs successfully, return the output
            return {"success": True, "output": result.stdout}

        except subprocess.CalledProcessError as e:
            # If an error occurs during script execution
            return {"success": False, "error": e.stderr}
