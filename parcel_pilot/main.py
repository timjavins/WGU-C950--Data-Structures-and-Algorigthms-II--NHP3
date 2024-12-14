# main.py

from data.parser import DataParser
from router.package_handler import link_packages, group_linked_packages
from simulator.interface import TimeSimulatorUI
from data.trucks import Truck
import tkinter as tk
from datetime import datetime, timedelta

# Create an instance of DataParser
data_parser = DataParser()

# Parse the data files
data_parser.parse_distance_table('inputs/WGUPS Distance Table.csv')
data_parser.parse_package_file('inputs/WGUPS Package File.csv')

# Access the parsed data
distances = data_parser.distances
locations = data_parser.locations
map_locations = data_parser.map_locations
map_locations_reverse = data_parser.map_locations_reverse
packages = data_parser.packages

# Process the packages
linked_packages = link_packages(packages)
grouped_packages = group_linked_packages(linked_packages)

print("Locations:", map_locations)
print()
print("Packages:", packages)
print()
print("Distances:", distances)
print()
print("Grouped Packages:", grouped_packages)
print()

# Create three trucks
truck_0 = Truck(0)
truck_1 = Truck(1)
truck_2 = Truck(2)

# Initialize and run the UI
def main():
    root = tk.Tk()
    app = TimeSimulatorUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()