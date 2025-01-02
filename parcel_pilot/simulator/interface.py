import tkinter as tk
from tkinter import ttk, messagebox
from simulator.time_sim import calculate_time, calculate_minutes, precompute_simulation_states
import re

class InfoDisplayUI:
    def __init__(self, root, time_simulator, packages, trucks):
        self.root = root
        self.time_simulator = time_simulator
        self.root.title("Parcel Pilot Dashboard")

        # Set the callback mechanism for time updates
        self.time_simulator.set_time_update_callback(self.update_time)

        # Current time display
        self.time_label = ttk.Label(root, text="", font=("Helvetica", 16))
        self.time_label.pack(pady=10)

        # Package information display
        self.package_frame = ttk.Frame(root)
        self.package_frame.pack(pady=10)
        self.package_tree = ttk.Treeview(self.package_frame, columns=("PID", "Status", "Location", "Truck", "Group", "Priority"), show="headings")
        self.package_tree.heading("PID", text="PID")
        self.package_tree.heading("Status", text="Status")
        self.package_tree.heading("Location", text="Location")
        self.package_tree.heading("Truck", text="Truck")
        self.package_tree.heading("Group", text="Group")
        self.package_tree.heading("Priority", text="Priority")
        self.package_tree.pack()

        # Configure TKinter tags for alternating row colors in package_tree
        self.package_tree.tag_configure("oddrow", background="#ffffff") # white
        self.package_tree.tag_configure("evenrow", background="#f0f0ff") # light blue


        # Truck information display
        self.truck_frame = ttk.Frame(root)
        self.truck_frame.pack(pady=10)
        self.truck_tree = ttk.Treeview(self.truck_frame, columns=("Truck ID", "Packages", "Location", "Miles"), show="headings")
        self.truck_tree.heading("Truck ID", text="Truck ID")
        self.truck_tree.heading("Packages", text="Packages")
        self.truck_tree.heading("Location", text="Location")
        self.truck_tree.heading("Miles", text="Miles")
        self.truck_tree.pack()

        # Configure TKinter tags for alternating row colors in truck_tree
        self.truck_tree.tag_configure("oddrow", background="#ffffff") # white
        self.truck_tree.tag_configure("evenrow", background="#f0f0ff") # light blue

        # Summary information display
        self.package_frame = ttk.Frame(root)
        self.package_frame.pack(pady=10)
        self.package_tree = ttk.Treeview(self.package_frame, columns=("PID", "Status", "Location", "Truck", "Group", "Priority"), show="headings")
        self.package_tree.heading("PID", text="PID")
        self.package_tree.heading("Status", text="Status")
        self.package_tree.heading("Location", text="Location")
        self.package_tree.heading("Truck", text="Truck")
        self.package_tree.heading("Group", text="Group")
        self.package_tree.heading("Priority", text="Priority")
        self.package_tree.pack()

        # Populate the information
        self.populate_package_info(packages)
        self.populate_truck_info(trucks)

        # Update the time display
        self.update_time()

    def update_time(self):
        if not self.time_simulator.is_editing: # This should not run when the user is editing the time input
            current_time = self.time_simulator.get_current_time()
            self.time_label.config(text=f"Current Time: {current_time}")
            simulation_state = self.time_simulator.get_simulation_state(current_time)
            if simulation_state:
                self.update_display(simulation_state)

    def update_display(self, simulation_state):
        """
        Updates the display with the given simulation state.
        
        Parameters:
        simulation_state (dict): The simulation state containing the states of packages and trucks.
        """
        # Clear the current display
        for item in self.package_tree.get_children():
            self.package_tree.delete(item)
        for item in self.truck_tree.get_children():
            self.truck_tree.delete(item)
        # Populate the package information
        self.populate_package_info(simulation_state["packages"])
        # Populate the truck information
        self.populate_truck_info(simulation_state["trucks"])

    def populate_package_info(self, packages):
        for index, package in enumerate(packages):
            tag = 'evenrow' if index % 2 == 0 else 'oddrow'
            self.package_tree.insert(
                "",
                "end",
                values=(
                    package.pid,
                    package.status,
                    package.location,
                    package.truck_id,
                    package.group,
                    package.priority
                    ),
                tags=(tag,)
            )

    def populate_truck_info(self, trucks):
        for index, truck in enumerate(trucks):
            tag = 'evenrow' if index % 2 == 0 else 'oddrow'
            package_ids = ", ".join(str(pkg.pid) for pkg in truck.packages)
            self.truck_tree.insert(
                "",
                "end",
                values=(
                    truck.truck_id,
                    package_ids,
                    truck.current_location,
                    truck.total_distance
                ),
                tags=(tag,)
            )

class TimeSimulatorUI:
    def __init__(self, root, simulation_states):
        self.root = root
        self.root.title("Time Simulator")
        self.is_editing = False # Flag to track if the user is editing the time input
        self.time_update_callback = None # Instance variable to store the callback function
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

    # Set the callback function for time updates
    def set_time_update_callback(self, callback):
        self.time_update_callback = callback

    def update_time(self, value):
        minutes_passed = int(float(value))
        current_time, _ = calculate_time(minutes_passed)
        self.time_var.set(current_time)
        if self.time_update_callback:
            self.time_update_callback() # Send the new time to other methods

    def get_current_time(self):
        return self.time_var.get()

    def on_focus_in(self, event):
        self.is_editing = True  # Set flag to True when editing starts
        self.time_input.selection_range(0, tk.END)

    def on_focus_out(self, event):
        self.validate_and_update_time()

    def on_enter(self, event):
        self.validate_and_update_time()

    def validate_and_update_time(self):
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
            self.time_update_callback() # Send the new time to other functions

    def get_simulation_state(self, time_str):
        """
        Allows passing the precomputed simulation state for the given time to other methods.

        Parameters:
        time_str (str): The time in 24-hour format (HH:MM).

        Returns:
        dict: The simulation state for the given time.
        """
        return self.simulation_states.get(time_str, None)

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')

# Position the TimeSimulatorUI (sub_root) window immediately above the InfoDisplayUI (root) window
def position_time_simulator(root, sub_root):
    x = screen_width = sub_root.winfo_screenwidth() // 2 - sub_root.winfo_width() // 2
    root_y = root.winfo_y() - sub_root.winfo_height() - 31
    sub_root.geometry(f'+{x}+{root_y}')

# Close both windows when one window is closed
def on_closing(root, sub_root):
    try:
        root.destroy()
    except tk.TclError:
        pass
    try:
        sub_root.destroy()
    except tk.TclError:
        pass