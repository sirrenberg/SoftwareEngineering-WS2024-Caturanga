import os
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
from create_validation_data import create_refugee_csv


# global variables (default values)
POPULATION_THRESHOLD = 10000
FATALITIES_THRESHOLD = 0
CONFLICT_THRESHOLD = 100
LOCATION_TYPE = 'location'
ADDED_CONFLICT_DAYS = 7
NBR_SHOWN_ROWS = 10



def acled_data_to_csv(country, folder_name, start_date, end_date):
    '''
    Extracts the ACLED data for the given country and time period and saves it to a CSV file.

        Parameters:
            country (str): Country name
            folder_name (str): Folder name for the CSV file
            start_year (int): Start year of the time period
            end_year (int): End year of the time period	
        Returns:
            acled_url (str): URL of the ACLED data source
            retrieval_date (str): Date of retrieval
            last_update (str): Date of the last update of the ACLED data
            reformatted_start_date (str): Start date of the time period in the format YYYY-MM-DD
            reformatted_end_date (str): End date of the time period in the format YYYY-MM-DD
            oldest_event_date (str): Oldest event date of the ACLED data in the format YYYY-MM-DD
            latest_event_date (str): Latest event date of the ACLED data in the format YYYY-MM-DD
    '''

    # date of retrieval, which is the date when the script is executed. Format: YYYY-MM-DD HH:MM:SS
    retrieval_date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    
    # reformat the given date from DD-MM-YYYY to YYYY-MM-DD in order to have the same format as in the ACLED-API
    split_start_date = start_date.split("-")
    split_end_date = end_date.split("-")
    reformatted_start_date = str(split_start_date[2]) + "-" + str(split_start_date[1]) + "-" + str(split_start_date[0])
    reformatted_end_date = str(split_end_date[2]) + "-" + str(split_end_date[1]) + "-" + str(split_end_date[0])

    # extract start_year and end_year
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

    # parameters for the API call
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

    # extract latest event date (this is not always the same as the end_date). We want to store the event date in the DB
    # the extracted format of the date is 'YYYY-MM-DD' - we also want to store it in this format 
    # from API doc: ACLED data is returned in date order DESC (starting with the latest). 
    # get latest entry for event_date 
    latest_event_date = acled_df['event_date'][0]

    # get oldest event_date
    oldest_event_date = acled_df['event_date'].iloc[-1]
    
    # url we want to show in the frontend and store in DB
    acled_url = 'https://acleddata.com/data-export-tool/'
    
    # store in folder_name as CSV file
    acled_df.to_csv(os.path.join(folder_name, 'acled.csv'), index=False)
    
    # return the data source and date information
    return acled_url, retrieval_date, last_update_str, reformatted_start_date, reformatted_end_date, oldest_event_date, latest_event_date


def run_extraction(country_name, start_date, end_date):
    '''
    Runs the data extraction process for the given country and time period.
    
            Parameters:
                country_name (str): Country name
                start_date (str): Start date of the time period
                end_date (str): End date of the time period
    '''
    start_year = int(start_date.split('-')[2])
    end_year = int(end_date.split('-')[2])

    # 1. create folder for country with start_year and time (for uniqueness)
    folder_name = country_name.lower() + str(start_year) + "_" + datetime.today().strftime('%Y-%m-%d_%H-%M-%S')
    os.mkdir(folder_name)
    
    # 2. get acled data and create acled.csv
    acled_url, acled_retrieval_date, acled_last_update, acled_reformatted_start_date, acled_reformatted_end_date, acled_oldest_event_date, acled_latest_event_date = acled_data_to_csv(country_name, folder_name, start_date, end_date)


    # 3. get population data and create population.csv.  population date in format YYYY-MM-DD
    population_url, population_retrieval_date, population_date = extract_population_info_from_web(country_name, folder_name, POPULATION_THRESHOLD) 
    
    # 4. extract location data and create locations.csv
    # TODO: check how the code (from FabFlee) handels the fact that locations can appear multiple times in the ACLED data
    extract_locations_csv(folder_name, start_date, LOCATION_TYPE, FATALITIES_THRESHOLD, CONFLICT_THRESHOLD, NBR_SHOWN_ROWS)

    # 5. add camps to locations.csv
    # Caution: This has to be done manually. 
    # Data for Ethiopia is available here: https://data.unhcr.org/en/documents/details/101743
    add_camp_locations(folder_name)

    # 6. extract conflict data and create conflict_info.csv
    extract_conflict_info(country_name, folder_name, start_date, end_date, LOCATION_TYPE, ADDED_CONFLICT_DAYS)

    # 7. extract conflict information from conflict_info.csv, modify data and create conflict.csv
    extract_conflicts_csv(folder_name, start_date, end_date)

    # 8. add camps to locations.csv
    # Caution: This has to be done manually. 
    # Data for Ethiopia is available here: https://data.unhcr.org/en/documents/details/101743
    add_camp_locations(folder_name)

    # 9. extract routes from locations.csv and create routes.csv
    extract_routes_csv(folder_name)
    
    # 10. create empty closures.csv
    create_empty_closure_csv(folder_name)
    
    # 11. create empty registration_correction.csv
    create_empty_registration_corrections_csv(folder_name)
    
    # 12. create sim_period.csv
    create_sim_period_csv(folder_name, start_date, end_date)
    
    # 13. insert data into DB
    current_dir = os.getcwd()
    folder_path = os.path.join(current_dir, folder_name)
    
    acled_source_list=[acled_url, acled_retrieval_date, acled_last_update, acled_reformatted_start_date, acled_reformatted_end_date, acled_oldest_event_date, acled_latest_event_date]
    population_source_list = [population_url, population_retrieval_date, population_date]

    insert_data_into_DB([country_name], folder_path, acled_source_list, population_source_list)
    
    
    # 14. create validation data
    # create folder in conflict_validation
    # TODO: error handling if folder already exists
    os.mkdir(os.path.join('conflict_validation', folder_name))
    
    # create refugee.csv
    val_retrieval_date, val_reformatted_start_date, val_reformatted_end_date, val_oldest_date, val_latest_date = create_refugee_csv(folder_name, start_date, end_date)
    # this could also be stored in the database in the future, when the validation data is stored


# variables that can be changed
# date format: dd-mm-yyyy
country_name = "Ethiopia"
start_date = "01-01-2023"
end_date =  "11-01-2024"


run_extraction(country_name, start_date, end_date)





    