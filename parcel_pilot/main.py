"""
The main Python file in the Parcel Pilot application orchestrates data parsing, object initialization, and user interface setup for simulating package delivery.

Functions
---------
main()
    Parses data, prepares simulation states, and runs the graphical user interface.
"""

from data.parser import DataParser
from router.package_handler import link_packages, group_linked_packages
from simulator.interface import ChooseAlgo, TimeSimulatorUI, InfoDisplayUI, center_window, position_time_simulator, on_closing
from data.trucks import TruckManager
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
graph = data_parser.graph
packages = data_parser.initialize_packages()

# Group the packages
linked_packages = link_packages(packages)
grouped_packages = group_linked_packages(linked_packages, packages)

# message box that allows the user to pick between Dijkstra's and Nearest Neighbor
# Create a custom dialog to choose the algorithm
# mbox = tk.Tk()
# mbox.withdraw()  # Hide the root window
# dialog = ChooseAlgo(mbox)
# algo = dialog.result if dialog.result else "nearest neighbor"
algo = "nearest neighbor"

# Create a TruckManager instance
truck_manager = TruckManager()

# Get trucks using the manager
truck_0 = truck_manager.get_truck(0)
truck_1 = truck_manager.get_truck(1)
truck_2 = truck_manager.get_truck(2)
trucks = [truck_0, truck_1, truck_2]

simulation_states = precompute_simulation_states(packages, trucks, distances, graph, algo)

# Initialize and run the UI
def main():
    """
    Sets up data parsing, simulation states, and the UI before running the main loop.

    Space Complexity
    ---------------
        O(n)

    Time Complexity
    ---------------
        O(n)
    """
    root = tk.Tk() # Create the main window for the InfoDisplayUI
    sub_root = tk.Toplevel() # Create a sub window for the TimeSimulatorUI
    # Instantiate the main user interface components
    time_simulator = TimeSimulatorUI(sub_root, simulation_states)
    dashboard = InfoDisplayUI(root, time_simulator, simulation_states)
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