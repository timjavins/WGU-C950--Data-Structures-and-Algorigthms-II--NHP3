"""
This module contains utility functions for managing the graphical user interface (GUI) of both the Parcel Pilot dashboard and the time simulation.

Functions
---------
center_window(window, width, height)
    Centers the given window on the screen based on the specified width and height.

position_time_simulator(root, sub_root)
    Positions the TimeSimulatorUI window immediately above the InfoDisplayUI window.

on_closing(root, sub_root)
    Closes both the root and sub_root windows when one window is closed.
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, font
from simulator.time_sim import calculate_time, calculate_minutes
import re

class ChooseAlgo(simpledialog.Dialog): # Currently bypassed
    """
    A dialog class for choosing between Dijkstra's algorithm and the Nearest Neighbor algorithm.

    Methods
    -------
    body(master)
        Creates the body of the dialog with a label.
    buttonbox()
        Creates the button box with options for Dijkstra's and Nearest Neighbor algorithms.
    use_dijkstra()
        Sets the result to "dijkstra" and closes the dialog.
    use_nearest_neighbor()
        Sets the result to "nearest neighbor" and closes the dialog.
    """

    def body(self, master):
        """
        Creates the body of the dialog with a label.

        Parameters
        ----------
        master : tk.Tk
            The master widget.

        Returns
        -------
        None
        """
        tk.Label(master, text="Choose Algorithm").grid(row=0, column=0, columnspan=2)
        return None

    def buttonbox(self):
        """
        Creates the button box with options for Dijkstra's and Nearest Neighbor algorithms.

        Returns
        -------
        None
        """
        box = tk.Frame(self)

        self.dijkstra_button = tk.Button(box, text="Dijkstra's", width=10, command=self.use_dijkstra)
        self.dijkstra_button.grid(row=0, column=0, padx=5, pady=5)

        self.nearest_neighbor_button = tk.Button(box, text="Nearest Neighbor", width=15, command=self.use_nearest_neighbor)
        self.nearest_neighbor_button.grid(row=0, column=1, padx=5, pady=5)

        box.pack()

    def use_dijkstra(self):
        """
        Sets the result to "dijkstra" and closes the dialog.

        Returns
        -------
        None
        """
        self.result = "dijkstra"
        self.destroy()

    def use_nearest_neighbor(self):
        """
        Sets the result to "nearest neighbor" and closes the dialog.

        Returns
        -------
        None
        """
        self.result = "nearest neighbor"
        self.destroy()

class InfoDisplayUI:
    """
    A class for displaying the state of packages and trucks in the simulation.

    Attributes
    ----------
    root : tk.Tk
        The root window of the Tkinter application.
    time_simulator : TimeSimulator
        The time simulator object.
    simulation_states : dict
        The dictionary containing simulation states for each minute.
    time_label : ttk.Label
        The label displaying the current time.
    package_frame : ttk.Frame
        The frame containing the package information display.
    package_tree : ttk.Treeview
        The tree view displaying package information.
    truck_frame : ttk.Frame
        The frame containing the truck information display.
    truck_tree : ttk.Treeview
        The tree view displaying truck information.
    summary_frame : ttk.Frame
        The frame containing the summary information display.
    progress_bar : ttk.Progressbar
        The progress bar showing the delivery progress.
    progress_label : ttk.Label
        The label displaying the delivery progress.
    on_time_percentage_label : ttk.Label
        The label displaying the on-time delivery percentage.
    total_miles_label : ttk.Label
        The label displaying the total miles traveled.
    score_label : ttk.Label
        The label displaying the score.
    """

    def __init__(self, root, time_simulator, simulation_states):
        """
        Initializes the InfoDisplayUI with the given root, time simulator, and simulation states.

        Parameters
        ----------
        root : tk.Tk
            The root window of the Tkinter application.
        time_simulator : TimeSimulator
            The time simulator object.
        simulation_states : dict
            The dictionary containing simulation states for each minute.
        """
        self.root = root
        self.time_simulator = time_simulator
        self.simulation_states = simulation_states
        self.root.title("Parcel Pilot Dashboard")

        # Set the callback mechanism for time updates
        self.time_simulator.set_time_update_callback(self.update_time)

        # Current time display
        self.time_label = ttk.Label(root, text="", font=("Helvetica", 16))
        self.time_label.pack(pady=10)

        # Package information display
        self.package_frame = ttk.Frame(root)
        self.package_frame.pack(fill='both', expand=True)
        self.package_tree = ttk.Treeview(self.package_frame, columns=("PID", "Status", "Delivery Time", "Deadline", "Timely", "Group", "Destination", "Location", "Truck", "Notes"), show="headings")
        self.package_tree.heading("PID", text="PID")
        self.package_tree.heading("Status", text="Status")
        self.package_tree.heading("Delivery Time", text="Delivery Time")
        self.package_tree.heading("Deadline", text="Deadline")
        self.package_tree.heading("Timely", text="Timely")
        self.package_tree.heading("Group", text="Group")
        self.package_tree.heading("Destination", text="Destination")
        self.package_tree.heading("Location", text="Location")
        self.package_tree.heading("Truck", text="Truck")
        self.package_tree.heading("Notes", text="Notes")
        self.package_tree.pack(fill='both', expand=True)
        
        # Truck information display
        self.truck_frame = ttk.Frame(root)
        self.truck_frame.pack(fill='both', expand=True, side=tk.LEFT)
        self.truck_tree = ttk.Treeview(self.truck_frame, columns=("Truck ID", "Packages", "Location", "Miles", "Road Time"), show="headings")
        self.truck_tree.heading("Truck ID", text="Truck ID")
        self.truck_tree.heading("Packages", text="Packages")
        self.truck_tree.heading("Location", text="Location")
        self.truck_tree.heading("Miles", text="Miles")
        self.truck_tree.heading("Road Time", text="Road Time")
        self.truck_tree.pack(fill='both', expand=True)

        # Summary information display
        self.summary_frame = ttk.Frame(root)
        self.summary_frame.pack(fill='both', expand=True, side=tk.RIGHT)
        self.progress_bar = ttk.Progressbar(self.summary_frame, orient='horizontal', length=200, mode='determinate')
        self.progress_bar.pack(pady=10)
        self.progress_label = ttk.Label(self.summary_frame, text="Progress: 0/0 packages delivered", font=("Helvetica", 14))
        self.progress_label.pack(pady=10)
        self.on_time_percentage_label = ttk.Label(self.summary_frame, text="On-Time Delivery: 0%", font=("Helvetica", 14))
        self.on_time_percentage_label.pack(pady=10)
        self.total_miles_label = ttk.Label(self.summary_frame, text="Total Miles: 0", font=("Helvetica", 14))
        self.total_miles_label.pack(pady=10)
        self.score_label = ttk.Label(self.summary_frame, text="Score: 0%", font=("Helvetica", 14))
        self.score_label.pack(pady=10)

        # Configure TKinter tags for alternating row colors in package_tree and truck_tree
        self.package_tree.tag_configure("oddrow", background="#ffffff") # white
        self.package_tree.tag_configure("evenrow", background="#f0f0ff") # light blue
        self.truck_tree.tag_configure("oddrow", background="#ffffff") # white
        self.truck_tree.tag_configure("evenrow", background="#f0f0ff") # light blue

        # Populate the information
        self.update_time()
        # Adjust column widths to fit content initially
        self.adjust_column_widths(self.package_tree)
        self.adjust_column_widths(self.truck_tree)

    def update_time(self):
        """
        Updates the current time display and the simulation state.

        Space Complexity
        ---------------
            O(1)

        Time Complexity
        ---------------
            O(n)
        """
        if not self.time_simulator.is_editing: # This should not run when the user is editing the time input
            simulation_state = None
            current_time = self.time_simulator.get_current_time()
            self.time_label.config(text=f"Current Time: {current_time}")
            simulation_state = self.time_simulator.get_simulation_state(current_time)
            if simulation_state:
                self.update_display(simulation_state)

    def update_display(self, simulation_state):
        """
        Updates the display with the given simulation state.
        
        Parameters
        ----------
        simulation_state : Minute
            The simulation state containing the states of packages and trucks.

        Space Complexity
        ---------------
            O(n)

        Time Complexity
        ---------------
            O(n)
        """
        # Clear the current display
        for item in self.package_tree.get_children():
            self.package_tree.delete(item)
        for item in self.truck_tree.get_children():
            self.truck_tree.delete(item)
        # Populate the package information
        self.populate_package_info(simulation_state.packages)
        # Populate the truck information
        self.populate_truck_info(simulation_state.trucks)
        # Update the summary information
        self.update_summary_info(simulation_state)

    def populate_package_info(self, package_hash):
        """
        Populates the package information display with the given package hash table.
        
        Parameters
        ----------
        package_hash : PackageHashTable
            The hash table containing package information.

        Space Complexity
        ---------------
            O(n)

        Time Complexity
        ---------------
            O(n)
        """
        indices = 0
        package_list = []
        for bucket in package_hash.table:
            if bucket is not None:
                for item in bucket:
                    package_list.append(item)
        # Sort the package list by pid
        package_list.sort(key=lambda x: int(x[0]))
        # item[0] is the PID
        # item[1:] holds address, city, state, zip_code, deadline, weight, status, etc.
        for item in package_list:
            pid = item[0]
            status = item[7]
            delivery_time = item[15]
            deadline = item[5]
            timely = item[16]
            group = item[12]
            destination = item[14]
            location = item[11]
            truck_id = item[10]
            notes = item[8]
            # mechanism for alternating row colors
            tag = 'evenrow' if indices % 2 == 0 else 'oddrow'
            self.package_tree.insert(
                "",
                "end",
                values=(pid, status, delivery_time, deadline, timely, group, destination, location, truck_id, notes),
                tags=(tag,)
            )
            indices += 1
    
    def populate_truck_info(self, truck_hash):
        """
        Populates the truck information display with the given truck hash table.
        
        Parameters
        ----------
        truck_hash : TruckHashTable
            The hash table containing truck information.

        Space Complexity
        ---------------
            O(n)

        Time Complexity
        ---------------
            O(n)
        """
        indices = 0
        truck_list = []
        for bucket in truck_hash.table:
            if bucket is not None:
                for item in bucket:
                    truck_list.append(item)
        
        # Sort the truck list by truck_id
        truck_list.sort(key=lambda x: int(x[0]))
    
        for item in truck_list:
            truck_id = item[0]
            truck_data = item[1]
            package_list = truck_data['packages']
            package_ids = ", ".join(str(pkg_id) for pkg_id in package_list)  # Directly use pkg_id
            total_time = self.format_time(truck_data['total_time']) # Convert total time to hours and minutes
            total_distance = round(truck_data['total_distance'], 2)  # Round the total distance to 2 decimal places
            # mechanism for alternating row colors
            tag = 'evenrow' if indices % 2 == 0 else 'oddrow'
            self.truck_tree.insert(
                "",
                "end",
                values=(
                    truck_id,
                    package_ids,
                    truck_data['current_location'],
                    total_distance,
                    total_time
                ),
                tags=(tag,)
            )
            indices += 1

    def update_summary_info(self, simulation_state):
        """
        Updates the summary information display with the given simulation state.
        
        Parameters
        ----------
        simulation_state : Minute
            The simulation state containing the states of packages and trucks.
    
        Space Complexity
        ---------------
            O(n)
    
        Time Complexity
        ---------------
            O(n)
        """
        total_miles = sum(truck_data['total_distance'] for bucket in simulation_state.trucks.table if bucket for truck_id, truck_data in bucket)
        total_miles = round(total_miles, 2)
        total_packages = sum(1 for package_list in simulation_state.packages.table if package_list for package in package_list)
        delivered_on_time = sum(1 for package_list in simulation_state.packages.table if package_list for package in package_list if package[16])
        total_delivered = sum(1 for package_list in simulation_state.packages.table if package_list for package in package_list if package[14] == package[11])
        on_time_percentage = (delivered_on_time / total_delivered * 100) if total_delivered > 0 else 0
        on_time_percentage = round(on_time_percentage, 2)
        score = round(((total_delivered + delivered_on_time) / (total_packages * 2) * 100), 2)
    
        self.score_label.config(text=f"Score: {score}%", width=20, anchor='w')
        self.on_time_percentage_label.config(text=f"On-Time Delivery: {on_time_percentage:.2f}%", width=22, anchor='w')
        self.progress_label.config(text=f"Progress: {total_delivered}/{total_packages} packages delivered", width=30, anchor='w')
        self.total_miles_label.config(text=f"Total Miles: {total_miles}", width=20, anchor='w')
        # progress bar
        self.progress_bar.config(length=300)
        self.progress_bar['value'] = total_delivered / total_packages * 100
    
        # Ensure labels are aligned to the left with padding
        self.score_label.pack(anchor='w', padx=10)
        self.on_time_percentage_label.pack(anchor='w', padx=10)
        self.progress_label.pack(anchor='w', padx=10)
        self.total_miles_label.pack(anchor='w', padx=10)
        self.progress_bar.pack(anchor='w', padx=10)

    def adjust_column_widths(self, tree):
        """
        Adjusts the column widths of the given tree view to fit the content.

        Parameters
        ----------
        tree : ttk.Treeview
            The tree view whose column widths need to be adjusted.

        Space Complexity
        ---------------
            O(n)

        Time Complexity
        ---------------
            O(n)
        """
        for col in tree["columns"]:
            max_width = font.Font().measure(col)
            for item in tree.get_children():
                item_text = tree.item(item, "values")[tree["columns"].index(col)]
                max_width = max(max_width, font.Font().measure(item_text))
            tree.column(col, width=max_width)
    
    def format_time(self, minutes):
        """
        Converts the given time in minutes to a string in hours and minutes format.

        Parameters
        ----------
        minutes : int
            The time in minutes.

        Returns
        -------
        str
            The formatted time string in hours and minutes.

        Space Complexity
        ---------------
            O(1)

        Time Complexity
        ---------------
            O(1)
        """
        hours = minutes // 60
        minutes = minutes % 60
        return f"{hours} hr, {minutes} min"

class TimeSimulatorUI:
    """
    A class for simulating and displaying time-based events in the package delivery system.

    Attributes
    ----------
    root : tk.Tk
        The root window of the Tkinter application.
    is_editing : bool
        Flag to track if the user is editing the time input.
    time_update_callback : function
        Instance variable to store the callback function for time updates.
    simulation_states : dict
        The dictionary containing precomputed simulation states for each minute.
    slider : ttk.Scale
        The slider for selecting the time in minutes.
    time_var : tk.StringVar
        The variable for storing the current time as a string.
    time_input : ttk.Entry
        The entry widget for displaying and editing the current time.
    """

    def __init__(self, root, simulation_states):
        """
        Initializes the TimeSimulatorUI with the given root and simulation states.

        Parameters
        ----------
        root : tk.Tk
            The root window of the Tkinter application.
        simulation_states : dict
            The dictionary containing precomputed simulation states for each minute.
        """
        self.root = root
        self.root.title("Time Simulator")
        self.is_editing = False  # Flag to track if the user is editing the time input
        self.time_update_callback = None  # Instance variable to store the callback function
        self.simulation_states = simulation_states  # Store the precomputed simulation states

        # Slider
        self.slider = ttk.Scale(root, from_=0, to=540, orient='horizontal', length=540, command=self.update_time)
        self.slider.pack(pady=1)

        # Time Input/Display
        self.time_var = tk.StringVar()
        self.time_input = ttk.Entry(root, textvariable=self.time_var, font=("Helvetica", 16), width=5)
        self.time_input.pack(pady=1, anchor='center')
        self.time_input.bind("<FocusIn>", self.on_focus_in)
        self.time_input.bind("<FocusOut>", self.on_focus_out)
        self.time_input.bind("<Return>", self.on_enter)

        # Initialize the display
        self.update_time(0)

    def set_time_update_callback(self, callback):
        """
        Sets the callback function for time updates.

        Parameters
        ----------
        callback : function
            The callback function to be called on time updates.

        Returns
        -------
        None
        """
        self.time_update_callback = callback

    def update_time(self, value):
        """
        Updates the current time display based on the slider value.

        Parameters
        ----------
        value : float
            The value of the slider representing the number of minutes passed since 08:00 AM.

        Returns
        -------
        None

        Space Complexity
        ---------------
            O(1)

        Time Complexity
        ---------------
            O(1)
        """
        minutes_passed = int(float(value))
        current_time, _ = calculate_time(minutes_passed)
        self.time_var.set(current_time)
        if self.time_update_callback:
            self.time_update_callback()  # Send the new time to other methods

    def get_current_time(self):
        """
        Gets the current time from the time input.

        Returns
        -------
        str
            The current time in 24-hour format (HH:MM).

        Space Complexity
        ---------------
            O(1)

        Time Complexity
        ---------------
            O(1)
        """
        return self.time_var.get()

    def on_focus_in(self, event):
        """
        Handles the focus-in event for the time input.

        Parameters
        ----------
        event : tk.Event
            The event object.

        Returns
        -------
        None
        """
        self.is_editing = True  # Set flag to True when editing starts
        self.time_input.selection_range(0, tk.END)

    def on_focus_out(self, event):
        """
        Handles the focus-out event for the time input.

        Parameters
        ----------
        event : tk.Event
            The event object.

        Returns
        -------
        None
        """
        self.validate_and_update_time()

    def on_enter(self, event):
        """
        Handles the enter key event for the time input.

        Parameters
        ----------
        event : tk.Event
            The event object.

        Returns
        -------
        None
        """
        self.validate_and_update_time()

    def validate_and_update_time(self):
        """
        Validates and updates the time input.

        Returns
        -------
        None

        Space Complexity
        ---------------
            O(1)

        Time Complexity
        ---------------
            O(1)
        """
        time_str = self.time_input.get()
        # Validate the input format
        if re.match(r'^\d{4}$', time_str) or re.match(r'^\d{2}:\d{2}$', time_str):
            minutes_passed = calculate_minutes(time_str)
            # Check if the time is within the valid range (08:00 to 17:00)
            if 0 <= minutes_passed <= 540:
                self.slider.set(minutes_passed)
                self.update_time(minutes_passed)
            else:
                messagebox.showerror("Invalid Input", "Please enter a 24-hour time between 08:00 and 17:00.")
                self.update_time(self.slider.get())
        else:
            messagebox.showerror("Invalid Input", "Please enter a 24-hour time in HHMM or HH:MM format.")
            self.update_time(self.slider.get())
        self.is_editing = False  # Set flag back to False when editing ends
        if self.time_update_callback:
            self.time_update_callback()  # Send the new time to other functions

    def get_simulation_state(self, time_str):
        """
        Gets the precomputed simulation state for the given time.

        Parameters
        ----------
        time_str : str
            The time in 24-hour format (HH:MM).

        Returns
        -------
        dict
            The simulation state for the given time.

        Space Complexity
        ---------------
            O(1)

        Time Complexity
        ---------------
            O(1)
        """
        return self.simulation_states.get(time_str)

def center_window(window, width, height):
    """
    Centers the given window on the screen based on the specified width and height.

    Parameters
    ----------
    window : tk.Tk or tk.Toplevel
        The window to be centered.
    width : int
        The width of the window.
    height : int
        The height of the window.

    Space Complexity
    ---------------
        O(1)

    Time Complexity
    ---------------
        O(1)
    """
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')

def position_time_simulator(root, sub_root):
    """
    Positions the TimeSimulatorUI window immediately above the InfoDisplayUI window.

    Parameters
    ----------
    root : tk.Tk
        The root window of the InfoDisplayUI.
    sub_root : tk.Toplevel
        The sub window of the TimeSimulatorUI.

    Space Complexity
    ---------------
        O(1)

    Time Complexity
    ---------------
        O(1)
    """
    x = screen_width = sub_root.winfo_screenwidth() // 2 - sub_root.winfo_width() // 2
    root_y = root.winfo_y() - sub_root.winfo_height() - 31
    sub_root.geometry(f'+{x}+{root_y}')

def on_closing(root, sub_root):
    """
    Closes both the root and sub_root windows when one window is closed.

    Parameters
    ----------
    root : tk.Tk
        The root window of the InfoDisplayUI.
    sub_root : tk.Toplevel
        The sub window of the TimeSimulatorUI.

    Space Complexity
    ---------------
        O(1)

    Time Complexity
    ---------------
        O(1)
    """
    try:
        root.destroy()
    except tk.TclError:
        pass
    try:
        sub_root.destroy()
    except tk.TclError:
        pass