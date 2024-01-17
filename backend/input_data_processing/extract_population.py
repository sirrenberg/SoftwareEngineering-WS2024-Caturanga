import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime


def extract_population_info_from_web(country, folder_name, threshold):
    """
    Extracts population information from citypopulation.de
        Parameters:
            country (str): Name of the country
            folder_name (str): Name of the folder where the file will be saved
            threshold (int): The minimum population threshold
        Returns
            url (str): URL of the data source
            retrieval_date (str): Date of retrieval
            latest_date (str): Latest date of the data source
    """
    # date of retrieval, which is the date when the script is executed. Format: YYYY-MM-DD HH:MM:SS
    retrieval_date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

    city_data = {}

    # URL to scrape for ethiopia
    # The population of all Ethiopian cities and towns with more than 20,000 inhabitants according to census results and latest official projections.
    country = country.lower()
    url = f"https://www.citypopulation.de/en/{country}/cities/"
    latest_date = ""

    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        city_section = soup.find('section', {'id': 'citysection'})

        if city_section:
            city_table = city_section.find('table', {'id': 'ts'})

            if city_table:
                # Extract information from the table
                header_row = city_table.find('tr', {'id': 'tsh'})
                if header_row:
                    # Find the header cell containing the latest date
                    latest_date_cell = header_row.find('th', {'class': 'rpop prio1'})
                    if latest_date_cell:
                        # the format is YYYY-MM-DD
                        latest_date = latest_date_cell['data-coldate']
                # find all rows in the table
                for row in city_table.find_all('tr'):
                    columns = row.find_all(['td', 'th'])
                    # Check if it's a data row
                    if columns and 'itemscope' in row.attrs:
                        city_name = columns[1].find('span', {'itemprop': 'name'}).text.strip()
                        adm = columns[2].text.strip()
                        population_latest = row.find('td', {'class': 'rpop prio1'}).text.strip()
                        # string to int
                        population_latest = population_latest.replace(',', '')
                        population_latest = int(population_latest)

                        # just add city if population is greater than threshold
                        if population_latest >= threshold:
                            # Store information in the dictionary
                            city_data[city_name] = {
                                'Latest Population': population_latest
                            }
            else:
                print("Table with id='ts' not found.")
        else:
            print("Section with id='citysection' not found.")
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")

    # create a csv in folder_name with the following structure: name, population
    with open(f'{folder_name}/population.csv', 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['name', 'population'])
        for key, value in city_data.items():
            writer.writerow([key, value['Latest Population']])
    
    return url, retrieval_date, latest_date



