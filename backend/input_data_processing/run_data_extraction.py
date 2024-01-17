import os
import sys
from dotenv import load_dotenv
import requests
import pandas as pd
from io import StringIO
from datetime import datetime, timedelta
from extract_population import extract_population_info_from_web
from extract_locations_csv import extract_locations_csv
from extract_conflict_info import extract_conflict_info
from extract_conflicts_csv import extract_conflicts_csv
from extract_routes_csv import extract_routes_csv
from add_camp_locations import add_camp_locations
from create_closures_csv import create_empty_closure_csv
from create_registration_corrections_csv import create_empty_registration_corrections_csv
from create_sim_period_csv import create_sim_period_csv
from file_converter import insert_data_into_DB
from create_validation_data import create_validation_data
from helper_functions import date_format
from pathlib import Path


# global variables (default values mostly from FLEE)
POPULATION_THRESHOLD = 10000
FATALITIES_THRESHOLD = 0
CONFLICT_THRESHOLD = 100
LOCATION_TYPE = 'location'
ADDED_CONFLICT_DAYS = 7
NBR_SHOWN_ROWS = 10


def acled_data_to_csv(country, folder_name, start_date, fetching_end_date):
    '''
    Extracts the ACLED data for the given country and time period and saves it to a CSV file.

        Parameters:
            country (str): Country name
            folder_name (str): Folder name for the CSV file
            start_date (str): Start date of the time period
            fetching_end_date (str): End date of the time period for fetching data
        Returns:
            acled_url (str): URL of the ACLED data source
            retrieval_date (str): Date of retrieval. When the script is executed.
            last_update (str): Date of the last update of the ACLED data
            reformatted_start_date (str): Start date of the time period in the format YYYY-MM-DD
            reformatted_end_date (str): End date of the time period in the format YYYY-MM-DD
            oldest_event_date (str): Oldest event date of the ACLED data in the format YYYY-MM-DD
            latest_event_date (str): Most recent event date of the ACLED data in the format YYYY-MM-DD
    '''


    # date of retrieval, which is the date when the script is executed. Format: YYYY-MM-DD HH:MM:SS
    retrieval_date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    
    # reformat the given date from DD-MM-YYYY to YYYY-MM-DD in order to have the same format as in the ACLED-API
    reformatted_start_date = date_format(start_date)
    reformatted_end_date = date_format(fetching_end_date)

    # extract start_year and end_year for API call
    split_start_date = start_date.split("-")
    split_end_date = fetching_end_date.split("-")
    start_year = int(split_start_date[2])
    end_year = int(split_end_date[2])


    # get the API key and email from the environment variables
    load_dotenv()
    ACLED_API_KEY = os.environ.get('ACLED_API_KEY')
    ACLED_API_MAIL = os.environ.get('ACLED_API_MAIL')

    # e.g. start_year = 2021, end_year = 2023 -> years = '2021|2022|2023'
    if start_year < end_year:
        years = '|'.join([str(year) for year in range(start_year, end_year + 1)])
    else:
        years = str(start_year)

    # API endpoint URL
    url_json = 'https://api.acleddata.com/acled/read'

    # parameters for the API call. Used these parameter values based on flee.readthedocs
    params = {
    'key': ACLED_API_KEY,
    'email': ACLED_API_MAIL,
    'country': country,
    'year': years,
    'event_type': 'Battle',
    'sub_event_type': 'Armed clash|Attack|Government regains territory|Non-state actor overtakes territory',
    'field': 'event_id_cnty|event_date|year|event_type|country|admin1|admin2|location|latitude|longitude|timestamp'
    }

    # Make the GET request
    response = requests.get(url_json, params=params)

    if response.status_code == 200:
        # convert response to json
        response = response.json()

        # last_update is the number of hours since the last update to the data
        acled_last_update = response['last_update']

        # Subtract acled_last_update from current time
        last_update_datetime = datetime.now() - timedelta(hours=acled_last_update)

        # Format in YYYY_MM_DD HH:MM:SS
        last_update_str = last_update_datetime.strftime('%Y-%m-%d %H:%M:%S')

        # number of events in the response
        number_of_events = response['count']

        # extract the acled data with the events
        acled_data = response['data']

        # convert to dataframe
        acled_df = pd.DataFrame(acled_data)

        # filter the data by start&end date and reset index
        acled_df = acled_df[(acled_df['event_date'] >= reformatted_start_date) & (acled_df['event_date'] <= reformatted_end_date)]
        acled_df = acled_df.reset_index(drop=True)

        # extract latest event date (this is not always the same as the fetching_end_date). We want to store the event date in the DB
        # the extracted format of the date is 'YYYY-MM-DD' - we also want to store it in this format 
        # from API doc: ACLED data is returned in date order DESC (starting with the latest). 
        # get latest entry for event_date 
        latest_event_date = acled_df['event_date'][0]

        # get oldest event_date
        oldest_event_date = acled_df['event_date'].iloc[-1]
        
        # url we want to show in the frontend as source and store in DB
        acled_url = 'https://acleddata.com/data-export-tool/'
        
        # store in folder_name as CSV file
        acled_df.to_csv(os.path.join(folder_name, 'acled.csv'), index=False)
    else: 
        print(f"Error: Could not retrieve data from ACLED API. Status code: {response.status_code}")
        acled_url = ""
        acled_last_update = ""
        last_update_str = ""
        oldest_event_date = ""
        latest_event_date = ""
    
    # return the data source and date information
    return acled_url, retrieval_date, last_update_str, reformatted_start_date, reformatted_end_date, oldest_event_date, latest_event_date


