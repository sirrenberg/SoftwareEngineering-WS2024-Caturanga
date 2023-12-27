import os
from dotenv import load_dotenv
import requests
import pandas as pd
from io import StringIO
from extract_population import extract_population_info_from_web
from extract_locations_csv import extract_locations_csv
from extract_conflict_info import extract_conflict_info
from extract_conflicts_csv import extract_conflicts_csv
from extract_routes_csv import extract_routes_csv
from add_camp_locations import add_camp_locations
from create_closures_csv import create_empty_closure_csv
from create_registration_corrections_csv import create_empty_registration_corrections_csv
from create_sim_period_csv import create_sim_period_csv



# global variables (default values)
POPULATION_THRESHOLD = 10000
FATALITIES_THRESHOLD = 0
CONFLICT_THRESHOLD = 100
LOCATION_TYPE = 'location'
ADDED_CONFLICT_DAYS = 7



def acled_data_to_csv(country, folder_name, start_year, end_year):
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
    url_csv = 'https://api.acleddata.com/acled/read.csv'

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
    response = requests.get(url_csv, params=params)

    # Convert the response text to a CSV
    data = pd.read_csv(StringIO(response.text))
    # Save the data to a CSV file

    # store in folder_name
    data.to_csv(os.path.join(folder_name, 'acled.csv'), index=False)



def run_extraction(country_name, start_year, end_year):
    # TODO: start&end date adjustable to the day. Right now the simulation only starts at the beginning of a year and ends at the end of a year. Change if necessary

    start_date = '01-01-' + str(start_year)
    end_date = '31-12-' + str(end_year)

    # 1. create folder for country with start_year
    folder_name = country_name.lower() + str(start_year)
    os.mkdir(folder_name)

    # 2. get acled data and create acled.csv
    acled_data_to_csv(country_name, folder_name, start_year, end_year)

    # 3. get population data and create population.csv
    extract_population_info_from_web(country_name, folder_name, POPULATION_THRESHOLD)

    # 4. extract location data and create locations.csv
    extract_locations_csv(country_name, folder_name, start_date, LOCATION_TYPE, FATALITIES_THRESHOLD, CONFLICT_THRESHOLD)

    # 5. extract conflict data and create conflict_info.csv
    extract_conflict_info(country_name, folder_name, start_date, end_date, LOCATION_TYPE, ADDED_CONFLICT_DAYS)

    # 6. extract conflict information from conflict_info.csv, modify data and create conflict.csv
    extract_conflicts_csv(country_name, folder_name, start_date, end_date)

    # 7. add camps to locations.csv
    # Caution: This has to be done manually. 
    # Data for Ethiopia is available here: https://data.unhcr.org/en/documents/details/101743
    add_camp_locations(folder_name)

    # 8. extract routes from locations.csv and create routes.csv
    extract_routes_csv(country_name, folder_name)
    
    # 9. create empty closures.csv
    create_empty_closure_csv(folder_name)
    
    # 10. create empty registration_correction.csv
    create_empty_registration_corrections_csv(folder_name)
    
    # 11. create sim_period.csv
    create_sim_period_csv(folder_name, start_date, end_date)
    




# variables that can be changed
country_name = 'Ethiopia'
start_year = 2023
end_year = 2023


run_extraction(country_name, start_year, end_year)





    