from data.parser import DataParser
from router.package_handler import link_packages, group_linked_packages, prioritize_packages, intake_packages
from simulator.interface import TimeSimulatorUI, InfoDisplayUI, center_window, position_time_simulator, on_closing
from data.trucks import TruckManager
from router.distributor import Distributor
import tkinter as tk
from simulator.time_sim import precompute_simulation_states

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
intake_packages(packages, "08:00")
prioritize_packages(packages)
linked_packages = link_packages(packages)
grouped_packages = group_linked_packages(linked_packages, packages)

print("Locations:", map_locations)
print()
print("Packages:")
for package in packages:
    print(package)
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

# Distribute packages into trucks using the Distributor class
distributor = Distributor([truck_0, truck_1, truck_2])
distributor.distribute_packages(packages, grouped_packages)
simulation_states = precompute_simulation_states(packages, [
    truck_manager.get_truck(0),
    truck_manager.get_truck(1),
    truck_manager.get_truck(2)
    ]
)

# Initialize and run the UI
def main():
    root = tk.Tk() # Create the main window for the InfoDisplayUI
    sub_root = tk.Toplevel() # Create a sub window for the TimeSimulatorUI
    # Instantiate the user interface components
    timer = TimeSimulatorUI(sub_root, simulation_states)
    dashboard = InfoDisplayUI(root, timer, packages, [truck_0, truck_1, truck_2])
    # Center the InfoDisplayUI window
    root.update_idletasks()
    center_window(root, root.winfo_width(), root.winfo_height())
    # Ensure the InfoDisplayUI window's position and size are updated
    root.update_idletasks()
    # Position the TimeSimulatorUI window immediately beneath the InfoDisplayUI window
    position_time_simulator(root, sub_root)
    # Bind the close event to the on_closing function
    root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root, sub_root))
    sub_root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root, sub_root))
    # Run the main loop
    root.mainloop()

if __name__ == "__main__":
    main()