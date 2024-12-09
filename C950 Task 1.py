# Imports from Python Standard Library
import csv
from collections import defaultdict
import heapq
import re

### HELPER FUNCTIONS ###

def find_partial_match(locations, partial_string):
    """
    Finds a partial match in the locations array and returns the matched value.
    
    Parameters:
    locations (list): The list of location strings.
    partial_string (str): The partial string to search for.
    
    Returns:
    str: The matched value, otherwise None.
    """
    for location in locations:
        if partial_string.lower() in location.lower():
            return location
    return None

def array_to_dict(array):
    """
    Converts an array into a dictionary with integer-based keys starting from 0.
    
    Parameters:
    array (list): The input array to be converted into a dictionary.
    
    Returns:
    dict: A dictionary with integer keys and array elements as values.
    """
    return {i: array[i] for i in range(len(array))}

def reverse_dict(dictionary):
    """
    Reverses the keys and values of a dictionary.
    
    Parameters:
    dictionary (dict): The dictionary to reverse.
    
    Returns:
    dict: A new dictionary with keys and values swapped.
    """
    return {value: key for key, value in dictionary.items()}

### DATA PARSING ###

# Parse the WGUPS Distance Table
def parse_distance_table(file_path):
    distances = {}
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        locations = next(reader)[1:]  # Skip the first column header
        map_locations = array_to_dict(locations)
        map_locations_reverse = reverse_dict(map_locations)
        for row in reader:
            location = map_locations_reverse[row[0]]
            try:
                distances[location] = {map_locations_reverse[locations[i]]: float(row[i + 1]) for i in range(len(locations)) if row[i + 1] and row[i + 1].replace('.', '', 1).isdigit()}
            except ValueError:
                continue
    return distances, locations, map_locations, map_locations_reverse

# Parse the WGUPS Package File
def parse_package_file(file_path):
    packages = []
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            location_lookup = find_partial_match(locations, row['Address'])
            location = map_locations_reverse[location_lookup] if location_lookup else None
            info = {
                'PID': row['PID'],
                'Destination': location,
                'Deadline': row['Deadline'],
                'Zip': row['Zip'],
                'Notes': row['Notes']
            }
            packages.append(info)
    return packages

# Create the variables for the parsed data
distances, locations, map_locations, map_locations_reverse = parse_distance_table('WGUPS Distance Table.csv')
packages = parse_package_file('WGUPS Package File.csv')

print("Locations:", map_locations)
print()
print("Packages:", packages)
print()
print("Distances:", distances)
print()

### GRAPH REPRESENTATION ###

# class Graph:
#     def __init__(self):
#         self.edges = defaultdict(list)
#         self.weights = {}

#     def add_edge(self, from_node, to_node, weight):
#         self.edges[from_node].append(to_node)
#         self.edges[to_node].append(from_node)
#         self.weights[(from_node, to_node)] = weight
#         self.weights[(to_node, from_node)] = weight

# graph = Graph()
# for from_node, edges in distances.items():
#     for to_node, weight in edges.items():
#         graph.add_edge(from_node, to_node, weight)

# ### DIJKSTRA'S ALGORITHM WITH BINARY HEAP ###

# def dijkstra(graph, initial):
#     shortest_paths = {initial: (None, 0)}
#     priority_queue = [(0, initial)]
#     visited = set()

#     while priority_queue:
#         current_weight, current_node = heapq.heappop(priority_queue)
#         if current_node in visited:
#             continue
#         visited.add(current_node)
#         destinations = graph.edges[current_node]
#         weight_to_current_node = shortest_paths[current_node][1]

#         for next_node in destinations:
#             weight = graph.weights[(current_node, next_node)] + weight_to_current_node
#             if next_node not in shortest_paths or weight < shortest_paths[next_node][1]:
#                 shortest_paths[next_node] = (current_node, weight)
#                 heapq.heappush(priority_queue, (weight, next_node))

#     return shortest_paths

# ### PACKAGE DISTRIBUTION ###

# trucks = [0, 1, 2]
def link_packages(packages):
    linked_packages = {}
    for package in packages:
        if package['Notes'].startswith('Must be delivered with'):
            # extract the linked package IDs by looking for numbers in the notes via regex
            links = re.findall(r'\d+', package['Notes'])
            # add the PID to the list of linked packages
            if package['PID'] not in linked_packages:
                linked_packages[package['PID']] = links
    print("Linked Packages:", linked_packages)
    return linked_packages

