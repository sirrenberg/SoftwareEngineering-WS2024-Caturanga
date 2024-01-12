import csv
import os
from datetime import datetime
from helper_functions import date_format



def create_validation_data(dtm_merged_df, round_data, folder_name,country_name, start_date, end_date):
    # TODO: do something with start_date and end_date
    # reformat the given dates from DD-MM-YYYY to YYYY-MM-DD in order to have the same format as in the ACLED-API
    reformatted_start_date = date_format(start_date)
    reformatted_end_date = date_format(end_date)

    create_refugee_csv(folder_name, round_data)
    location_files, camp_names = create_camp_csv(folder_name, country_name, dtm_merged_df, round_data)
    create_data_layout_csv(folder_name, location_files, camp_names)


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
    




# OLD
"""
def create_refugee_csv(folder_name, start_date, end_date):
    '''
    Add the total number of IDPs to refugees.csv.
        Parameters:
            folder_name (str): Name of the folder where the file will be saved
            start_date (str): Start date of the time period
            end_date (str): End date of the time period
    '''

    '''
    The following files were used:
    Excel files from this websites where used:
    https://dtm.iom.int/datasets/ethiopia-site-assessment-round-34
    https://dtm.iom.int/datasets/ethiopia-site-assessment-round-33
    https://dtm.iom.int/datasets/ethiopia-site-assessment-round-32
    https://dtm.iom.int/datasets/ethiopia-site-assessment-round-31
    https://dtm.iom.int/datasets/ethiopia-site-assessment-round-30
    https://dtm.iom.int/datasets/ethiopia-site-assessment-round-29
    https://dtm.iom.int/datasets/ethiopia-site-assessment-round-28


    To just take into account the IDPs caused by conflict, often the following Excel command was used to calculate the sums:
    =SUMMEWENN(Table1[1.5.e.1: Reason for displacement]; "Conflict"; Table1[2.1.b.7: Total Number of IDP Individuals])
    '''


    # according to flee, date must have the format "yyyy-mm-dd"
    round_data = [
    {"round": 28, "total_IDPs": 1249693, "date": "2022-01-07"},
    {"round": 29, "total_IDPs": 1781460, "date": "2022-04-18"},
    {"round": 30, "total_IDPs": 1810765, "date": "2022-07-09"},
    {"round": 31, "total_IDPs": 1872723, "date": "2022-09-17"},
    {"round": 32, "total_IDPs": 1849742, "date": "2023-01-09"},
    {"round": 33, "total_IDPs": 1900920, "date": "2023-06-29"},
    {"round": 34, "total_IDPs": 2237195, "date": "2023-09-02"},
    ]

    # from round_data, get the date of the highest round number and lowest round number
    highest_round = round_data[0]["round"]
    lowest_round = round_data[0]["round"]
    latest_date = round_data[0]["date"]
    oldest_date = round_data[0]["date"]
    for data in round_data:
        if data["round"] > highest_round:
            highest_round = data["round"]
            latest_date = data["date"]
        if data["round"] < lowest_round:
            lowest_round = data["round"]
            oldest_date = data["date"]
    
    
    # date of retrieval, which is the date when the script is executed. Format: YYYY-MM-DD HH:MM:SS
    retrieval_date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

    # reformat the given dates from DD-MM-YYYY to YYYY-MM-DD in order to have the same format as in the ACLED-API
    reformatted_start_date = date_format(start_date)
    reformatted_end_date = date_format(end_date)

    # Get the current directory
    current_dir = os.getcwd()
    #open refugees.csv
    locations_file = os.path.join(current_dir, "conflict_validation", folder_name, "refugees.csv")
    # write refugees.csv        
    with open(locations_file, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Date', 'Refugee_numbers'])
        for data in round_data:
            current_date = data["date"]
            # convert to datetime object
            current_date_object = datetime.strptime(current_date, '%Y-%m-%d')
            start_date_object = datetime.strptime(reformatted_start_date, '%Y-%m-%d')
            end_date_object = datetime.strptime(reformatted_end_date, '%Y-%m-%d')
            # compare dates
            if current_date_object >= start_date_object and current_date_object <= end_date_object:
                writer.writerow([data["date"], data["total_IDPs"]])
    
    print("Successfully added total IDP numbers to refugees.csv")
    
    return retrieval_date, reformatted_start_date, reformatted_end_date, oldest_date, latest_date
"""