def run_extraction(country_name, start_date, fetching_end_date, simulation_end_date, round_data):
    '''
    Runs the data extraction process for the given country and time period.
            Parameters:
                country_name (str): Country name
                start_date (str): Start date of the time period
                fetching_end_date (str): End date of the time period for fetching data
                simulation_end_date (str): (Maximum) end date of the simulation
                round_data (list): List of dictionaries with the round number, the source and the covered time period
    '''
    print(100*"-")
    print("Extract the information for:")
    print(f"Country: {country_name}")
    print(f"Start date: {start_date}")
    print(f"Fetching end date: {fetching_end_date}")
    print(f"Simulation end_date: {simulation_end_date}")
    print(f"Round data: {round_data}")
    print(100*"-")

    # check invalid dates
    if date_format(start_date) > date_format(fetching_end_date):
        print("Error: Start date is after fetching end date.")
        return
    elif date_format(start_date) > date_format(simulation_end_date):
        print("Error: Start date is after simulation end date.")
        return
    
    start_year = int(start_date.split('-')[2])
    end_year = int(fetching_end_date.split('-')[2])

    # 1. create folder for country with start_year and time (for uniqueness)
    folder_name = country_name.lower() + str(start_year) + "_" + datetime.today().strftime('%Y-%m-%d_%H-%M-%S')
    os.mkdir(folder_name)
    
    # 2. get acled data and create acled.csv
    acled_url, acled_retrieval_date, acled_last_update, acled_reformatted_start_date, acled_reformatted_end_date, acled_oldest_event_date, acled_latest_event_date = acled_data_to_csv(country_name, folder_name, start_date, fetching_end_date)

    # 3. get population data and create population.csv.  population date in format YYYY-MM-DD
    population_url, population_retrieval_date, population_date = extract_population_info_from_web(country_name, folder_name, POPULATION_THRESHOLD) 
    
    # 4. extract location data and create locations.csv
    extract_locations_csv(folder_name, start_date, LOCATION_TYPE, FATALITIES_THRESHOLD, CONFLICT_THRESHOLD, NBR_SHOWN_ROWS)
    
    # 5. add camps to locations.csv 
    camp_data_df, camp_rounds_dict, camps_last_update_url, camps_retrieval_date, camps_last_update, camps_reformatted_start_date, camps_reformatted_end_date, camps_latest_survey_date = add_camp_locations(round_data, folder_name, NBR_SHOWN_ROWS, start_date, fetching_end_date)

    # 6. extract conflict data and create conflict_info.csv
    extract_conflict_info(country_name, folder_name, start_date, simulation_end_date, LOCATION_TYPE, ADDED_CONFLICT_DAYS)

    # 7. extract conflict information from conflict_info.csv, modify data and create conflict.csv
    extract_conflicts_csv(folder_name, start_date, simulation_end_date)

    # 8. extract routes from locations.csv and create routes.csv
    extract_routes_csv(folder_name)
    
    # 9. create empty closures.csv
    create_empty_closure_csv(folder_name)
    
    # 10. create empty registration_correction.csv
    create_empty_registration_corrections_csv(folder_name)
    
    # 11. create sim_period.csv
    create_sim_period_csv(folder_name, start_date, fetching_end_date)

    # 12. create validation data
    # create folder in conflict_validation 
    # docker path
    # os.mkdir(os.path.join('conflict_validation', folder_name))
    current_dir = os.getcwd()
    validation_folder_path = os.path.join(current_dir, "input_data_processing", 'conflict_validation', folder_name)
    os.mkdir(validation_folder_path)

    # create validation csv files
    val_retrieval_date, val_reformatted_start_date, val_reformatted_end_date, val_covered_from, val_covered_to, val_oldest_url, val_latest_url = create_validation_data(camp_data_df, camp_rounds_dict, folder_name, country_name, start_date, fetching_end_date)


    # 13. insert data into DB
    current_dir = os.getcwd()
    acled_source_list=[acled_url, acled_retrieval_date, acled_last_update, acled_reformatted_start_date, acled_reformatted_end_date, acled_oldest_event_date, acled_latest_event_date]
    population_source_list = [population_url, population_retrieval_date, population_date]
    camp_source_list = [camps_last_update_url, camps_retrieval_date, camps_last_update, camps_reformatted_start_date, camps_reformatted_end_date, camps_latest_survey_date]
    validation_source_list = [val_retrieval_date, val_reformatted_start_date, val_reformatted_end_date, val_covered_from, val_covered_to, val_oldest_url, val_latest_url]

    insert_data_into_DB(country_name, current_dir, folder_name, acled_source_list, population_source_list, camp_source_list, validation_source_list)
    