def group_linked_packages(linked_packages):
    groups = []
    for key, values in linked_packages.items():
        # Create a new array with the key and each value inside the key's corresponding array
        new_group = [key] + values
        # If groups is empty, append the new group to groups
        if not groups:
            groups.append(new_group)
        else:
            # Check if any of the values in new_group are already in any existing group
            added_to_existing_group = False
            for group in groups:
                if any(item in group for item in new_group):
                    group.extend(item for item in new_group if item not in group)
                    added_to_existing_group = True
                    break
            # If the new group was not added to any existing group, append it as a new group
            if not added_to_existing_group:
                groups.append(new_group)
    print("Linked Package Groups:", groups)
    return groups

linked_packages = link_packages(packages)
packaged_groups = group_linked_packages(linked_packages)

# def get_delivery_route(graph, packages, start_location):
#     package_locations = {pkg['Delivery Address'] for pkg in packages}
#     shortest_paths = dijkstra(graph, start_location)
#     route = []
#     current_location = start_location

#     while package_locations:
#         next_location = min(package_locations, key=lambda loc: shortest_paths[loc][1])
#         route.append(next_location)
#         package_locations.remove(next_location)
#         current_location = next_location

#     return route

# start_location = 'Hub'  # Assuming 'Hub' is the starting location
# route = get_delivery_route(graph, packages, start_location)
# print("Delivery Route:", route)

# ### VALIDATION ###

# # Validate the total distance traveled
# def calculate_total_distance(route, graph):
#     total_distance = 0
#     for i in range(len(route) - 1):
#         total_distance += graph.weights[(route[i], route[i + 1])]
#     return total_distance

# total_distance = calculate_total_distance(route, graph)
# print("Total Distance Traveled:", total_distance)

# # Ensure the total distance is under 140 miles
# if total_distance <= 140:
#     print("The total distance traveled is within the limit.")
# else:
#     print("The total distance traveled exceeds the limit.")

# # 0 = "Western Governors University
# #     4001 South 700 East, 
# #     Salt Lake City, UT 84107"

# # 1 = "International Peace Gardens
# #  1060 Dalton Ave S"

# # 2 = "Sugar House Park
# #     1330 2100 S"

# # 3 = "Taylorsville-Bennion Heritage Gov Off
# #     1488 W 4800 S"

# # 4 = "Salt Lake City Division of Health Services
# #     177 W Price Ave"

# # 5 = "South Salt Lake Public Works
# #     195 W Oakland Ave"

# # 6 = "Salt Lake City Streets & Sanitation
# #     2010 W 500 S"

# # 7 = "Deker Lake
# #     2300 Parkway Blvd"

# # 8 = "Salt Lake City Ottinger Hall
# #     233 Canyon Rd"

# # 9 = "Columbus Library
# #     2530 S 500 E"

# # 10 = "Taylorsville City Hall
# #     2600 Taylorsville Blvd"

# # 11 = "South Salt Lake Police
# #     2835 Main St"

# # 12 = "Council Hall
# #     300 N State St"

# # 13 = "Redwood Park
# #     3060 Lester St"

# # 14 = "Salt Lake County Mental Health
# #     3148 S 1100 W"

# # 15 = "Salt Lake County/United Police Dept
# #     3365 S 900 W"

# # 16 = "West Valley Prosecutor
# #     3575 W Valley Central Sta bus Loop"

# # 17 = "Housing Auth. of Salt Lake County
# #     3595 Main St"

# # 18 = "Utah DMV Administrative Office
# #     380 W 2880 S"

# # 19 = "Third District Juvenile Court
# #     410 S State St"

# # 20 = "Cottonwood Regional Softball Complex
# #     4300 S 1300 E"

# # 21 = "Holidy City Office
# #     4580 S 2300 E"

# # 22 = "Murray City Museum
# #     5025 State St"

# # 23 = "Valley Regional Softball Complex
# #     5100 South 2700 West"

# # 24 = "City Center of Rock Springs
# #     5383 W 11800 S"

# # 25 = "Rice Terrace Pavilion Park
# #     600 E 900 South"

# # 26 = "Wheeler Historic Farm
# #     6351 S 900 E"