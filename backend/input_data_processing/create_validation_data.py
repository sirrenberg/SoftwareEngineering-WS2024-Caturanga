import csv
import os
from datetime import datetime
from helper_functions import date_format



def create_validation_data(dtm_merged_df, round_data, folder_name, country_name, start_date, end_date):
    """
    Create the validation data for the given country and time period.
        Parameters:
            dtm_merged_df (DataFrame): DataFrame containing the camp information
            round_data (list): List of dictionaries with the round number, the total number of IDPs and the date. This is already modified to just contain the rounds that are in the given time period.
            folder_name (str): Name of the folder where the CSV files will be stored
            country_name (str): Name of the country
            start_date (str): Start date of the time period
            end_date (str): End date of the time period
        Returns:
            retrieval_date (str): Date when the script was executed
            reformatted_start_date (str): Start date of the time period in the format YYYY-MM-DD
            reformatted_end_date (str): End date of the time period in the format YYYY-MM-DD
            covered_from (str): Date of the oldest round in the time period
            covered_to (str): Date of the latest round in the time period
            oldest_url (str): URL of the oldest round in the time period
            latest_url (str): URL of the latest round in the time period    
    """

    # retrieval date
    retrieval_date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

    # reformat the given dates from DD-MM-YYYY to YYYY-MM-DD in order to have the same format as in the ACLED-API
    reformatted_start_date = date_format(start_date)
    reformatted_end_date = date_format(end_date)

    # sort round_data by round number in descending order to get period covered
    round_data.sort(key=lambda x: x["round"], reverse=True)
    covered_to = round_data[0]["covered_to"]
    covered_from = round_data[-1]["covered_from"]
    latest_url = round_data[0]["source"]
    oldest_url = round_data[-1]["source"]


    create_refugee_csv(folder_name, round_data)
    location_files, camp_names = create_camp_csv(folder_name, country_name, dtm_merged_df, round_data)
    create_data_layout_csv(folder_name, location_files, camp_names)


    return retrieval_date, reformatted_start_date, reformatted_end_date, covered_from, covered_to, oldest_url, latest_url


def create_refugee_csv(folder_name, round_data):
    """ 
    Create refugees.csv with the date and the total number of conflict-driven IDPs at that moment
        Parameters:
            folder_name (str): Name of the folder where the CSV file will be stored
            round_data (list): List of dictionaries with the round number, the total number of IDPs and the date
    """
    # Get the current directory
    current_dir = os.getcwd()
    #open refugees.csv
    locations_file = os.path.join(current_dir, "conflict_validation", folder_name, "refugees.csv")
    # write refugees.csv        
    with open(locations_file, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        # header according to flee: https://github.com/djgroen/flee/blob/master/conflict_validation/ethiopia2020/refugees.csv
        writer.writerow(['Date', 'Refugee_numbers'])
        for data in round_data:
            latest_date = data["covered_to"]
            total_IDPs = data["total_IDP_conflict_number"]
            writer.writerow([latest_date, total_IDPs])
    
    print("Successfully added total IDP numbers to refugees.csv")


def create_camp_csv(folder_name, country_name, dtm_merged_df, round_data):
    """
    Create country_name-camp_name.csv for each camp in dtm_merged_df
        Parameters:
            folder_name (str): Name of the folder where the CSV files will be stored
            country_name (str): Name of the country
            dtm_merged_df (DataFrame): DataFrame containing the camp information
            round_data (list): List of dictionaries with the round number, the total number of IDPs and the date
    """
    # create a csv file for each camp with the title: countryname-campname.csv
    # write the following information into the csv file: date, population
    location_files = []
    camp_names = []
    for index, row in dtm_merged_df.iterrows():
        # Get the current directory
        current_dir = os.getcwd()
        #open country_name-camp_name.csv
        camp_name = row["name"]
        camp_names.append(camp_name)
        file_name = f"{country_name}-{camp_name}.csv"
        location_files.append(file_name)
        locations_file = os.path.join(current_dir, "conflict_validation", folder_name, file_name)
        # write country_name-camp_name.csv        
        with open(locations_file, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            # accordingly to flee, no header
            for data in round_data:
                latest_date = data["covered_to"]
                total_IDPs = row[f"population_round_{data['round']}"]
                writer.writerow([latest_date, total_IDPs])
    
    print("Successfully created files country_name-camp_name.csv and added conflict-driven IDP numbers to them")
    return location_files, camp_names



def create_data_layout_csv(folder_name, location_files, camp_names):
    """
    Create data_layout.csv
        Parameters:
            folder_name (str): Name of the folder where the CSV file will be stored
            location_files (list): List of the names of the location files
            camp_names (list): List of the names of the camps
    """

    combined_list = zip(location_files, camp_names)
    # Get the current directory
    current_dir = os.getcwd()
    #open data_layout.csv
    data_layout_file = os.path.join(current_dir, "conflict_validation", folder_name, "data_layout.csv")
    # write data_layout.csv        
    with open(data_layout_file, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        #header according to flee: https://github.com/djgroen/flee/blob/master/conflict_validation/ethiopia2020/data_layout.csv
        writer.writerow(['total', 'refugees.csv'])
        for entry in combined_list:
            location_file = entry[0]
            camp_name = entry[1]
            writer.writerow([camp_name, location_file])
        
        
    print("Successfully created data_layout.csv")