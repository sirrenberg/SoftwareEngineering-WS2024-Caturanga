# This script is based on https://github.com/djgroen/FabFlee/blob/master/scripts/04_extract_conflicts_csv.py 
# but changed where necessary to work automatically with the data from the ACLED API and the population data

import os
import pandas as pd
from datetime import datetime


def between_date(d1, d2):
    '''
    Function to calculate the number of days between two dates in "dd-mm-yyyy" format
        Parameters:
            d1 (str): First date in "dd-mm-yyyy" format
            d2 (str): Second date in "dd-mm-yyyy" format
        Returns:
            (int): Number of days between the two dates
    '''
    d1list = d1.split("-")
    d2list = d2.split("-")
    date1 = datetime(int(d1list[2]), int(d1list[1]), int(d1list[0]))
    date2 = datetime(int(d2list[2]), int(d2list[1]), int(d2list[0]))

    return abs((date1 - date2).days)


def extract_conflicts_csv(folder_name, start_date, end_date):
    '''
    Extract the conflicts.csv file for the specified country and date range. Reads conflict data from the "conflict_info.csv" file, 
    which includes location names, their corresponding start dates, and conflict periods. The function calculates the number of days 
    between the start_date and end_date, then creates a DataFrame with a range of days as columns.
    It populates the DataFrame with 1s for days that fall within the conflict periods of each location and 0s for the rest.

        Parameters:
            folder_name (str): Name of the folder containing the CSV files.
            start_date (str): The starting date to consider when calculating conflict periods (e.g., "01-01-2023").
            end_date (str): The ending date to limit the number of days in the conflicts.csv file (e.g., "31-12-2023").
    '''

    # Get the current directory
    current_dir = os.getcwd()

    # Load conflict info 
    conflict_info_file = os.path.join(current_dir, folder_name, "conflict_info.csv")
    conflict_info_df = pd.read_csv(conflict_info_file)

    # Calculate the number of days between start_date and end_date
    period = between_date(start_date, end_date)

    conflict_zones = conflict_info_df["name"].tolist()

    # Create a DataFrame to store the conflicts data
    data = {'day': list(range(period + 1))}  # +1 to include end_date
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

        # Update the corresponding columns with 1s for conflict days
        conflict_df.loc[start_index:end_index, location] = 1

    # Save the conflicts DataFrame to a CSV file
    output_file = os.path.join(current_dir, folder_name, "conflicts.csv")
    conflict_df.to_csv(output_file, index=False)

    # Print a completion message
    print(f'{folder_name}/conflicts.csv created. Please inspect the file for unwanted anomalies!')
