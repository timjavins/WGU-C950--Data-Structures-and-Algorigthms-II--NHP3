"""
This module contains the DataParser class for parsing CSV files and creating data structures for the package delivery simulation.

Classes
-------
DataParser
    A class that parses CSV files and creates data structures for the package delivery simulation.

Functions
---------
parse_distance_table(file_path)
    Parses the distance table CSV file and creates a graph representation of the delivery locations.

create_graph_from_distances()
    Creates a graph representation of the delivery locations based on the parsed distance table.

parse_package_file(file_path)
    Parses the package file CSV and inserts package data into the package hash table.
"""

import csv
from data.package_hash import PackageHashTable
from helpers import find_partial_match, convert_to_24_hour_format, array_to_dict, reverse_dict
from data.packages import Package
from data.graph import Graph

class DataParser:
    """
    A class that parses CSV files and creates data structures for the package delivery simulation.

    Attributes
    ----------
    distances : dict
        A dictionary containing distances between locations.
    locations : list
        A list of delivery locations.
    map_locations : dict
        A dictionary mapping location names to their indices.
    map_locations_reverse : dict
        A dictionary mapping indices to location names.
    packages : PackageHashTable
        A hash table for storing package data.
    graph : Graph
        A graph representation of the delivery locations.
    """

    def __init__(self):
        """
        Initializes the DataParser with empty data structures.
        """
        self.distances = {}
        self.locations = []
        self.map_locations = {}
        self.map_locations_reverse = {}
        self.packages = PackageHashTable()
        self.graph = None

    def parse_distance_table(self, file_path):
        """
        Parses the distance table CSV file and creates a graph representation of the delivery locations.

        Parameters
        ----------
        file_path : str
            The path to the distance table CSV file.

        Returns
        -------
        None

        Space Complexity
        ---------------
            O(n)

        Time Complexity
        ---------------
            O(n^2)
        """
        with open(file_path, mode='r') as file:
            reader = csv.reader(file)
            self.locations = next(reader)[1:]  # Skip the first column header
            self.map_locations = array_to_dict(self.locations)
            self.map_locations_reverse = reverse_dict(self.map_locations)
            for row in reader:
                location = self.map_locations_reverse[row[0]]
                try:
                    self.distances[location] = [
                        float(row[i + 1]) for i in range(len(self.locations))
                        if row[i + 1] and row[i + 1].replace('.', '', 1).isdigit()
                    ]
                except ValueError:
                    continue
        self.create_graph_from_distances()

    def create_graph_from_distances(self):
        """
        Creates a graph representation of the delivery locations based on the parsed distance table.

        Returns
        -------
        None

        Space Complexity
        ---------------
            O(n)

        Time Complexity
        ---------------
            O(n^2)
        """
        graph = Graph()
        for location, distances in self.distances.items():
            for i, distance in enumerate(distances):
                if distance or distance == 0.0:  # Include zero distances
                    neighbor = self.locations[i]
                    graph.add_edge(location, neighbor, distance)
                    # Ensure the neighbor node is also added to the graph
                    if neighbor not in graph.edges:
                        graph.add_edge(neighbor, location, distance)
        self.graph = graph
    
    def parse_package_file(self, file_path):
        """
        Parses the package file CSV and inserts package data into the package hash table.
    
        Parameters
        ----------
        file_path : str
            The path to the package file CSV.
    
        Returns
        -------
        None
    
        Space Complexity
        ---------------
            O(n)
    
        Time Complexity
        ---------------
            O(n)
        """
        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                location_lookup = find_partial_match(self.locations, row['Address'])
                location = self.map_locations_reverse[location_lookup] if location_lookup else None
                self.packages.insert(
                    row['PID'],
                    row['Address'],
                    row['City'],
                    row['State'],
                    row['Zip'],
                    convert_to_24_hour_format(row['Deadline']) if row['Deadline'] != "EOD" else "EOD",
                    row['Weight'],
                    'IN TRANSIT',
                    row['Notes']
                )
    
    def initialize_packages(self):
        """
        Initializes the packages from the package hash table.
    
        Returns
        -------
        list
            The list of initialized packages.
    
        Space Complexity
        ---------------
            O(n)
    
        Time Complexity
        ---------------
            O(n)
        """
        packages = []
        for pid in range(self.packages.size):
            # Ignore empty buckets in the hash table
            if self.packages.table[pid] is None:
                continue
            for package_data in self.packages.table[pid]:
                package = Package(
                    pid=package_data[0],
                    address=package_data[1],
                    city=package_data[2],
                    state=package_data[3],
                    zip_code=package_data[4],
                    deadline=package_data[5],
                    weight=package_data[6],
                    status=package_data[7],
                    notes=package_data[8]
                )
                try:
                    package.destination = self.map_locations_reverse[find_partial_match(self.locations, package.address)]
                except KeyError:
                    package.destination = None
                packages.append(package)
    
        return packages