# variables that can be passed as parameters
# date format: dd-mm-yyyy

country_name = "Ethiopia"
start_date = "01-01-2023" # start date for the data fetching
fetching_end_date =  "17-01-2024" # end date for the data fetching
simulation_end_date = "31-12-2024" # this is the furthest date that can be used for the simulation

# according to flee, date must have the format "yyyy-mm-dd"
# this is necessary for the validation data.
# this data is manually added for now because of the inconsistent format of the data
# according to Diana from the development team of FLEE, the last 3 rounds are enough 
round_data = [
{"round": 32, "source": "https://dtm.iom.int/datasets/ethiopia-site-assessment-round-32", "covered_from": "2022-11-25", "covered_to": "2023-01-09"},
{"round": 33, "source": "https://dtm.iom.int/datasets/ethiopia-site-assessment-round-33", "covered_from": "2023-06-11", "covered_to": "2023-06-29"},
{"round": 34, "source": "https://dtm.iom.int/datasets/ethiopia-site-assessment-round-34", "covered_from": "2023-08-01", "covered_to": "2023-09-02"},
]

# take args & check if they are set
if len(sys.argv) < 5:
    print("Not enough arguments provided. Please provide the following arguments: country_name, start_date, end_date, simulation_end_date")
    print(f"The default parameters were taken instead: country_name = {country_name}, start_date = {start_date}, fetching end_date = {fetching_end_date}, simulation_end_date = {simulation_end_date}")
else: 
    country_name = sys.argv[1]
    start_date = sys.argv[2]
    fetching_end_date = sys.argv[3]
    simulation_end_date = sys.argv[4]

# start the script
run_extraction(country_name, start_date, fetching_end_date, simulation_end_date, round_data)