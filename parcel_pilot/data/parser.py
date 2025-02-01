# parser.py

import csv
from data.package_hash import PackageHashTable
from helpers import find_partial_match, convert_to_24_hour_format, array_to_dict, reverse_dict
from data.packages import Package
from data.graph import Graph

class DataParser:
    def __init__(self):
        self.distances = {}
        self.locations = []
        self.map_locations = {}
        self.map_locations_reverse = {}
        self.packages = PackageHashTable()
        self.graph = None

    def parse_distance_table(self, file_path):
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