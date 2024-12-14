import tkinter as tk
from tkinter import ttk, messagebox
from simulator.time_sim import calculate_time, calculate_minutes
import re

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