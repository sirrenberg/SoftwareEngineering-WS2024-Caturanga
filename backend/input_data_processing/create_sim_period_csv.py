import datetime
from helper_functions import date_format, between_date


def create_sim_period_csv(folder_name, start_date, simulation_end_date):
    '''
    Create sim_period.csv
        Parameters:
            folder_name (str): Name of the folder where the file will be saved
            start_date (str): Start date of the time period
            simulation_end_date (str): End date of the simulation
    '''

    duration = between_date(start_date, simulation_end_date)

    formatted_start_date = date_format(start_date)

    # format: 
        # "StartDate", 'YYYY-MM-DD'
        # "Length", int
    with open(folder_name + "/sim_period.csv", "w") as csv_file:
        csv_file.write('"StartDate","' + formatted_start_date + '"\n')
        csv_file.write('"Length",' + str(duration) + '\n')
    
        print(f'{folder_name}/sim_period.csv created.')