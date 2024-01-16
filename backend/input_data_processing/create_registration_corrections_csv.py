import os 
import csv

def create_empty_registration_corrections_csv(folder_name):
    '''
    Create empty registration_corrections.csv
        Parameters:
            folder_name (str): Name of the folder where the file will be saved
            '''
    # Get the current directory
    current_dir = os.getcwd()
    #open locations.csv
    closures_file = os.path.join(current_dir, folder_name, "registration_corrections.csv")

    # write in closures_file.csv
    with open(closures_file, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
    
    print(f'{folder_name}/registration_corrections.csv created.')


    

