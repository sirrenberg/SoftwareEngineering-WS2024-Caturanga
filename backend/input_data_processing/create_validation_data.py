import csv
import os
from datetime import datetime


def date_format(in_date):
    '''
    Function to format "dd-mm-yyyy" into "yyyy-mm-dd" format
        Parameters:
            in_date (str): Date in "dd-mm-yyyy" format
        Returns:
            (str): Date in "yyyy-mm-dd" format
    '''
    if "-" in in_date:
        split_date = in_date.split("-")
    else:
        split_date = in_date.split(" ")

    out_date = str(split_date[2]) + "-" + str(split_date[1]) + "-" + str(split_date[0])

    return out_date



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

    # convert start_date and end_date to "yyyy-mm-dd" format
    start_date = date_format(start_date)
    end_date = date_format(end_date)


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
            start_date_object = datetime.strptime(start_date, '%Y-%m-%d')
            end_date_object = datetime.strptime(end_date, '%Y-%m-%d')
            # compare dates
            if current_date_object >= start_date_object and current_date_object <= end_date_object:
                writer.writerow([data["date"], data["total_IDPs"]])

    
    print("Successfully added total IDP numbers to refugees.csv")
