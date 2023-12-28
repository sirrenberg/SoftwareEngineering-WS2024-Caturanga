# This script is based on https://github.com/djgroen/FabFlee/blob/master/scripts/05_extract_routes_csv.py 
# but changed where necessary to work automatically with the data from the ACLED API and the population data

"""
Input: 
- 'locations.csv': A CSV file containing geographical locations for a specific country or dataset. This file should include columns for 'name', 'latitude', and 'longitude' of each location.

Output: 
- 'routes.csv': A CSV file generated in the specified country's directory, containing the routes between locations. Each entry in the file includes the starting location ('name1'), the destination location ('name2'), the distance between these locations, and a placeholder for 'forced_redirection'.

Description:
This script, '05_extract_routes_csv.py', processes geographical location data to generate a set of routes between locations within a specified country or dataset. It uses a nearest neighbor approach, enhanced with the consideration of intermediate stops, to determine the most efficient routes based on Euclidean distance. 

The script functions as follows:
1. Reads location data from 'locations.csv' within a directory named after the specified country.
2. For each location, it finds the nearest neighbor and considers possible intermediate stops to optimize the route.
3. Records the routes, including the start and end locations and the calculated distances, in a 'routes.csv' file within the same country-specific directory.

Usage:
1. Prepare location data in 'locations.csv' with 'name', 'latitude', and 'longitude' columns.
2. Place this file within a directory named after the country or dataset.
3. Run the script with the country or dataset name as a command-line argument.
"""

import os 
import csv
import requests 
import pandas as pd
import numpy as np

def calculate_distance(lat1, lon1, lat2, lon2):
    return np.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2) * 1000

def find_nearest_neighbor(current_index, visited, locations_df):
    nearest_distance = float('inf')
    nearest_index = None
    for i in range(len(locations_df)):
        if not visited[i] and i != current_index:
            distance = calculate_distance(locations_df.iloc[current_index]['latitude'], locations_df.iloc[current_index]['longitude'],
                                          locations_df.iloc[i]['latitude'], locations_df.iloc[i]['longitude'])
            if distance < nearest_distance:
                nearest_distance = distance
                nearest_index = i
    return nearest_index, nearest_distance

def extract_routes_csv(country, folder_name):

    # Get the current directory
    current_dir = os.getcwd()

    # Get the locations file
    locations_file = os.path.join(current_dir, folder_name, "locations.csv")

    # Load the locations data from locations.csv into a DataFrame
    locations_df = pd.read_csv(locations_file)

    # Nearest Neighbor with Intermediate Stops
    visited = [False] * len(locations_df)
    route = [0]  # Start from the first location (index 0)
    visited[0] = True

    routes = []  # To store the routes and distances

    while not all(visited):
        current_index = route[-1]
        next_index, direct_distance = find_nearest_neighbor(current_index, visited, locations_df)

        # Check for possible intermediate stop
        for i in range(len(locations_df)):
            if not visited[i] and i != current_index and i != next_index:
                intermediate_distance = calculate_distance(locations_df.iloc[current_index]['latitude'], locations_df.iloc[current_index]['longitude'],
                                                           locations_df.iloc[i]['latitude'], locations_df.iloc[i]['longitude']) + \
                                        calculate_distance(locations_df.iloc[i]['latitude'], locations_df.iloc[i]['longitude'],
                                                           locations_df.iloc[next_index]['latitude'], locations_df.iloc[next_index]['longitude'])
                # If the route via the intermediate location is shorter, choose it
                if intermediate_distance < direct_distance:
                    next_index = i
                    direct_distance = intermediate_distance
                    break

        route.append(next_index)
        visited[next_index] = True
        routes.append([locations_df.iloc[current_index]['#name'], locations_df.iloc[next_index]['#name'], round(direct_distance, 2), 0])

    # Save the routes to a CSV file
    with open(f'{folder_name}/routes.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['name1', 'name2', 'distance', 'forced_redirection'])
        for route in routes:
            writer.writerow(route)

    print(f'{folder_name}/routes.csv created. Please inspect the file for unwanted anomalies!')
