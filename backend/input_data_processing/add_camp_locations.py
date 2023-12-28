import csv
import os

def add_camp_locations(folder_name):

    # camp data (manually added from https://reliefweb.int/report/ethiopia/ethiopia-refugee-population-camp-site-and-settlement-31-may-2023)
    # gps data: https://www.gpskoordinaten.de/

    camps =[['Melkadida', 'Somali', 'Ethiopia', 4.5277801, 41.7250996, 'camp', 0, 41804],
            ['Bokolmanyo', 'Somali', 'Ethiopia', 4.5316201, 41.5369015, 'camp', 0, 32265],
            ['Kobe', 'Somali', 'Ethiopia', 4.4831533, 41.7564201, 'camp', 0, 37527],
            ['Helaweyn', 'Somali', 'Ethiopia', 4.3665831, 41.8593599, 'camp', 0, 48947],
            ['Buramino', 'Somali', 'Ethiopia', 4.3007472, 41.9337459, 'camp', 0, 47274],
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
