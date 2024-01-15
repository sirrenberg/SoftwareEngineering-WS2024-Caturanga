# This script is based on https://github.com/djgroen/FabFlee/blob/master/scripts/03_extract_conflict_info.py 
# but changed where necessary to work automatically with the data from the ACLED API and the population data
import os
from datetime import datetime
import pandas as pd
import pprint
from helper_functions import date_format, between_date

pp = pprint.PrettyPrinter(indent=4)


def extract_conflict_info(country, folder_name, start_date, max_simulation_end_date, location_type, added_conflict_days):
    '''
    Extract conflict information from ACLED data and write it to a CSV file.
    The function calculates the conflict period for each location based on the provided start date and the event date

        Parameters:
            country (str): Name of the country or dataset
            folder_name (str): Name of the folder containing the CSV files
            start_date (str): The starting date to consider when calculating conflict periods
            max_simulation_end_date (str): The maximum end date to consider when calculating conflict periods
            location_type (str): The type of location to focus on
            added_conflict_days (int): The number of days to add to the calculated conflict periods for estimating event periods
    '''
    # Get the current directory
    current_dir = os.getcwd()

    # Load the ACLED data from acled.csv into a DataFrame
    acled_file = os.path.join(current_dir, folder_name, "acled.csv")
    acled_df = pd.read_csv(acled_file)

    # Extract relevant columns from the ACLED DataFrame
    acled_df = acled_df[["event_date", "country", location_type]]

    # Process event dates and calculate conflict periods
    event_dates = acled_df["event_date"].tolist()
    formatted_event_dates = [date_format(date) for date in event_dates]
    # number of days between the start_date and the event_date
    conflict_date = [between_date(d, start_date) for d in formatted_event_dates]
    acled_df['conflict_date'] = conflict_date

    # Group the locations by admin-level
    # TODO: is the grouping necessary? 
    grouped = acled_df.groupby(location_type)


    # Create a new DataFrame to store the results
    results_df = pd.DataFrame(columns=
                              ["name",
                               "country",
                               "event_count",
                               "start_date",
                               "max_simulation_end_date",
                               "conflict_date",
                               "modified_conflict_date"]
                              )

    # Iterate through the grouped locations and calculate the conflict period for each location
    for name, group in grouped:
        event_dates = group['event_date'].tolist()
        event_count = len(event_dates)
        formatted_dates = [date_format(date) for date in event_dates] 

        conflict_date = [between_date(formatted_dates[0], max_simulation_end_date)]
        modified_conflict_date = conflict_date[0] + int(added_conflict_days) # add the estimated number of days to the conflict period


        results_df.loc[len(results_df)] = {
            "name": name,
            "country": country,
            "start_date": formatted_dates[0],
            "max_simulation_end_date": max_simulation_end_date,
            "event_count": event_count,
            "conflict_date": conflict_date[0],
            "modified_conflict_date": modified_conflict_date
        }

    # print(results_df.to_string(index=False))
    
    # Write the results dataframe to a CSV file
    output_file = os.path.join(current_dir, folder_name, "conflict_info.csv")
    results_df.to_csv(output_file, index=False)

    # Print a completion message
    print(f'{folder_name}/conflict_info.csv created. Please inspect the file for unwanted anomalies!')
    
