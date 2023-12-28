# This script is based on https://github.com/djgroen/FabFlee/blob/master/scripts/03_extract_conflict_info.py 
# but changed where necessary to work automatically with the data from the ACLED API and the population data

'''
Input: ACLED data (acled.csv)
Output: Conflict information data (conflict_info.csv)

Description:
This script processes ACLED conflict data for a specified country and extracts information about conflict periods and their estimated durations for different locations. It calculates the conflict period for each location based on the provided start date, and it adds an estimated conflict duration based on the number of added conflict days.

Usage:
1. Prepare ACLED conflict data for the desired country and save it as a CSV file (acled.csv).
2. Ensure the ACLED data includes columns for "event_date," "country," and the relevant location type (e.g., "admin2").
3. Specify the desired parameters:
    - <country>: Name of the country or dataset (e.g., nigeria2016).
    - <start_date>: The starting date to consider when calculating conflict periods (e.g., "01-01-2016").
    - <end_date>: The end date to consider when calculating conflict periods (e.g., "31-12-2016").
    - <location_type>: The type of location to focus on (e.g., "admin2" for administrative region level 2).
    - <added_conflict_days>: The number of days to add to the calculated conflict periods for estimating event periods.
'''

import os
from datetime import datetime
import pandas as pd
import pprint

pp = pprint.PrettyPrinter(indent=4)

# Function to format a date string into "dd-mm-yyyy" format
def date_format(in_date):
    if "-" in in_date:
        split_date = in_date.split("-")
    else:
        split_date = in_date.split(" ")

    out_date = str(split_date[2]) + "-" + str(split_date[1]) + "-" + str(split_date[0])

    return out_date


# Function to convert month names to month numbers
def month_convert(month_name):
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


# Function to calculate the number of days between two dates in "dd-mm-yyyy" format
def between_date(d1, d2):
    d1list = d1.split("-")
    d2list = d2.split("-")
    date1 = datetime(int(d1list[2]), int(d1list[1]), int(d1list[0]))
    date2 = datetime(int(d2list[2]), int(d2list[1]), int(d2list[0]))

    return abs((date1 - date2).days)


def extract_conflict_info(country, folder_name, start_date, end_date, location_type, added_conflict_days):
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
        if len(unique_event_dates) > 0:
            print(f"Location: {name}, Event Dates: ", end='')
            pp.pprint(unique_event_dates)
    print("")

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

    for name, group in grouped:
        event_dates = group['event_date'].tolist()
        event_count = len(event_dates)
        formatted_dates = [date_format(date) for date in event_dates]

        if event_count == 1:
            # For locations with one event date
            conflict_date = [between_date(formatted_dates[0], end_date)]
            modified_conflict_date = conflict_date[0] + int(added_conflict_days)

        elif event_count == 2:
            # For locations with two event dates
            conflict_date = [between_date(formatted_dates[0], end_date)]
            modified_conflict_date = conflict_date[0] + int(added_conflict_days)

        else:
            # For locations with more than two event dates
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

    print(results_df.to_string(index=False))

    # Write the results dataframe to a CSV file
    output_file = os.path.join(current_dir, folder_name, "conflict_info.csv")
    results_df.to_csv(output_file, index=False)

    # Print a completion message
    print(f'{folder_name}/conflict_info.csv created. Please inspect the file for unwanted anomalies!')
