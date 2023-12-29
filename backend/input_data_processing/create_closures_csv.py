import os 
import csv

def create_empty_closure_csv(folder_name):
    '''
    Create empty closures.csv
        Parameters:
            folder_name (str): Name of the folder where the file will be saved
    '''
    # Get the current directory
    current_dir = os.getcwd()
    #open locations.csv
    closures_file = os.path.join(current_dir, folder_name, "closures.csv")

    # write in closures_file.csv
    with open(closures_file, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['#closure_type', 'name1', 'name2', 'closure_start', 'closure_end'])
    
    print(f'{folder_name}/closures.csv created.')


    

