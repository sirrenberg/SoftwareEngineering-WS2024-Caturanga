import csv
import os
import openpyxl #TODO: necessary??
import pandas as pd
import numpy as np
from datetime import datetime
from extract_locations_csv import date_format

# TODO: do this for all date_format calls

def extract_camp_locations(rows_shown):
    # TODO: docstring
    '''
    Add camp locations to locations.csv
        Parameters:
            folder_name (str): Name of the folder containing the CSV files
            rows_shown (int): Number of camps to be shown in the CSV file
    '''

    '''
    The following files were used:
    Excel files from this websites where used:
    https://dtm.iom.int/datasets/ethiopia-site-assessment-round-34
    https://dtm.iom.int/datasets/ethiopia-site-assessment-round-33
    https://dtm.iom.int/datasets/ethiopia-site-assessment-round-32
    https://dtm.iom.int/datasets/ethiopia-site-assessment-round-31
    '''


    # according to flee, date must have the format "yyyy-mm-dd"
    round_data = [
    {"round": 32, "covered_from": "2022-11-25", "covered_to": "2023-01-09"},
    {"round": 33, "covered_from": "2023-06-11", "covered_to": "2023-06-29"},
    {"round": 34, "covered_from": "2023-08-01", "covered_to": "2023-09-02"},
    ]

    # REMARK: neither the data format of the excel files nor the available columns is consistent, therefore the extraction of the data is not universally applicable.
    # data for round 34 has no informatin for longitude and latitude of sites, therefore the basis for the extraction is round 33
    # other differences (among others):
        #  "DTM Ethiopia - Site Assessment Round 34.xlsx' has no information for longitude and latitude of sites
        #  "DTM Ethiopia - Site Assessment Round 34.xlsx' has "xxxx: Site Classification" instead of "Site Classification"
        #  "DTM Ethiopia - Site Assessment Round 33.xlsx' has "xxxx: Settlement/site type" instead of "1.3.b.1: Settlement/site type"
    

    # get current directory
    current_dir = os.getcwd()
    # paths to files with camp information
    paths_dtm = os.path.join(current_dir, "conflict_validation", "data_source")


    round_numbers = [34, 33, 32]
    dtm_merged_df = pd.DataFrame()

    for round_number in round_numbers:
        excel_file = os.path.join(paths_dtm, f"DTM Ethiopia - Site Assessment Round {round_number}.xlsx")

        # extract information from excel files
        file_path = os.path.join(paths_dtm, excel_file)
        data = pd.ExcelFile(file_path)
        sheet_names = data.sheet_names

        # worksheet it is either "Sites", "Master Location Baseline Update" or "R32 and R33 Consolidated Sites"
        if "Sites" in sheet_names:
            dtm_df = data.parse("Sites")
        elif "Master Location Baseline Update" in sheet_names:
            dtm_df = data.parse("Master Location Baseline Update")
        elif "R32 and R33 Consolidated Sites" in sheet_names:
            dtm_df = data.parse("R32 and R33 Consolidated Sites")
        else: 
            print("Sheet not found")
        if (round_number == 32 or round_number == 33):
            dtm_df = dtm_df[["1.1.a.1: Survey Date", "Country", "1.1.a.2: Survey Round", "1.1.c.1: Site ID", "1.1.d.1: Site Name", "1.1.f.1: GPS: Longitude", "1.1.f.2: GPS: Latitude", "1.1.e.1: Region", "Most reported reason for displacement in the site", "Site Classification", "1.3.b.1: Settlement/site type", "2.1.b.7: Total Number of IDP Individuals", "Reason for Displacement (Individuals): Conflict"]]
            # rename columns
            dtm_df = dtm_df.rename(columns={"1.1.a.1: Survey Date": "survey_date", "Country": "country", "1.1.a.2: Survey Round": "survey_round", "1.1.c.1: Site ID": "site_id", "1.1.d.1: Site Name": "site_name", "1.1.f.1: GPS: Longitude": "longitude", "1.1.f.2: GPS: Latitude": "latitude", "1.1.e.1: Region": "region", "Most reported reason for displacement in the site": "main_reason_for_displacement", "Site Classification": "site_classification", "1.3.b.1: Settlement/site type": "settlement_type", "2.1.b.7: Total Number of IDP Individuals": "total_number_IDPs", "Reason for Displacement (Individuals): Conflict": "number_IDPs_conflict"})
        elif round_number == 34:
            dtm_df = dtm_df[["1.1.a.1: Survey Date", "Country", "1.1.a.2: Survey Round", "1.1.c.1: Site ID", "1.1.d.1: Site Name", "1.1.e.1: Region", "1.5.e.1: Reason for displacement", "xxxx: Site Classification", "1.3.b.1: Settlement/site type", "2.1.b.7: Total Number of IDP Individuals"]]
            # rename columns
            dtm_df = dtm_df.rename(columns={"1.1.a.1: Survey Date": "survey_date", "Country": "country", "1.1.a.2: Survey Round": "survey_round", "1.1.c.1: Site ID": "site_id", "1.1.d.1: Site Name": "site_name", "1.1.e.1: Region": "region", "1.5.e.1: Reason for displacement" : "reason_for_displacement", "xxxx: Site Classification": "site_classification", "1.3.b.1: Settlement/site type": "settlement_type", "2.1.b.7: Total Number of IDP Individuals": "total_number_IDPs"})
        else: 
            print("Not possible to extract information for this round_number due to incompatibility of data formats!")


        if round_number == 33:
            # drop first row and reset index
            dtm_df = dtm_df.drop([0])
            dtm_df = dtm_df.reset_index(drop=True)
        
        """
        DISCLAIMER:
        In the Excel file for round 34 there is just given the main reason for displacement (1.5.e.1: Reason for displacement) and the total number of IDPs (2.1.b.7: Total Number of IDP Individuals) in the camp. This file is our baseline since it contains the most recent data.
        For the other rounds, the Excel files contain the total number of IDPs (2.1.b.7: Total Number of IDP Individuals) in the camp, the "Most reported reason for displacement in the site" and then split by the different reasons: among others "Reason for Displacement (Individuals): Conflict", "Reason for Displacement (Individuals): Drought"
        The problem is that for example in round 34 the main reason is conflict and the total number of IDPs is 15595. But in round 33 the most reported reason is drought and the total number of IDPs is 17169, split by 0 IDPs for conflict and 17169 IDPs for drought. 
        """

        if (round_number == 32 or round_number == 33):
            # Replace non-finite values with zero
            dtm_df["number_IDPs_conflict"] = dtm_df["number_IDPs_conflict"].replace([np.inf, -np.inf, np.nan], 0)
            # convert number_IDPs_conflict to int
            dtm_df["number_IDPs_conflict"] = dtm_df["number_IDPs_conflict"].astype(int)
        elif round_number == 34:
            # Replace non-finite values with zero
            dtm_df["total_number_IDPs"] = dtm_df["total_number_IDPs"].replace([np.inf, -np.inf, np.nan], 0)
            # convert total_number_IDPs to int
            dtm_df["total_number_IDPs"] = dtm_df["total_number_IDPs"].astype(int)
        else: 
            print("Not possible to extract information for this round_number due to incompatibility of data formats!")

        # TODO: check if site_id unique
        
        # total number of IDPs caused by conflict
        if round_number == 34:
            total_IDP_conflict_number = dtm_df.loc[dtm_df["reason_for_displacement"] == "Conflict", "total_number_IDPs"].sum()
        elif (round_number == 32 or round_number == 33):
            # sum of column number_IDPs_conflict (formerly: Reason for Displacement (Individuals): Conflict)
            total_IDP_conflict_number = dtm_df["number_IDPs_conflict"].sum()
        else: 
            print("Not possible to extract information for this round_number due to incompatibility of data formats!")
        
        
        # add total_IDP_conflict_number to round_data
        for round_data_dict in round_data:
            if round_data_dict["round"] == round_number:
                round_data_dict["total_IDP_conflict_number"] = total_IDP_conflict_number

        # first iteration
        if dtm_merged_df.empty:
            # Keep only the rows with settlement_type: Spontaneous camp/site or Planned camp/site
            dtm_df = dtm_df.loc[(dtm_df["settlement_type"] == "Spontaneous camp/site") | (dtm_df["settlement_type"] == "Planned camp/site")]
            
            # sort by number_IDPs_conflict
            dtm_df.sort_values(by="total_number_IDPs", ascending=False, inplace=True)
            dtm_df = dtm_df.reset_index(drop=True)

            # just keep top rows_shown entries
            dtm_df = dtm_df.head(rows_shown)

        # check if dtm_merged_df is empty
        else:
            # get site ids as list
            relevant_site_ids = dtm_merged_df["site_id"].tolist()
            dtm_df = dtm_df[dtm_df["site_id"].isin(relevant_site_ids)]
        

        # delete columns and change order to match locations.csv. Add location_type and conflict_date
        dtm_df["location_type"] = "idpcamp"
        dtm_df["conflict_date"] = 0

        if "latitude" in dtm_df.columns:
            # number_IDPs_conflict for each camp (additionally there could be other reasons why IDPs flee. We just focus on conflicts)
            dtm_df = dtm_df[['site_id', 'site_name', 'region', 'country', 'latitude', 'longitude', 'location_type', 'conflict_date', 'number_IDPs_conflict']]
            # Rename the columns
            dtm_df = dtm_df.rename(columns={"site_id": "site_id", "site_name": "name", "region": "region", "country": "country", "latitude": "latitude", "longitude": "longitude", "location_type": "location_type", "conflict_date": "conflict_date", "number_IDPs_conflict": "population"})
        else: 
            dtm_df = dtm_df[['site_id', 'site_name', 'region', 'country', 'location_type', 'conflict_date', 'total_number_IDPs']]
            # Rename the columns
            dtm_df = dtm_df.rename(columns={"site_id": "site_id", "site_name": "name", "region": "region", "country": "country", "location_type": "location_type", "conflict_date": "conflict_date", "total_number_IDPs": "population"})

        dtm_df_premerged = pd.DataFrame()

        if dtm_merged_df.empty:
            dtm_merged_df = dtm_df
            dtm_merged_df = dtm_merged_df.rename(columns={"population": f"population_round_{round_number}"})
        else:
            dtm_df_premerged = dtm_df[['site_id', 'latitude', 'longitude', 'population']]
            dtm_df_premerged = dtm_df_premerged.rename(columns={"site_id": "site_id", "latitude": "latitude", "longitude": "longitude", "population": f"population_round_{round_number}"})
        

        # check if column latitude and longitude is in dtm_merged_df. Then drop
        if "latitude" in dtm_merged_df.columns:
            # drop column in dtm_df_premerged
            dtm_df_premerged = dtm_df_premerged.drop(columns=["latitude", "longitude"])
        
        if not dtm_df_premerged.empty:
            dtm_merged_df = pd.merge(dtm_merged_df, dtm_df_premerged, on="site_id", how="left")
        
        dtm_merged_df = dtm_merged_df.rename(columns={"population": f"population_round_{round_number}"})


        print(f"round_number: {round_number}, total_IDP_conflict_number: {total_IDP_conflict_number}")

        # print("dtm_merged_df:")
        # print(dtm_merged_df)
    
    print("dtm_merged_df:")
    print(dtm_merged_df)
    return dtm_merged_df, round_data
    


