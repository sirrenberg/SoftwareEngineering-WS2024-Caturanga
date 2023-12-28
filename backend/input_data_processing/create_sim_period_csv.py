import datetime


def between_date(d1, d2):
    '''
    Function to calculate the number of days between two dates in "dd-mm-yyyy" format
        Parameters:
            d1 (str): First date in "dd-mm-yyyy" format
            d2 (str): Second date in "dd-mm-yyyy" format
        Returns:
            (int): Number of days between the two dates
    '''
    d1list = d1.split("-")
    d2list = d2.split("-")
    date1 = datetime.datetime(int(d1list[2]), int(d1list[1]), int(d1list[0]))
    date2 = datetime.datetime(int(d2list[2]), int(d2list[1]), int(d2list[0]))

    return abs((date1 - date2).days)


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



def create_sim_period_csv(folder_name, start_date, end_date):
    '''
    Create sim_period.csv
        Parameters:
            folder_name (str): Name of the folder containing the CSV files
            start_date (str): Start date of the time period
            end_date (str): End date of the time period
    '''

    duration = between_date(start_date, end_date)

    formatted_start_date = date_format(start_date)

    # format: 
        # "StartDate", 'YYYY-MM-DD'
        # "Length", int
    with open(folder_name + "/sim_period.csv", "w") as csv_file:
        csv_file.write('"StartDate","' + formatted_start_date + '"\n')
        csv_file.write('"Length",' + str(duration) + '\n')
    
        print(f'{folder_name}/sim_period.csv created.')







