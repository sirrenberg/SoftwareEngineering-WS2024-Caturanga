import csv
import os
import pandas as pd
import numpy as np
from datetime import datetime
from helper_functions import date_format
import openpyxl

def add_camp_locations(round_data, folder_name, rows_shown, start_date, end_date):
    """
    The function adds the latest camp information to the locations.csv file.
    Parameters:
        round_data (list): List of dictionaries with information about the rounds
        folder_name (str): Name of the folder containing the CSV files
        rows_shown (int): Number of camps to be shown in the CSV file
        start_date (str): Start date of the time period
        end_date (str): End date of the time period
    Returns:
        dtm_merged_df (dataframe): Merged dataframe with the camp locations within the specified time period
        modified_round_data (list): List of dictionaries with information about the rounds within the time period. The total number of IDPs caused by conflict is added to the dictionary.
        last_update_url (str): URL of the source of the last update
        retrieval_date (str): Date of retrieval, which is the date when the script is executed. Format: YYYY-MM-DD HH:MM:SS
        last_update (str): Last update of the data. Format: YYYY-MM-DD
        reformatted_start_date (str): Reformatted start date. Format: YYYY-MM-DD
        reformatted_end_date (str): Reformatted end date. Format: YYYY-MM-DD
        latest_survey_date (str): Latest survey date. Format: YYYY-MM-DD
    """
    # sort dict by round number in descending order
    round_data.sort(key=lambda x: x["round"], reverse=True)

    # filter by end_date: Just include the rounds which are covered by the end_date and start_date
    reformatted_start_date = date_format(start_date)
    reformatted_end_date = date_format(end_date)
    round_data = [round for round in round_data if round["covered_from"] >= reformatted_start_date and round["covered_to"] <= reformatted_end_date]
    
    dtm_merged_df, modified_round_data, latest_survey_date = extract_camp_locations(round_data, rows_shown)

    # sort round_data by round number in descending order to get latest info
    modified_round_data.sort(key=lambda x: x["round"], reverse=True)
    last_update = modified_round_data[0]["covered_to"]
    last_update_url = modified_round_data[0]["source"]
    latest_round = modified_round_data[0]["round"]
    # date of retrieval, which is the date when the script is executed. Format: YYYY-MM-DD HH:MM:SS
    retrieval_date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

    # get the key for population for the latest round
    latest_round_population_key = f"population_round_{latest_round}"
    latest_dtm_df = dtm_merged_df[["name", "region", "country", "latitude", "longitude", "location_type", "conflict_date", latest_round_population_key]]
    latest_dtm_df = latest_dtm_df.rename(columns={"name":"#name", latest_round_population_key: "population"})

    # append the locations.csv with the latest camp information
    latest_dtm_df.to_csv(os.path.join(folder_name, "locations.csv"), mode='a', header=False, index=False)

    print("Successfully added camp locations to locations.csv")

    return dtm_merged_df, modified_round_data, last_update_url, retrieval_date, last_update, reformatted_start_date, reformatted_end_date, latest_survey_date



