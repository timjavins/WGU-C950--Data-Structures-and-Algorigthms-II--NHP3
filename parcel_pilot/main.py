# main.py

from data.parser import DataParser
from router.package_handler import link_packages, group_linked_packages
from simulator.interface import TimeSimulatorUI, InfoDisplayUI
from data.trucks import TruckManager
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

# Create a TruckManager instance
truck_manager = TruckManager()

# Get trucks using the manager
truck_0 = truck_manager.get_truck(0)
truck_1 = truck_manager.get_truck(1)
truck_2 = truck_manager.get_truck(2)

# Function to center a window on the screen
def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')

# Initialize and run the UI
def main():
    root = tk.Tk()
    time_simulator_root = tk.Toplevel()
    # Create the UI instances
    timer = TimeSimulatorUI(time_simulator_root)
    dashboard = InfoDisplayUI(root, timer, packages, [truck_0, truck_1, truck_2])
    # Center the InfoDisplayUI window
    root.update_idletasks()
    center_window(root, root.winfo_width(), root.winfo_height())
    # Position the TimeSimulatorUI window immediately beneath the InfoDisplayUI window
    def position_time_simulator():
        _ = time_simulator_root
        x = screen_width = _.winfo_screenwidth() // 2 - _.winfo_width() // 2
        root_y = root.winfo_y() - _.winfo_height() - 30
        time_simulator_root.update_idletasks()
        time_simulator_root.geometry(f'+{x}+{root_y}')
    # Schedule the positioning of the TimeSimulatorUI window
    root.after(1, position_time_simulator)    
    # Run the main loop
    root.mainloop()

if __name__ == "__main__":
    main()