def add_camp_locations(folder_name, country_name, rows_shown, start_date, end_date):
    # TODO: docstring
    dtm_merged_df, round_data = extract_camp_locations(rows_shown)

    # TODO: do something with start_date and end_date

    dtm_34_df = dtm_merged_df[["name", "region", "country", "latitude", "longitude", "location_type", "conflict_date", "population_round_34"]]
    dtm_34_df = dtm_34_df.rename(columns={"name":"#name", "population_round_34": "population"})


    # Get the current directory
    current_dir = os.getcwd()
    #open locations.csv
    locations_file = os.path.join(current_dir, folder_name, "locations.csv")
    # append the locations.csv with the camp information
    dtm_34_df.to_csv(os.path.join(folder_name, "locations.csv"), mode='a', header=False, index=False)

    print("Successfully added camp locations to locations.csv")


    create_validation_data(dtm_merged_df, round_data, folder_name, country_name, start_date, end_date)




def create_validation_data(dtm_merged_df, round_data, folder_name,country_name, start_date, end_date):
    # TODO: do something with start_date and end_date
    # reformat the given dates from DD-MM-YYYY to YYYY-MM-DD in order to have the same format as in the ACLED-API
    reformatted_start_date = date_format(start_date)
    reformatted_end_date = date_format(end_date)

    create_refugee_csv(folder_name, round_data)
    location_files, camp_names = create_camp_csv(folder_name, country_name, dtm_merged_df, round_data)
    create_data_layout_csv(folder_name, location_files, camp_names)


    # needed csv files:
    # refugee.csv with total numbers of IDPs: data, number
    # country_name-camp_name.csv:
    # data_layout.csv with: camp name,  country_name-camp_name.csv


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
    






