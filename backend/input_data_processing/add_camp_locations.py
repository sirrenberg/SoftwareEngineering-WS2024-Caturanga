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
    dtm_merged_df, modified_round_data = extract_camp_locations(round_data)

    # filter by dates: Just include the rounds which are covered by the end_date and start_date
    reformatted_start_date = date_format(start_date)
    reformatted_end_date = date_format(end_date)

     # get rounds which are and which are not in the time period
    rounds_not_in_time_period = [round_entry["round"] for round_entry in modified_round_data if round_entry["covered_from"] < reformatted_start_date or round_entry["covered_to"] > reformatted_end_date]
    rounds_in_time_period = [round_entry["round"] for round_entry in modified_round_data if round_entry["covered_from"] >= reformatted_start_date and round_entry["covered_to"] <= reformatted_end_date]
    
    # modify modified_round_data to just inclide rounds in time period
    modified_round_data = [round_entry for round_entry in modified_round_data if round_entry["covered_from"] >= reformatted_start_date and round_entry["covered_to"] <= reformatted_end_date] 


    # delete the population columns and survey columns which do not have a round in the time period -> just keep rounds in time period
    for round_number in rounds_not_in_time_period:
        dtm_merged_df = dtm_merged_df.drop(columns=[f"population_round_{round_number}", f"survey_date_round_{round_number}"])


    # latest round -> sort by IDP conflict number -> keep top 10 rows -> get latest survey date
    # sort modified_round_data by round number in descending order to get latest info
    modified_round_data.sort(key=lambda x: x["round"], reverse=True)
    last_update = modified_round_data[0]["covered_to"]
    last_update_url = modified_round_data[0]["source"]
    latest_round = modified_round_data[0]["round"]
    # date of retrieval, which is the date when the script is executed. Format: YYYY-MM-DD HH:MM:SS
    retrieval_date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

    # sort by number_IDPs_conflict of latest round
    dtm_merged_df.sort_values(by=f"population_round_{latest_round}", ascending=False, inplace=True)
    dtm_merged_df = dtm_merged_df.reset_index(drop=True)
    
    # just keep top rows_shown entries
    dtm_merged_df = dtm_merged_df.head(rows_shown)

    # get latest survey date
    latest_survey_date = dtm_merged_df[f"survey_date_round_{latest_round}"].tolist()
    latest_survey_date.sort(reverse=True)
    latest_survey_date = latest_survey_date[0]


    # get the key for population for the latest round 
    latest_round_population_key = f"population_round_{latest_round}"
    latest_dtm_df = dtm_merged_df[["name", "region", "country", "latitude", "longitude", "location_type", "conflict_date", latest_round_population_key]]
    latest_dtm_df = latest_dtm_df.rename(columns={"name":"#name", latest_round_population_key: "population"})

    # append the locations.csv with the latest camp information
    latest_dtm_df.to_csv(os.path.join(folder_name, "locations.csv"), mode='a', header=False, index=False)

    print("Successfully added camp locations to locations.csv")

    # remove survey_dates for all rounds from dtm_merged_df except for the latest round
    for round_number in rounds_in_time_period:
        if round_number != latest_round:
            dtm_merged_df = dtm_merged_df.drop(columns=[f"survey_date_round_{round_number}"])

    print("modified round data")
    print(modified_round_data)
    print("latest_dtm_df")
    print(latest_dtm_df)
    print("dtm_merged_df: ")
    print(dtm_merged_df)
    print("dtm_mgerged_df columns: ")
    print(dtm_merged_df.columns)

    return dtm_merged_df, modified_round_data, last_update_url, retrieval_date, last_update, reformatted_start_date, reformatted_end_date, latest_survey_date