def extract_camp_locations(round_data, rows_shown):
    """
    The function extracts the camp locations with information from the DTM excel files and returns a dataframe with the camps and IDP numbers. Additionally it adds the total number of IDPs per period to round_data.
    Parameters:
        round_data (list): List of dictionaries with information about the rounds
        rows_shown (int): Number of camps to be shown in the CSV file
    Returns:
        dtm_merged_df (dataframe): Merged dataframe with the camp locations
        round_data (list): List of dictionaries with information about the rounds. The total number of IDPs caused by conflict is added to the dictionary.
        latest_survey_date (str): Latest survey date. Format: YYYY-MM-DD
    """

    # REMARK: neither the data format of the excel files nor the available columns is consistent, therefore the extraction of the data is not universally applicable.
    # data for round 34 has no informatin for longitude and latitude of sites
    # other differences (among others):
        #  "DTM Ethiopia - Site Assessment Round 34.xlsx' has no information for longitude and latitude of sites
        #  "DTM Ethiopia - Site Assessment Round 34.xlsx' has "xxxx: Site Classification" instead of "Site Classification"
        #  "DTM Ethiopia - Site Assessment Round 33.xlsx' has "xxxx: Settlement/site type" instead of "1.3.b.1: Settlement/site type"
    
    #TODO: make it universal. weniger if else für rounds

    # get current directory
    current_dir = os.getcwd()
    # paths to files with camp information
    # TODO: docker path
    # paths_dtm = os.path.join(current_dir, "input_data_processing", "conflict_validation", "data_source")
    paths_dtm = os.path.join(current_dir, "conflict_validation", "data_source")

    # get round numbers from dict
    round_numbers = []
    for round in round_data:
        round_numbers.append(round["round"])

    # create empty dataframe
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
            dtm_df = dtm_df[["1.1.a.1: Survey Date", "Reported Date", "Country", "1.1.a.2: Survey Round", "1.1.c.1: Site ID", "1.1.d.1: Site Name", "1.1.f.1: GPS: Longitude", "1.1.f.2: GPS: Latitude", "1.1.e.1: Region", "Most reported reason for displacement in the site", "Site Classification", "1.3.b.1: Settlement/site type", "2.1.b.7: Total Number of IDP Individuals", "Reason for Displacement (Individuals): Conflict"]]
            # rename columns
            dtm_df = dtm_df.rename(columns={"1.1.a.1: Survey Date": "survey_date", "Reported Date": "reported_date", "Country": "country", "1.1.a.2: Survey Round": "survey_round", "1.1.c.1: Site ID": "site_id", "1.1.d.1: Site Name": "site_name", "1.1.f.1: GPS: Longitude": "longitude", "1.1.f.2: GPS: Latitude": "latitude", "1.1.e.1: Region": "region", "Most reported reason for displacement in the site": "main_reason_for_displacement", "Site Classification": "site_classification", "1.3.b.1: Settlement/site type": "settlement_type", "2.1.b.7: Total Number of IDP Individuals": "total_number_IDPs", "Reason for Displacement (Individuals): Conflict": "number_IDPs_conflict"})
        elif round_number == 34:
            dtm_df = dtm_df[["1.1.a.1: Survey Date", "Reported Date", "Country", "1.1.a.2: Survey Round", "1.1.c.1: Site ID", "1.1.d.1: Site Name", "1.1.e.1: Region", "1.5.e.1: Reason for displacement", "xxxx: Site Classification", "1.3.b.1: Settlement/site type", "2.1.b.7: Total Number of IDP Individuals"]]
            # rename columns
            dtm_df = dtm_df.rename(columns={"1.1.a.1: Survey Date": "survey_date", "Reported Date": "reported_date", "Country": "country", "1.1.a.2: Survey Round": "survey_round", "1.1.c.1: Site ID": "site_id", "1.1.d.1: Site Name": "site_name", "1.1.e.1: Region": "region", "1.5.e.1: Reason for displacement" : "reason_for_displacement", "xxxx: Site Classification": "site_classification", "1.3.b.1: Settlement/site type": "settlement_type", "2.1.b.7: Total Number of IDP Individuals": "total_number_IDPs"})
        else: 
            print("Not possible to extract information for this round_number due to incompatibility of data formats!")


        if round_number == 33:
            # drop first row and reset index. Due to the fact that the first row contains unnecessary information because of the Excel file
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

        
        # check if site_id unique. If not, then group by site_id and sum relevant columns
        if not dtm_df["site_id"].is_unique:
            if round_number == 34:
                # Group by "site_id" and sum "total_number_IDPs", keeping other columns unchanged (use first value with "first")
                dtm_df = dtm_df.groupby("site_id").agg({
                    "survey_date": "first",
                    "reported_date": "first",
                    "country": "first",
                    "survey_round": "first",
                    "site_name": "first",
                    "region": "first",
                    "reason_for_displacement": "first",
                    "site_classification": "first",
                    "settlement_type": "first",
                    "total_number_IDPs": "sum"
                }).reset_index()
            elif (round_number == 32 or round_number == 33):
                # Group by "site_id" and sum "total_number_IDPs" and "number_IDPs_conflict", keeping other columns unchanged
                dtm_df = dtm_df.groupby("site_id").agg({
                    "survey_date": "first",
                    "reported_date": "first",
                    "country": "first",
                    "survey_round": "first",
                    "site_name": "first",
                    "longitude": "first",
                    "latitude": "first",
                    "region": "first",
                    "main_reason_for_displacement": "first",
                    "site_classification": "first",
                    "settlement_type": "first",
                    "total_number_IDPs": "sum",
                    "number_IDPs_conflict": "sum"
                }).reset_index()
            else:
                print("Not possible to extract information for this round_number due to incompatibility of data formats!")


        # first iteration
        if dtm_merged_df.empty:
            # Keep only the rows with settlement_type: Spontaneous camp/site or Planned camp/site
            dtm_df = dtm_df.loc[(dtm_df["settlement_type"] == "Spontaneous camp/site") | (dtm_df["settlement_type"] == "Planned camp/site")]
            
            # sort by number_IDPs_conflict
            dtm_df.sort_values(by="total_number_IDPs", ascending=False, inplace=True)
            dtm_df = dtm_df.reset_index(drop=True)

            # just keep top rows_shown entries
            dtm_df = dtm_df.head(rows_shown)

            # latest reported_date  
            survey_dates = dtm_df["survey_date"].tolist()
            survey_dates.sort(reverse=True)
            latest_survey_date = survey_dates[0]


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
            dtm_df = dtm_df.rename(columns={"site_name": "name", "number_IDPs_conflict": "population"})
        else: 
            dtm_df = dtm_df[['site_id', 'site_name', 'region', 'country', 'location_type', 'conflict_date', 'total_number_IDPs']]
            # Rename the columns
            dtm_df = dtm_df.rename(columns={"site_name": "name","total_number_IDPs": "population"})

        dtm_df_premerged = pd.DataFrame()

        if dtm_merged_df.empty:
            dtm_merged_df = dtm_df
            dtm_merged_df = dtm_merged_df.rename(columns={"population": f"population_round_{round_number}"})
        else:
            dtm_df_premerged = dtm_df[['site_id', 'latitude', 'longitude', 'population']]
            dtm_df_premerged = dtm_df_premerged.rename(columns={"population": f"population_round_{round_number}"})
        

        # check if column latitude and longitude is in dtm_merged_df. Then drop
        if "latitude" in dtm_merged_df.columns:
            # drop column in dtm_df_premerged
            dtm_df_premerged = dtm_df_premerged.drop(columns=["latitude", "longitude"])
        
        if not dtm_df_premerged.empty:
            dtm_merged_df = pd.merge(dtm_merged_df, dtm_df_premerged, on="site_id", how="left")
        
        dtm_merged_df = dtm_merged_df.rename(columns={"population": f"population_round_{round_number}"})

        print(f"round_number: {round_number}, total_IDP_conflict_number: {total_IDP_conflict_number}")
    print(dtm_merged_df)

    return dtm_merged_df, round_data, latest_survey_date