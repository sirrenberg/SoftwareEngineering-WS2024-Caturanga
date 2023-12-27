import datetime

# Function to calculate the number of days between two dates in "dd-mm-yyyy" format
def between_date(d1, d2):
    d1list = d1.split("-")
    d2list = d2.split("-")
    date1 = datetime.datetime(int(d1list[2]), int(d1list[1]), int(d1list[0]))
    date2 = datetime.datetime(int(d2list[2]), int(d2list[1]), int(d2list[0]))

    return abs((date1 - date2).days)

# Function to format "dd-mm-yyyy" into "yyyy-mm-dd" format
def date_format(in_date):
    if "-" in in_date:
        split_date = in_date.split("-")
    else:
        split_date = in_date.split(" ")

    out_date = str(split_date[2]) + "-" + str(split_date[1]) + "-" + str(split_date[0])
    return out_date



def create_sim_period_csv(folder_name, start_date, end_date):
    duration = between_date(start_date, end_date)

    formatted_start_date = date_format(start_date)

    # format: 
        # "StartDate", 'YYYY-MM-DD'
        # "Length", int
    with open(folder_name + "/sim_period.csv", "w") as csv_file:
        csv_file.write('"StartDate","' + formatted_start_date + '"\n')
        csv_file.write('"Length",' + str(duration) + '\n')
    
        print(f'{folder_name}/sim_period.csv created.')







