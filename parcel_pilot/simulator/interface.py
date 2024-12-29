import tkinter as tk
from tkinter import ttk, messagebox
from simulator.time_sim import calculate_time, calculate_minutes
import re

class InfoDisplayUI:
    def __init__(self, root, time_simulator, packages, trucks):
        self.root = root
        self.time_simulator = time_simulator
        self.root.title("Parcel Pilot Dashboard")

        # Current time display
        self.time_label = ttk.Label(root, text="", font=("Helvetica", 16))
        self.time_label.pack(pady=10)

        # Package information display
        self.package_frame = ttk.Frame(root)
        self.package_frame.pack(pady=10)
        self.package_tree = ttk.Treeview(self.package_frame, columns=("PID", "Status", "Location", "Truck"), show="headings")
        self.package_tree.heading("PID", text="PID")
        self.package_tree.heading("Status", text="Status")
        self.package_tree.heading("Location", text="Location")
        self.package_tree.heading("Truck", text="Truck")
        self.package_tree.pack()

        # Truck information display
        self.truck_frame = ttk.Frame(root)
        self.truck_frame.pack(pady=10)
        self.truck_tree = ttk.Treeview(self.truck_frame, columns=("Truck ID", "Packages", "Location"), show="headings")
        self.truck_tree.heading("Truck ID", text="Truck ID")
        self.truck_tree.heading("Packages", text="Packages")
        self.truck_tree.heading("Location", text="Location")
        self.truck_tree.pack()

        # Populate the information
        self.populate_package_info(packages)
        self.populate_truck_info(trucks)

        # Update the time display
        self.update_time()

    def update_time(self):
        current_time = self.time_simulator.get_current_time()
        self.time_label.config(text=f"Current Time: {current_time}")
        self.root.after(1000, self.update_time)  # Update every second

    def populate_package_info(self, packages):
        for package in packages:
            self.package_tree.insert("", "end", values=(package.pid, package.status, package.location, package.truck_id))

    def populate_truck_info(self, trucks):
        for truck in trucks:
            package_ids = ", ".join(str(pkg.pid) for pkg in truck.packages)
            self.truck_tree.insert("", "end", values=(truck.truck_id, package_ids, truck.current_location))

class TimeSimulatorUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Time Simulator")

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

    def update_time(self, value):
        minutes_passed = int(float(value))
        current_time, _ = calculate_time(minutes_passed)
        self.time_var.set(current_time)

    def get_current_time(self):
        return self.time_var.get()

    def on_focus_in(self, event):
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

# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    app = TimeSimulatorUI(root)
    root.mainloop()