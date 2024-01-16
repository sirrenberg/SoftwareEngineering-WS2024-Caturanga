import csv
import math
import networkx as nx
import os

# FabFlee used the euclidian distance in its implementation. 
# I use the haversine formula to calculate the linear distance between 2 locations in km
def haversine_distance(lat1, lon1, lat2, lon2):
    """
    This function calculates the distance between two locations on Earth using the Haversine formula.
    The function takes the latitude and longitude of the two locations as parameters and returns the distance in km.
        Parameters:
            lat1 (float): Latitude of the first location
            lon1 (float): Longitude of the first location
            lat2 (float): Latitude of the second location
            lon2 (float): Longitude of the second location
        Returns:
            distance (float): Distance between the two locations in km
    """
    # mean radius of the Earth
    R = 6371.0 # https://en.wikipedia.org/wiki/Great-circle_distance
    
    # Conversion from degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    # Deltas of the coordinates
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    # Haversine formula
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    # calculation of the distance
    distance = R * c
    # round to 2 decimals
    return round(distance, 2)


def extract_routes_csv(folder_name, top=3):
    """
    Extract the routes.csv file for the specified country.
    The function processes location data to generate a set of routes between locations.
        Parameters:
            folder_name (str): Name of the folder with the data.
            top (int): Number of routes to find for each location.
    """
    # Get the current directory
    current_dir = os.getcwd()
    # Get the locations file
    locations_file = os.path.join(current_dir, folder_name, "locations.csv")
    # Read CSV file and create a graph
    locations = []
    with open(locations_file, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            locations.append({
                'name': row['#name'],
                'latitude': float(row['latitude']),
                'longitude': float(row['longitude'])
            })

    G = nx.Graph() # empty graph
    # add all nodes and edges. The distance between the locations is the weight of the path/edge
    for i in range(len(locations)):
        for j in range(i + 1, len(locations)):
            distance = haversine_distance(locations[i]['latitude'], locations[i]['longitude'],
                                locations[j]['latitude'], locations[j]['longitude'])
            G.add_edge(locations[i]['name'], locations[j]['name'], weight=distance) 
        

    # Function to find the shortest paths for each node
    def find_shortest_paths(graph, node, top=3):
        paths = []
        for target_node in graph.nodes():
            if target_node != node:
                # with dijkstra find shortest paths with distance
                path = nx.shortest_path(graph, source=node, target=target_node, weight='weight')
                distance = nx.shortest_path_length(graph, source=node, target=target_node, weight='weight')
                paths.append({'target': target_node, 'path': path, 'distance': distance})
        return sorted(paths, key=lambda x: x['distance'])[:top] # for each location, just return the top shortest paths

    # calculate the top x shortest paths for each location
    shortest_paths = {}
    for location in locations:
        shortest_paths[location['name']] = find_shortest_paths(G, location['name'], top)
    
    # check if route already exists but with other direction. It should only be listed once.
    processed_routes = set() # no dublicates are allowed in a set

    # Write the results to a new CSV file
    with open(f'{folder_name}/routes.csv', 'w', newline='') as csvfile:
        fieldnames = ['name1', 'name2', 'distance', 'forced_redirection']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for source_node, paths in shortest_paths.items():
            for path in paths:
                target_node = path['target']
                # Check if the route or its reverse has already been processed
                if (source_node, target_node) not in processed_routes and (target_node, source_node) not in processed_routes:
                    writer.writerow({
                        'name1': source_node,
                        'name2': target_node,
                        'distance': path['distance'],
                        'forced_redirection': 0
                    })
                    # Add route to the set
                    processed_routes.add((source_node, target_node))
                    processed_routes.add((target_node, source_node))
    
