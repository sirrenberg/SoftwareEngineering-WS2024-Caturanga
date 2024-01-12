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
    date1 = datetime(int(d1list[2]), int(d1list[1]), int(d1list[0]))
    date2 = datetime(int(d2list[2]), int(d2list[1]), int(d2list[0]))

    return abs((date1 - date2).days)

