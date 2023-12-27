# This script is based on https://github.com/djgroen/FabFlee/blob/master/scripts/02_extract_locations_csv.py 
# but changed where necessary to work automatically with the data from the ACLED API and the population data

'''
Input: ACLED data (acled.csv) & Population data (population.csv)
Output: Location data (locations.csv)

Description:
This script processes ACLED conflict data for a specified country and extracts location-based information such as town or administrative region names, their populations, and other relevant data. It then classifies locations into "towns" and "conflict zones" based on predefined conflict thresholds and combines this information with population data obtained separately.

Usage:
1. Prepare ACLED conflict data for the desired country and save it as a CSV file (acled.csv).
2. Ensure the ACLED data includes columns for "event_date," "country," "admin1" (administrative region level 1), "admin2" (administrative region level 2), "location," "latitude," "longitude," and "fatalities."
3. Specify the desired parameters:
    - <country>: Name of the country or dataset (e.g., nigeria2016).
    - <start_date>: The starting date to consider when calculating conflict periods (e.g., "01-01-2016").
    - <location_type>: The type of location to focus on (e.g., "admin2" for administrative region level 2).
    - <fatalities_threshold>: Minimum fatalities count for including a location.
    - <conflict_threshold>: Conflict period threshold for classifying locations.
'''

import os
from datetime import datetime
import numpy as np
import pandas as pd


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


# Function to drop rows in a DataFrame based on a condition
def drop_rows(inputdata, columnname, dropparameter):
    removedrows = inputdata.index[inputdata[columnname] <= dropparameter].tolist()
    outputdata = inputdata.drop(removedrows)

    return outputdata


# Function to filter a DataFrame by location based on column name
def filter_by_location(inputdata, columnname):
    if columnname == "admin1":
        location_list = inputdata.admin1.unique()
    elif columnname == "admin2":
        location_list = inputdata.admin2.unique()
    elif columnname == "location":
        location_list = inputdata.location.unique()
    else:
        print("Invalid location type!")

    outputdata = pd.DataFrame()
    for loc in location_list:
        # keep admin 1 as they are 
        tempdf = inputdata.loc[inputdata[columnname] == loc]
        tempdf.sort_values(columnname, ascending=True)
        outputdata = pd.concat([outputdata, tempdf.tail(1)])

    outputdata = outputdata[['event_date', 'country', columnname, 'admin1', 'latitude', 'longitude', 'fatalities', 'conflict_period']]

    return outputdata


# Main function to extract and process location data
def extract_locations_csv(country, folder_name, start_date, location_type, fatalities_threshold, conflict_threshold):
    # Get the current directory
    current_dir = os.getcwd()

    print(folder_name)
    print(current_dir)

    # Load the ACLED data from acled.csv into a DataFrame
    acled_file = os.path.join(current_dir, folder_name, "acled.csv")
    acled_df = pd.read_csv(acled_file)

    # Load the population data from population.csv into a DataFrame
    population_input_file = os.path.join(current_dir, folder_name, "population.csv")
    population_df = pd.read_csv(population_input_file)

    # Create a dictionary mapping location names to their populations from the population DataFrame
    population_dict = {row['name']: row['population'] for index, row in population_df.iterrows()}

    # Extract unique location names from population.csv and acled.csv
    population_locations = set(population_df['name'])
    acled_location_types = set(acled_df[location_type])

    # Check if there are any matching locations between the two datasets
    matching_population = population_locations.intersection(acled_location_types)

    # Create a list of locations without population data
    locations_without_population = list(acled_location_types - matching_population)

    # Print messages based on the results of the matching locations
    if matching_population:
        print("We found population data for all ACLED locations.")
    else:
        print("We did not find population data for all ACLED locations.")

        if locations_without_population:
            print("These locations without populations:")
            for location in locations_without_population:
                print(f"- {location}")

            print("Please refer to extract_population.py to select different population-table from population.html!")

    # Extract relevant columns from the ACLED DataFrame
    acled_df = acled_df[["event_date", "country", "admin1", "admin2", "location", "latitude", "longitude", "fatalities"]]

    # Process event dates and calculate conflict periods
    event_dates = acled_df["event_date"].tolist()
    formatted_event_dates = [date_format(date) for date in event_dates]
    conflict_period = [between_date(d, start_date) for d in formatted_event_dates]
    acled_df['conflict_period'] = conflict_period


    # Filter ACLED data based on location type, fatalities threshold, and sort by conflict period
    acled_df = filter_by_location(acled_df, location_type)
    acled_df = acled_df.loc[acled_df['fatalities'] > fatalities_threshold]
    acled_df = acled_df.sort_values('conflict_period')
    
    # Split ACLED data into towns and conflict zones
    towns_df = acled_df[acled_df['conflict_period'] <= conflict_threshold].copy()
    conflict_zones_df = acled_df[acled_df['conflict_period'] > conflict_threshold].copy()

    # Add location type labels to the dataframes
    towns_df['location_type'] = 'town'
    conflict_zones_df['location_type'] = 'conflict_zone'

    # Concatenate the dataframes for towns and conflict zones
    merged_df = pd.concat([towns_df, conflict_zones_df])

    # Retrieve and add population information to the merged dataframe
    merged_df['population'] = [population_dict.get(name, 0) for name in merged_df[location_type]]
    merged_df['population'] = merged_df['population'].replace([np.inf, -np.inf, np.nan], 0)
    merged_df['population'] = merged_df['population'].astype(int)

    # Select and rename columns for the final output
    # show index of merged_df
    merged_df = merged_df[[location_type, 'admin1', 'country', 'latitude', 'longitude', 'location_type', 'conflict_period', 'population']]
    merged_df.columns = ['#name', 'region', 'country',  'latitude', 'longitude', 'location_type', 'conflict_period', 'population']

    # Write the merged dataframe to a CSV file
    output_file = os.path.join(current_dir, folder_name, "locations.csv")
    merged_df.to_csv(output_file, index=False)

    # Print the merged dataframe and a completion message
    print(merged_df.to_string(index=0))
    print(f'{folder_name}/locations.csv created. Please add refugee camps to the locations,csv file.')