def extract_camp_locations(round_data):
    """
    The function extracts the camp locations with information from the DTM excel files and returns a dataframe with the camps and IDP numbers. Additionally it adds the total number of IDPs per period to round_data.
    Parameters:
        round_data (list): List of dictionaries with information about the rounds
    Returns:
        dtm_merged_df (dataframe): Merged dataframe with the camp locations
        round_data (list): List of dictionaries with information about the rounds. The total number of IDPs caused by conflict is added to the dictionary.
    """

    # REMARK: neither the data format of the excel files nor the available columns is consistent, therefore the extraction of the data is not universally applicable.
    # data for round 34 has no informatin for longitude and latitude of sites
    # other differences (among others):
        #  "DTM Ethiopia - Site Assessment Round 34.xlsx' has no information for longitude and latitude of sites
        #  "DTM Ethiopia - Site Assessment Round 34.xlsx' has "xxxx: Site Classification" instead of "Site Classification"
        #  "DTM Ethiopia - Site Assessment Round 33.xlsx' has "xxxx: Settlement/site type" instead of "1.3.b.1: Settlement/site type"
    

    # get current directory
    current_dir = os.getcwd()
    # paths to files with camp information
    # docker path
    # paths_dtm = os.path.join(current_dir, "input_data_processing", "conflict_validation", "data_source")
    paths_dtm = os.path.join(current_dir, "conflict_validation", "data_source")


    # create empty dataframe
    dtm_merged_df = pd.DataFrame()

    for current_round in round_data: # rounds already in descending order
        round_number = current_round["round"]
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
        if round_number == 34: # round 34 has no extra split up number of IDPs by reason for displacement. Do it by myself
            # create new column "number_IDPs_conflict" and fill with values for "total_number_IDPs" if "reason_for_displacement" == "Conflict", otherwise with 0
            dtm_df["number_IDPs_conflict"] = np.where(dtm_df["reason_for_displacement"] == "Conflict", dtm_df["total_number_IDPs"], 0)

        # sum the number_IDPs_conflict column
        total_IDP_conflict_number = dtm_df["number_IDPs_conflict"].sum()

        # add total_IDP_conflict_number to correct round_data
        for round_data_entry in round_data:
            if round_data_entry["round"] == round_number:
                round_data_entry["total_IDP_conflict_number"] = total_IDP_conflict_number

        
        # check if site_id unique. If not, then group by site_id and sum relevant columns
        if not dtm_df["site_id"].is_unique:
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


        if dtm_merged_df.empty:  # first iteration through the loop
            # Keep only the rows with settlement_type: Spontaneous camp/site or Planned camp/site
            # these camps of the latest data (round 34) are the baseline 
            dtm_df = dtm_df.loc[(dtm_df["settlement_type"] == "Spontaneous camp/site") | (dtm_df["settlement_type"] == "Planned camp/site")]
        else:
            # get site ids as list
            relevant_site_ids = dtm_merged_df["site_id"].tolist()
            # just keep the rows with site_id of our baseline (round 34)
            dtm_df = dtm_df[dtm_df["site_id"].isin(relevant_site_ids)]
        

        # delete columns and change order to match locations.csv. Add location_type and conflict_date
        dtm_df["location_type"] = "idpcamp"
        dtm_df["conflict_date"] = 0

        if "latitude" in dtm_df.columns:
            # number_IDPs_conflict for each camp (additionally there could be other reasons why IDPs flee. We just focus on conflicts)
            dtm_df = dtm_df[['site_id', 'site_name', 'region', 'country', 'latitude', 'longitude', 'location_type', 'survey_date', 'conflict_date', 'number_IDPs_conflict']]
            # Rename the columns
            dtm_df = dtm_df.rename(columns={"site_name": "name", "number_IDPs_conflict": "population"})
        else: 
            dtm_df = dtm_df[['site_id', 'site_name', 'region', 'country', 'location_type', 'survey_date', 'conflict_date', 'number_IDPs_conflict']]
            # Rename the columns
            dtm_df = dtm_df.rename(columns={"site_name": "name", "number_IDPs_conflict": "population"})

        dtm_df_premerged = pd.DataFrame()

        if dtm_merged_df.empty: # first iteration through the loop
            dtm_merged_df = dtm_df
            dtm_merged_df = dtm_merged_df.rename(columns={"population": f"population_round_{round_number}", "survey_date": f"survey_date_round_{round_number}"})
        else:
            dtm_df_premerged = dtm_df[['site_id', 'latitude', 'longitude', 'population', 'survey_date']]
            dtm_df_premerged = dtm_df_premerged.rename(columns={"population": f"population_round_{round_number}", "survey_date": f"survey_date_round_{round_number}"})
        

        # check if column latitude and longitude is in dtm_merged_df, then drop
        if "latitude" in dtm_merged_df.columns:
            # drop column in dtm_df_premerged
            dtm_df_premerged = dtm_df_premerged.drop(columns=["latitude", "longitude"])
        
        # merge (append) dataframes if not empty
        if not dtm_df_premerged.empty:
            dtm_merged_df = pd.merge(dtm_merged_df, dtm_df_premerged, on="site_id", how="inner") # inner join on site_id
        # rename current round population and survey_date column
        # TODO: necessary??
        dtm_merged_df = dtm_merged_df.rename(columns={"population": f"population_round_{round_number}", "survey_date": f"survey_date_round_{round_number}"})

        print(f"round_number: {round_number}, total_IDP_conflict_number: {total_IDP_conflict_number}")
    print(dtm_merged_df.sort_values(by="site_id"))

    return dtm_merged_df, round_data