import csv
import os
import openpyxl
import pandas as pd
import numpy as np

def add_camp_locations(folder_name, rows_shown):
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

    # get current directory
    current_dir = os.getcwd()
    # paths to files with camp information
    paths_dtm = os.path.join(current_dir, "conflict_validation", "data_source")

    # list excel files in folder and sort in descending order
    excel_files = [f for f in os.listdir(paths_dtm) if f.endswith('.xlsx')]
    excel_files.sort(reverse=True)
    "##########################################################################################################"
    round_numbers = [34, 33, 32]
    dtm_merged_df = pd.DataFrame()

    for round_number in round_numbers:
        test_file = os.path.join(paths_dtm, f"DTM Ethiopia - Site Assessment Round {round_number}.xlsx")

        # extract information from excel files
        file_path = os.path.join(paths_dtm, test_file)
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
            # sum of column Reason for Displacement (Individuals): Conflict
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
            dtm_df = dtm_df.rename(columns={"site_id": "site_id", "site_name": "#name", "region": "region", "country": "country", "latitude": "latitude", "longitude": "longitude", "location_type": "location_type", "conflict_date": "conflict_date", "number_IDPs_conflict": "population"})
        else: 
            dtm_df = dtm_df[['site_id', 'site_name', 'region', 'country', 'location_type', 'conflict_date', 'total_number_IDPs']]
            # Rename the columns
            dtm_df = dtm_df.rename(columns={"site_id": "site_id", "site_name": "#name", "region": "region", "country": "country", "location_type": "location_type", "conflict_date": "conflict_date", "total_number_IDPs": "population"})

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


        print(f"Round number: {round_number}")
        print("dtm_merged_df:")
        print(dtm_merged_df)
    
    print(round_data)









    "##########################################################################################################"
    # REMARK: neither the data format of the excel files nor the available columns is consistent, therefore the extraction of the data is not universally applicable.
    # data for round 34 has no informatin for longitude and latitude of sites, therefore the basis for the extraction is round 33
    # other differences (among others):
        #  "DTM Ethiopia - Site Assessment Round 34.xlsx' has no information for longitude and latitude of sites
        #  "DTM Ethiopia - Site Assessment Round 34.xlsx' has "xxxx: Site Classification" instead of "Site Classification"
        #  "DTM Ethiopia - Site Assessment Round 33.xlsx' has "xxxx: Settlement/site type" instead of "1.3.b.1: Settlement/site type"
    
    """
    # extract values for round 34 as baseline. The problem is that this does not contains longitude and latitude of sites
    round_number = 34
    test_file = os.path.join(paths_dtm, f"DTM Ethiopia - Site Assessment Round {round_number}.xlsx")

    # extract information from excel files
    file_path = os.path.join(paths_dtm, test_file)
    data = pd.ExcelFile(file_path)
    sheet_names = data.sheet_names

    # worksheet it is either "Sites", "Master Location Baseline Update" or "R32 and R33 Consolidated Sites"
    if "Sites" in sheet_names:
        dtm_df_34 = data.parse("Sites")
    elif "Master Location Baseline Update" in sheet_names:
        dtm_df_34 = data.parse("Master Location Baseline Update")
    elif "R32 and R33 Consolidated Sites" in sheet_names:
        dtm_df_34 = data.parse("R32 and R33 Consolidated Sites")
    else: 
        print("Sheet not found")

    dtm_df_34 = dtm_df_34[["1.1.a.1: Survey Date", "Country", "1.1.a.2: Survey Round", "1.1.c.1: Site ID", "1.1.d.1: Site Name", "1.1.e.1: Region", "1.5.e.1: Reason for displacement", "xxxx: Site Classification", "1.3.b.1: Settlement/site type", "2.1.b.7: Total Number of IDP Individuals"]]
    # rename columns
    dtm_df_34 = dtm_df_34.rename(columns={"1.1.a.1: Survey Date": "survey_date", "Country": "country", "1.1.a.2: Survey Round": "survey_round", "1.1.c.1: Site ID": "site_id", "1.1.d.1: Site Name": "site_name", "1.1.e.1: Region": "region", "1.5.e.1: Reason for displacement" : "reason_for_displacement", "xxxx: Site Classification": "site_classification", "1.3.b.1: Settlement/site type": "settlement_type", "2.1.b.7: Total Number of IDP Individuals": "total_number_IDPs"})

   
    # Replace non-finite values with zero
    dtm_df_34["total_number_IDPs"] = dtm_df_34["total_number_IDPs"].replace([np.inf, -np.inf, np.nan], 0)
    # convert total_number_IDPs to int
    dtm_df_34["total_number_IDPs"] = dtm_df_34["total_number_IDPs"].astype(int)

    # TODO: check if site_id unique

    # sum of column Reason for Displacement (Individuals): Conflict
    total_IDP_conflict_number = dtm_df_34.loc[dtm_df_34["reason_for_displacement"] == "Conflict", "total_number_IDPs"].sum()

    # Keep only the rows with settlement_type: Spontaneous camp/site or Planned camp/site
    dtm_df_34 = dtm_df_34.loc[(dtm_df_34["settlement_type"] == "Spontaneous camp/site") | (dtm_df_34["settlement_type"] == "Planned camp/site")]
    
    # sort by number_IDPs_conflict
    dtm_df_34.sort_values(by="total_number_IDPs", ascending=False, inplace=True)
    dtm_df_34 = dtm_df_34.reset_index(drop=True)

    # just keep top rows_shown entries
    dtm_df_34 = dtm_df_34.head(rows_shown)

    # delete columns and change order to match locations.csv. Add location_type and conflict_date
    dtm_df_34["location_type"] = "idpcamp"
    dtm_df_34["conflict_date"] = 0
    # number_IDPs_conflict for each camp (additionally there could be other reasons why IDPs flee. We just focus on conflicts)
    dtm_df_34 = dtm_df_34[['site_id', 'site_name', 'region', 'country', 'location_type', 'conflict_date', 'total_number_IDPs']]

    # rename to: name,region,country,latitude,longitude,location_type,conflict_date,population
    # Rename the columns
    dtm_df_34 = dtm_df_34.rename(columns={"site_id":"site_id", "site_name": "#name", "region": "region", "country": "country", "latitude": "latitude", "longitude": "longitude", "location_type": "location_type", "conflict_date": "conflict_date", "total_number_IDPs": "population"})

    # get site names as list
    site_names_34 = dtm_df_34["#name"].tolist()
    site_ids_34 = dtm_df_34["site_id"].tolist()

    print(f"Round number: {round_number}")
    print(f"Total number of IDPs: {total_IDP_conflict_number}")
    print(f"Site names: {site_names_34}")
    print(f"Site ids: {site_ids_34}")
    print(dtm_df_34) 

    print(100*"-")

    # take this sites as baseline for the other rounds
    round_numbers = [33, 32]
    dtm_merged_df = dtm_df_34
    dtm_merged_df = dtm_merged_df.rename(columns={"population": f"population_round_{round_number}"})

    for round_number in round_numbers:
        test_file = os.path.join(paths_dtm, f"DTM Ethiopia - Site Assessment Round {round_number}.xlsx")

        # extract information from excel files
        file_path = os.path.join(paths_dtm, test_file)
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
    """
    """
        DISCLAIMER:
        In the Excel file for round 34 there is just given the main reason for displacement (1.5.e.1: Reason for displacement) and the total number of IDPs (2.1.b.7: Total Number of IDP Individuals) in the camp. This file is our baseline since it contains the most recent data.
        For the other rounds, the Excel files contain the total number of IDPs (2.1.b.7: Total Number of IDP Individuals) in the camp, the "Most reported reason for displacement in the site" and then split by the different reasons: among others "Reason for Displacement (Individuals): Conflict", "Reason for Displacement (Individuals): Drought"
        The problem is that for example in round 34 the main reason is conflict and the total number of IDPs is 15595. But in round 33 the most reported reason is drought and the total number of IDPs is 17169, split by 0 IDPs for conflict and 17169 IDPs for drought. 
        """
    """
        if (round_number == 32 or round_number == 33):
            dtm_df = dtm_df[["1.1.a.1: Survey Date", "Country", "1.1.a.2: Survey Round", "1.1.c.1: Site ID", "1.1.d.1: Site Name", "1.1.f.1: GPS: Longitude", "1.1.f.2: GPS: Latitude", "1.1.e.1: Region", "Most reported reason for displacement in the site", "Site Classification", "1.3.b.1: Settlement/site type", "2.1.b.7: Total Number of IDP Individuals", "Reason for Displacement (Individuals): Conflict"]]
            # rename columns
            dtm_df = dtm_df.rename(columns={"1.1.a.1: Survey Date": "survey_date", "Country": "country", "1.1.a.2: Survey Round": "survey_round", "1.1.c.1: Site ID": "site_id", "1.1.d.1: Site Name": "site_name", "1.1.f.1: GPS: Longitude": "longitude", "1.1.f.2: GPS: Latitude": "latitude", "1.1.e.1: Region": "region", "Most reported reason for displacement in the site": "main_reason_for_displacement", "Site Classification": "site_classification", "1.3.b.1: Settlement/site type": "settlement_type", "2.1.b.7: Total Number of IDP Individuals": "total_number_IDPs", "Reason for Displacement (Individuals): Conflict": "number_IDPs_conflict"})
        else: 
            print("Not possible to extract information for this round_number due to incompatibility of data formats!")


        if round_number == 33:
            # drop first row and reset index
            dtm_df = dtm_df.drop([0])
            dtm_df = dtm_df.reset_index(drop=True)

        if (round_number == 32 or round_number == 33):
            # Replace non-finite values with zero
            dtm_df["number_IDPs_conflict"] = dtm_df["number_IDPs_conflict"].replace([np.inf, -np.inf, np.nan], 0)
            # convert number_IDPs_conflict to int
            dtm_df["number_IDPs_conflict"] = dtm_df["number_IDPs_conflict"].astype(int)
        else: 
            print("Not possible to extract information for this round_number due to incompatibility of data formats!")

        # sum of column Reason for Displacement (Individuals): Conflict
        total_IDP_conflict_number = dtm_df["number_IDPs_conflict"].sum()

        # keep only the sites from site_ids_34
        dtm_df = dtm_df[dtm_df["site_id"].isin(site_ids_34)]


        # delete columns and change order to match locations.csv. Add location_type and conflict_date
        dtm_df["location_type"] = "idpcamp"
        dtm_df["conflict_date"] = 0
        # number_IDPs_conflict for each camp (additionally there could be other reasons why IDPs flee. We just focus on conflicts)
        dtm_df = dtm_df[['site_id', 'site_name', 'region', 'country', 'latitude', 'longitude', 'location_type', 'conflict_date', 'number_IDPs_conflict']]

        # Rename the columns
        dtm_df = dtm_df.rename(columns={"site_id": "site_id", "site_name": "#name", "region": "region", "country": "country", "latitude": "latitude", "longitude": "longitude", "location_type": "location_type", "conflict_date": "conflict_date", "number_IDPs_conflict": "population"})

        dtm_df_premerged = dtm_df[['site_id', 'latitude', 'longitude', 'population']]
        dtm_df_premerged = dtm_df_premerged.rename(columns={"site_id": "site_id", "latitude": "latitude", "longitude": "longitude", "population": f"population_round_{round_number}"})
        
        # print(f"Round number: {round_number}")
        # print(dtm_df)  

        # check if column latitude and longitude is in dtm_merged_df. Then drop
        if "latitude" in dtm_merged_df.columns:
            # drop column in dtm_df_premerged
            dtm_df_premerged = dtm_df_premerged.drop(columns=["latitude", "longitude"])


        dtm_merged_df = pd.merge(dtm_merged_df, dtm_df_premerged, on="site_id", how="left")
        print(f"Round number: {round_number}")
        print("dtm_merged_df:")
        print(dtm_merged_df)
        """
        





    "##########################################################################################################"
    """
    round_numbers = [34, 33, 32]

    for round_number in round_numbers:
        test_file = os.path.join(paths_dtm, f"DTM Ethiopia - Site Assessment Round {round_number}.xlsx")

        # extract information from excel files
        file_path = os.path.join(paths_dtm, test_file)
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
            dtm_df_34 = dtm_df_34[["1.1.a.1: Survey Date", "Country", "1.1.a.2: Survey Round", "1.1.c.1: Site ID", "1.1.d.1: Site Name", "1.1.e.1: Region", "1.5.e.1: Reason for displacement", "xxxx: Site Classification", "1.3.b.1: Settlement/site type", "2.1.b.7: Total Number of IDP Individuals"]]
            # rename columns
            dtm_df_34 = dtm_df_34.rename(columns={"1.1.a.1: Survey Date": "survey_date", "Country": "country", "1.1.a.2: Survey Round": "survey_round", "1.1.c.1: Site ID": "site_id", "1.1.d.1: Site Name": "site_name", "1.1.e.1: Region": "region", "1.5.e.1: Reason for displacement" : "reason_for_displacement", "xxxx: Site Classification": "site_classification", "1.3.b.1: Settlement/site type": "settlement_type", "2.1.b.7: Total Number of IDP Individuals": "total_number_IDPs"})
        else: 
            print("Not possible to extract information for this round_number due to incompatibility of data formats!")


        if round_number == 33:
            # drop first row and reset index
            dtm_df = dtm_df.drop([0])
            dtm_df = dtm_df.reset_index(drop=True)

        if (round_number == 32 or round_number == 33):
            # Replace non-finite values with zero
            dtm_df["number_IDPs_conflict"] = dtm_df["number_IDPs_conflict"].replace([np.inf, -np.inf, np.nan], 0)
            # convert number_IDPs_conflict to int
            dtm_df["number_IDPs_conflict"] = dtm_df["number_IDPs_conflict"].astype(int)
        elif round_number == 34:
            # Replace non-finite values with zero
            dtm_df_34["total_number_IDPs"] = dtm_df_34["total_number_IDPs"].replace([np.inf, -np.inf, np.nan], 0)
            # convert total_number_IDPs to int
            dtm_df_34["total_number_IDPs"] = dtm_df_34["total_number_IDPs"].astype(int)
        else: 
            print("Not possible to extract information for this round_number due to incompatibility of data formats!")

        # TODO: check if site_id unique



        # sum of column Reason for Displacement (Individuals): Conflict
        total_IDP_conflict_number = dtm_df_34.loc[dtm_df_34["reason_for_displacement"] == "Conflict", "total_number_IDPs"].sum()
        print(total_IDP_conflict_number)


        # Keep only the rows with settlement_type: Spontaneous camp/site or Planned camp/site
        dtm_df_34 = dtm_df_34.loc[(dtm_df_34["settlement_type"] == "Spontaneous camp/site") | (dtm_df_34["settlement_type"] == "Planned camp/site")]
        
        # sort by number_IDPs_conflict
        dtm_df_34.sort_values(by="total_number_IDPs", ascending=False, inplace=True)
        dtm_df_34 = dtm_df_34.reset_index(drop=True)

        # just keep top rows_shown entries
        dtm_df_34 = dtm_df_34.head(rows_shown)

        # delete columns and change order to match locations.csv. Add location_type and conflict_date
        dtm_df_34["location_type"] = "idpcamp"
        dtm_df_34["conflict_date"] = 0
        # number_IDPs_conflict for each camp (additionally there could be other reasons why IDPs flee. We just focus on conflicts)
        dtm_df_34 = dtm_df_34[['site_name', 'region', 'country', 'location_type', 'conflict_date', 'total_number_IDPs']]

        # rename to: name,region,country,latitude,longitude,location_type,conflict_date,population
        # Rename the columns
        dtm_df_34 = dtm_df_34.rename(columns={"site_name": "#name", "region": "region", "country": "country", "latitude": "latitude", "longitude": "longitude", "location_type": "location_type", "conflict_date": "conflict_date", "total_number_IDPs": "population"})

        print(f"Round number: {round_number}")
        print(dtm_df_34)   
    """

    "##########################################################################################################"


    """
        # TODO: check if site_id unique

        # sum of column Reason for Displacement (Individuals): Conflict
        total_IDP_conflict_number = dtm_df["number_IDPs_conflict"].sum()

        # Keep only the rows with settlement_type: Spontaneous camp/site or Planned camp/site
        dtm_df = dtm_df.loc[(dtm_df["settlement_type"] == "Spontaneous camp/site") | (dtm_df["settlement_type"] == "Planned camp/site")]
        
        # sort by number_IDPs_conflict
        dtm_df.sort_values(by="number_IDPs_conflict", ascending=False, inplace=True)
        dtm_df = dtm_df.reset_index(drop=True)

        # just keep top rows_shown entries
        dtm_df = dtm_df.head(rows_shown)

        # delete columns and change order to match locations.csv. Add location_type and conflict_date
        dtm_df["location_type"] = "idpcamp"
        dtm_df["conflict_date"] = 0
        # number_IDPs_conflict for each camp (additionally there could be other reasons why IDPs flee. We just focus on conflicts)
        dtm_df = dtm_df[['site_name', 'region', 'country', 'latitude', 'longitude', 'location_type', 'conflict_date', 'number_IDPs_conflict']]

        # rename to: name,region,country,latitude,longitude,location_type,conflict_date,population
        # Rename the columns
        dtm_df = dtm_df.rename(columns={"site_name": "#name", "region": "region", "country": "country", "latitude": "latitude", "longitude": "longitude", "location_type": "location_type", "conflict_date": "conflict_date", "number_IDPs_conflict": "population"})

        print(f"Round number: {round_number}")
        print(dtm_df)    
    """

     




    # Keep only the rows with settlement_type: Spontaneous camp/site or Planned camp/site
    # dtm_df = dtm_df.loc[(dtm_df["settlement_type"] == "Spontaneous camp/site") | (dtm_df["settlement_type"] == "Planned camp/site")]
    















    """
    # camp data (manually added from https://reliefweb.int/report/ethiopia/ethiopia-refugee-population-camp-site-and-settlement-31-may-2023)
    # gps data: https://www.gpskoordinaten.de/

    camps =[['Melkadida', 'Somali', 'Ethiopia', 4.5277801, 41.7250996, 'camp', 0, 41804],
            ['Bokolmanyo', 'Somali', 'Ethiopia', 4.5316201, 41.5369015, 'camp', 0, 32265],
            ['Kobe', 'Somali', 'Ethiopia', 4.4831533, 41.7564201, 'camp', 0, 37527],
            ['Helaweyn', 'Somali', 'Ethiopia', 4.3665831, 41.8593599, 'camp', 0, 48947],
            ['Bu
            ramino', 'Somali', 'Ethiopia', 4.3007472, 41.9337459, 'camp', 0, 47274],
            ['Sheder', 'Somali', 'Ethiopia', 9.7020584, 43.1315085, 'camp', 0, 14599],
            ['Aw-barre', 'Somali', 'Ethiopia', 9.7834822, 43.2239854, 'camp', 0, 13262],
            ['Kebribeyah', 'Somali', 'Ethiopia', 9.099511, 43.1738871, 'camp', 0, 17846],

            ['Okugo', 'Gambela', 'Ethiopia', 6.4901358, 35.1289466, 'camp', 0, 13769],
            ['Pinyudo', 'Gambela', 'Ethiopia', 7.6470239, 34.2572333, 'camp', 0, 51119],
            #['Pinyudo 2', 'Gambela', 'Ethiopia', '', '', 'camp', 0, 11368],
            ['Kule', 'Gambela', 'Ethiopia', 8.3032636, 34.2609099, 'camp', 0, 52914],
            # ['Nguenyiel', 'Gambela', 'Ethiopia', '', '', 'camp', 0, 11958], # not found
            ['Tierkidi', 'Gambela', 'Ethiopia', 8.2765403, 34.2918179, 'camp', 0, 72448],
            ['Jewi', 'Gambela', 'Ethiopia', 8.1410307, 34.7145155, 'camp', 0, 67903],

            ['Sherkole', 'Benshangul/Gumuz', 'Ethiopia', 10.666669845581055, 34.83332824707031, 'camp', 0, 13540],
            ['Tsore', 'Benshangul/Gumuz', 'Ethiopia', 10.2363348, 34.6146235, 'camp', 0, 43230],
            ['Bambasi', 'Benshangul/Gumuz', 'Ethiopia', 9.7604225,34.7298772, 'camp', 0, 20336],

            ['Barahle', 'Afar', 'Ethiopia', 13.8629006, 40.0214271, 'camp', 0, 28616],
            ['Serdo', 'Afar', 'Ethiopia', 11.95866,41.30781, 'camp', 0, 3324],
            ['Aysaita', 'Afar', 'Ethiopia', 11.5746575,41.4355373, 'camp', 0, 28754],
            ]


    # open locations.csv and add camps in the following structures:
    # name,country,latitude,longitude,location_type,conflict_date,population

    # Get the current directory
    current_dir = os.getcwd()
    #open locations.csv
    locations_file = os.path.join(current_dir, folder_name, "locations.csv")
    # write in locations.csv
    with open(locations_file, 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(camps)
    
    print("Successfully added camp locations to locations.csv")
    """
