# parser.py

import csv
from helpers import find_partial_match, array_to_dict, reverse_dict

class DataParser:
    def __init__(self):
        self.distances = {}
        self.locations = []
        self.map_locations = {}
        self.map_locations_reverse = {}
        self.packages = []

    def parse_distance_table(self, file_path):
        with open(file_path, mode='r') as file:
            reader = csv.reader(file)
            self.locations = next(reader)[1:]  # Skip the first column header
            self.map_locations = array_to_dict(self.locations)
            self.map_locations_reverse = reverse_dict(self.map_locations)
            for row in reader:
                location = self.map_locations_reverse[row[0]]
                try:
                    self.distances[location] = {self.map_locations_reverse[self.locations[i]]: float(row[i + 1]) for i in range(len(self.locations)) if row[i + 1] and row[i + 1].replace('.', '', 1).isdigit()}
                except ValueError:
                    continue

    def parse_package_file(self, file_path):
        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                location_lookup = find_partial_match(self.locations, row['Address'])
                location = self.map_locations_reverse[location_lookup] if location_lookup else None
                info = {
                    'PID': row['PID'],
                    'Destination': location,
                    'Deadline': row['Deadline'],
                    'Zip': row['Zip'],
                    'Notes': row['Notes']
                }
                self.packages.append(info)