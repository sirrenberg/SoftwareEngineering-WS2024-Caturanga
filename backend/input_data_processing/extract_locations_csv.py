# This script is based on https://github.com/djgroen/FabFlee/blob/master/scripts/02_extract_locations_csv.py 
# but changed where necessary to work automatically with the data from the ACLED API and the population data
import os
import numpy as np
import pandas as pd
from helper_functions import date_format, between_date


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



def drop_rows(input_data, column_name, drop_parameter):
    '''
    Function to drop rows in a DataFrame based on a condition
        
        Parameters: 
            input_data (DataFrame): Input DataFrame
            column_name (str): Name of the column to filter
            drop_parameter (int): Value to filter by
        Returns:
            output_data (DataFrame): Filtered DataFrame
    '''
    removedrows = input_data.index[input_data[column_name] <= drop_parameter].tolist()
    outputdata = input_data.drop(removedrows)

    return outputdata


def filter_by_location(input_data_df, column_name):
    '''
    Function to filter a DataFrame by location based on column name
        
        Parameters: 
            input_data (DataFrame): Input DataFrame
            column_name (str): Name of the column to filter
        Returns:
            output_data (DataFrame): Filtered DataFrame
    '''
    if column_name == "admin1":
        location_list = input_data_df.admin1.unique()
    elif column_name == "admin2":
        location_list = input_data_df.admin2.unique()
    elif column_name == "admin3":
        location_list = input_data_df.admin3.unique()
    elif column_name == "location":
        location_list = input_data_df.location.unique()
    else:
        print("Invalid location type!")

    outputdata = pd.DataFrame()
    for loc in location_list:
        # keep admin 1 as they are 
        tempdf = input_data_df.loc[input_data_df[column_name] == loc]
        tempdf.sort_values(column_name, ascending=True)
        outputdata = pd.concat([outputdata, tempdf.tail(1)])

    outputdata = outputdata[['event_date', 'country', column_name, 'admin1', 'latitude', 'longitude', 'fatalities', 'conflict_date']]

    return outputdata


# self-defined function to filter by population
def keep_rows_by_population(input_data_df, rows_shown):
    '''
    Function to keep rows_shown rows of the dataframe with the highest population
        
        Parameters: 
            input_data (DataFrame): Input DataFrame
            rows_shown (int): Number of rows to keep
        Returns:
            output_data (DataFrame): Filtered DataFrame
    '''

    print(input_data_df.to_string(index=0))
    # sort by population (descending)
    sorted_df = input_data_df.sort_values(by=['population'], ascending=False)
    
    # get the rows_shown number of highest population
    reduced_df = sorted_df.head(rows_shown)

    return reduced_df





def extract_locations_csv(folder_name, start_date, location_type, fatalities_threshold, conflict_threshold, rows_shown):
    '''
    Main function to extract location data from ACLED data and write it to a CSV file.
        Parameters:
            folder_name (str): Name of the folder containing the CSV files and where it will be saved
            start_date (str): The starting date to consider when calculating conflict periods
            location_type (str): The type of location to focus on
            fatalities_threshold (int): Minimum fatalities count for including a location
            conflict_threshold (int): Conflict period threshold for classifying locations
    '''
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
    acled_df = acled_df[["event_date", "country", "admin1", "admin2","admin3", "location", "latitude", "longitude", "fatalities"]]

    # Process event dates and calculate conflict periods
    event_dates = acled_df["event_date"].tolist()
    formatted_event_dates = [date_format(date) for date in event_dates]
    conflict_date = [between_date(d, start_date) for d in formatted_event_dates]
    acled_df['conflict_date'] = conflict_date


    # Filter ACLED data based on location type, fatalities threshold, and sort by conflict period
    acled_df = filter_by_location(acled_df, location_type)
    acled_df = acled_df.loc[acled_df['fatalities'] > fatalities_threshold]
    acled_df = acled_df.sort_values('conflict_date')
    
    # Split ACLED data into towns and conflict zones
    towns_df = acled_df[acled_df['conflict_date'] <= conflict_threshold].copy()
    conflict_zones_df = acled_df[acled_df['conflict_date'] > conflict_threshold].copy()

    # Add location type labels to the dataframes
    towns_df['location_type'] = 'town'
    conflict_zones_df['location_type'] = 'conflict_zone'


    # Retrieve and add population information to the towns dataframe
    towns_df['population'] = [population_dict.get(name, 0) for name in towns_df[location_type]]
    towns_df['population'] = towns_df['population'].replace([np.inf, -np.inf, np.nan], 0)
    towns_df['population'] = towns_df['population'].astype(int)

    # retrieve and add population information to the conflict zones dataframe
    conflict_zones_df['population'] = [population_dict.get(name, 0) for name in conflict_zones_df[location_type]]
    conflict_zones_df['population'] = conflict_zones_df['population'].replace([np.inf, -np.inf, np.nan], 0)
    conflict_zones_df['population'] = conflict_zones_df['population'].astype(int)

    # Select and rename columns for the final output
    towns_df = towns_df[[location_type, 'admin1', 'country', 'latitude', 'longitude', 'location_type', 'conflict_date', 'population']]
    towns_df.columns = ['#name', 'region', 'country',  'latitude', 'longitude', 'location_type', 'conflict_date', 'population']

    conflict_zones_df = conflict_zones_df[[location_type, 'admin1', 'country', 'latitude', 'longitude', 'location_type', 'conflict_date', 'population']]
    conflict_zones_df.columns = ['#name', 'region', 'country',  'latitude', 'longitude', 'location_type', 'conflict_date', 'population']


    # just take the conflict zones and townws with the highest rows_shown population
    towns_df = keep_rows_by_population(towns_df, rows_shown)
    conflict_zones_df = keep_rows_by_population(conflict_zones_df, rows_shown)
    

    # Concatenate the dataframes for towns and conflict zones
    merged_df = pd.concat([towns_df, conflict_zones_df])

    print(merged_df.to_string(index=0))

    # Write the merged dataframe to a CSV file
    output_file = os.path.join(current_dir, folder_name, "locations.csv")
    merged_df.to_csv(output_file, index=False)

    # Print the merged dataframe and a completion message
    # print(merged_df.to_string(index=0))
    print(f'{folder_name}/locations.csv created.')
