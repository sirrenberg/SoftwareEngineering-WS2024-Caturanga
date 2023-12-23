import requests
from bs4 import BeautifulSoup
import requests
from dotenv import load_dotenv
import os


def get_acled_data(country, start_year, end_year):
    """
    Retrieve ACLED data from the API.
    """

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
    url = 'https://api.acleddata.com/acled/read'

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
    response = requests.get(url, params=params)
    if response.status_code == 200:
        # Parse JSON data
        json_data = response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
    
    return json_data


def extract_locations_from_acled_data(acled_data_json):
    """
    Extracts location information from ACLED data.
    :param acled_data_json: ACLED data in JSON format
    :return: A list of lists containing location information
    """
    data_entries = acled_data_json.get('data', [])

    locations = []

    for element in data_entries:
        location_entry = []
        location_entry.append(element['location'])
        location_entry.append(element['admin1'])
        location_entry.append(element['admin2'])
        location_entry.append(element['country'])
        location_entry.append(element['latitude'])
        location_entry.append(element['longitude'])

        # each entry has the following format: [location, admin1, admin2, country, latitude, longitude]
        locations.append(location_entry)
    
    return locations


def extract_population_info_from_web(country):
    """
    Extracts population information from citypopulation.de
    :param country: country name
    :return: A dictionary containing city information
    """
    city_data = {}

    # URL to scrape for ethiopia
    # The population of all Ethiopian cities and towns with more than 20,000 inhabitants according to census results and latest official projections.
    country = country.lower()
    url = f"https://www.citypopulation.de/en/{country}/cities/"

    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        city_section = soup.find('section', {'id': 'citysection'})

        if city_section:
            city_table = city_section.find('table', {'id': 'ts'})

            if city_table:
                # Extract information from the table
                # Find all 'td' tags

                for row in city_table.find_all('tr'):
                    columns = row.find_all(['td', 'th'])

                    # Check if it's a data row
                    if columns and 'itemscope' in row.attrs:
                        city_name = columns[1].find('span', {'itemprop': 'name'}).text.strip()
                        adm = columns[2].text.strip()
                        population_latest = row.find('td', {'class': 'rpop prio1'}).text.strip()

                        # Store information in the dictionary
                        city_data[city_name] = {
                            'Latest Population': population_latest
                        }

                        print(f"City: {city_name}, Adm: {adm}, Latest Population: {population_latest}")

            else:
                print("Table with id='ts' not found.")
        else:
            print("Section with id='citysection' not found.")
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")

    return city_data



def run_extraction():
    country_name = 'Ethiopia'
    start_year = 2021
    end_year = 2023

    # get conflict data
    acled_data_json = get_acled_data(country_name, start_year, end_year)

    # extract location information from acled data
    conflict_locations = extract_locations_from_acled_data(acled_data_json)
    print(conflict_locations)


    # get population information
    '''
    population_info = extract_population_info_from_web(country_name)

    if population_info:
        for city, population in population_info.items():
            print(f"City: {city}, Latest Population: {population['Latest Population']}")
    '''
    

run_extraction()
    


