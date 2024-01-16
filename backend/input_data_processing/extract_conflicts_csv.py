# This script is partially based on https://github.com/djgroen/FabFlee/blob/master/scripts/04_extract_conflicts_csv.py 
# but changed where necessary to work automatically with the data from the ACLED API and the population data
import os
import pandas as pd
from datetime import datetime
from helper_functions import between_date


def extract_conflicts_csv(folder_name, start_date, max_simulation_end_date):
    '''
    Extract the conflicts.csv file for the specified country and date range. Reads conflict data from the "conflict_info.csv" file, 
    which includes location names, their corresponding start dates, and conflict periods. The function calculates the number of days 
    between the start_date and max_simulation_end_date, then creates a DataFrame with a range of days as columns.
    It populates the DataFrame with 1s for days that fall within the conflict periods of each location and 0s for the rest.

        Parameters:
            folder_name (str): Name of the folder containing the CSV files.
            start_date (str): The starting date to consider when calculating conflict periods (e.g., "01-01-2023").
            max_simulation_end_date (str): The max ending date to limit the number of days in the conflicts.csv file (e.g., "31-12-2023").
    '''

    # Get the current directory
    current_dir = os.getcwd()

    # Load conflict info 
    conflict_info_file = os.path.join(current_dir, folder_name, "conflict_info.csv")
    conflict_info_df = pd.read_csv(conflict_info_file)

    # Calculate the number of days between start_date and max_simulation_end_date
    period = between_date(start_date, max_simulation_end_date)

    conflict_zones = conflict_info_df["name"].tolist()

    # Create a DataFrame to store the conflicts data
    data = {'day': list(range(period + 1))}  # +1 to include max_simulation_end_date
    data.update({zone: [0] * (period + 1) for zone in conflict_zones})
    conflict_df = pd.DataFrame(data)

    # Loop through rows and update the conflicts DataFrame
    for index, row in conflict_info_df.iterrows():
        location = row['name']
        date = row['start_date']
        days = row['conflict_date']

        # Convert the start_date to datetime format
        start_datetime = datetime.strptime(date, "%d-%m-%Y")

        # Calculate the index at which to start marking conflicts
        start_index = (start_datetime - datetime.strptime(start_date, "%d-%m-%Y")).days

        # Calculate the end index of conflicts
        end_index = start_index + days

        # Ensure that the end_index does not exceed the period
        if end_index > period:
            end_index = period

        # Update the corresponding columns with 1s for conflict days, but only up to end_date
        conflict_df.loc[start_index:min(end_index, period), location] = 1


    # Save the conflicts DataFrame to a CSV file
    output_file = os.path.join(current_dir, folder_name, "conflicts.csv")
    conflict_df.to_csv(output_file, index=False)

    # Print a completion message
    print(f'{folder_name}/conflicts.csv created. Please inspect the file for unwanted anomalies!')
