# This script is based on https://github.com/djgroen/FabFlee/blob/master/scripts/03_extract_conflict_info.py 
# but changed where necessary to work automatically with the data from the ACLED API and the population data
import os
from datetime import datetime
import pandas as pd
import pprint
from helper_functions import date_format, between_date

pp = pprint.PrettyPrinter(indent=4)


def month_convert(month_name):
    '''
    Function to convert month names to month numbers.
        Parameters:
            month_name (str): Name of the month
        Returns:
            (str): Number of the month
    '''
    months = {
        "jan": "01", "january": "01",
        "feb": "02", "february": "02",
        "mar": "03", "march": "03",
        "apr": "04", "april": "04",
        "may": "05", "may": "05",
        "jun": "06", "june": "06",
        "jul": "07", "july": "07",
        "aug": "08", "august": "08",
        "sep": "09", "september": "09",
        "oct": "10", "october": "10",
        "nov": "11", "november": "11",
        "dec": "12", "december": "12"
    }

    # Convert the month name to lowercase and strip leading/trailing whitespace
    month_name = month_name.strip().lower()

    # Look up the month number in the dictionary
    if month_name in months:
        month_num = months[month_name]
    else:
        print("Invalid month name entered.")

    return month_num



def extract_conflict_info(country, folder_name, start_date, end_date, location_type, added_conflict_days):
    '''
    Extract conflict information from ACLED data and write it to a CSV file.
    The function calculates the conflict period for each location based on the provided start date, and it adds an estimated conflict duration based on the number of added conflict days.

        Parameters:
            country (str): Name of the country or dataset
            folder_name (str): Name of the folder containing the CSV files
            start_date (str): The starting date to consider when calculating conflict periods
            end_date (str): The end date to consider when calculating conflict periods
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
    conflict_date = [between_date(d, start_date) for d in formatted_event_dates]
    acled_df['conflict_date'] = conflict_date

    # Group the locations by admin-level
    grouped = acled_df.groupby(location_type)


    # Print groups that differ only in event_date
    for name, group in grouped:
        unique_event_dates = group['event_date'].unique()
        '''
        if len(unique_event_dates) > 0:
            print(f"Location: {name}, Event Dates: ", end='')
            pp.pprint(unique_event_dates)
        '''
    # print("")

    # Create a new DataFrame to store the results
    results_df = pd.DataFrame(columns=
                              ["name",
                               "country",
                               "event_count",
                               "start_date",
                               "end_date",
                               "conflict_date",
                               "modified_conflict_date"]
                              )

    # Iterate through the grouped locations and calculate the conflict period for each location
    for name, group in grouped:
        event_dates = group['event_date'].tolist()
        event_count = len(event_dates)
        formatted_dates = [date_format(date) for date in event_dates]

        conflict_date = [between_date(formatted_dates[0], end_date)]
        modified_conflict_date = conflict_date[0] + int(added_conflict_days)


        results_df.loc[len(results_df)] = {
            "name": name,
            "country": country,
            "start_date": formatted_dates[0],
            "end_date": end_date,
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
