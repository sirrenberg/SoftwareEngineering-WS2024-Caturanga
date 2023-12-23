import requests
from bs4 import BeautifulSoup

def extract_population_info(country):
    """
    Extracts population information from citypopulation.de
    :param country: country name
    :return: A dictionary containing city information
    """
    city_data = {}

    # URL to scrape for ethiopia
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
