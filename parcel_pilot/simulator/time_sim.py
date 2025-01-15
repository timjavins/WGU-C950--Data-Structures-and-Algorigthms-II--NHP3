from datetime import datetime, timedelta
from router.distributor import Distributor
from data.trucks import TruckManager, Truck
from router.package_handler import intake_packages, prioritize_packages
from simulator.minutes import Minute
import copy

def calculate_time(minutes_after_8am):
    """
    Calculates the current time based on the number of minutes after 8:00 AM.
    
    Parameters:
    minutes_after_8am (int): The number of minutes after 8:00 AM.
    
    Returns:
    tuple: A tuple containing the current time in 24-hour format (HH:MM) and the minutes passed.
    """
    # Define the start time as 8:00 AM
    start_time = datetime.strptime("08:00", "%H:%M")
    
    # Calculate the current time by adding the minutes to the start time
    current_time = start_time + timedelta(minutes=minutes_after_8am)
    
    # Format the current time in 24-hour format without seconds
    current_time_str = current_time.strftime("%H:%M")
    
    return current_time_str, minutes_after_8am

def calculate_minutes(current_time_str):
    """
    Calculates the number of minutes after 8:00 AM based on the current time.
    
    Parameters:
    current_time_str (str): The current time in 24-hour format (HH:MM).
    
    Returns:
    int: The number of minutes after 8:00 AM.
    """
    # Define the start time as 8:00 AM
    start_time = datetime.strptime("08:00", "%H:%M")
    
    # Parse the current time string into a datetime object
    try:
        if len(current_time_str) == 4:  # Format HHMM
            current_time = datetime.strptime(current_time_str, "%H%M")
        else:  # Format HH:MM
            current_time = datetime.strptime(current_time_str, "%H:%M")
    except ValueError:
        return 0  # Default to 0 if the input is invalid
    
    # Calculate the difference in minutes between the current time and the start time
    minutes_passed = int((current_time - start_time).total_seconds() / 60)
    
    return minutes_passed

def generate_time_list():
    """
    Generates a list of all times from 08:00 to 17:00 in one-minute increments.
    
    Returns:
    list: A list of times in 24-hour format (HH:MM) from 08:00 to 17:00.
    """
    start_time = datetime.strptime("08:00", "%H:%M")
    end_time = datetime.strptime("17:00", "%H:%M")
    time_list = []
    
    current_time = start_time
    while current_time <= end_time:
        time_list.append(current_time.strftime("%H:%M"))
        current_time += timedelta(minutes=1)
    
    return time_list

def precompute_simulation_states(all_packages, trucks, distances, algo):
    """
    Precomputes the states of all packages and trucks at each time from 08:00 to 17:00.
    
    Parameters:
    packages (list): The list of packages.
    trucks (list): The list of trucks.
    
    Returns:
    dict: A dictionary where keys are times in 24-hour format (HH:MM) and values are Minute objects.
    """
    time_list = generate_time_list()
    simulation_states = {}
    packages = prioritize_packages(all_packages)

    # Distribute packages into the trucks using the Distributor class
    distributor = Distributor(trucks)
    
    # Simulate the state of packages and trucks at the given times
    for time in time_list:
        # Iterate through the packages and get the next flight time
        next_flight_time = None
        arrival_times = []
        late_packages = 0
        intake_packages(packages, time)
        for package in packages:
            if package.arrival_time and package.arrival_time > time: 
                arrival_times.append(package.arrival_time)
        if arrival_times:
            next_flight_time = min(arrival_times)
            late_packages = len([time for time in arrival_times if time == next_flight_time])
        distributor.distribute_packages(packages, time, next_flight_time, late_packages, distances, algo)
        for truck in trucks:
            truck.update_position(time)
        # write the state of the packages and trucks to a text file
        with open("simulation_states.txt", "a") as file:
            file.write(f"Time: {time}\n")
            file.write("Trucks:\n")
            for truck in trucks:
                package_ids = [package.pid for package in truck.packages]
                file.write(f"Truck ID: {truck.truck_id}, Packages: {package_ids}\n")
                file.write(f"Current Location: {truck.current_location}, Mile Marker: {truck.mile_marker}, Trip Minutes: {truck.trip_minutes}\n")
                file.write(f"Log: {truck.travel_log}\n")
                file.write(f"Route: {truck.route}\n")
            file.write("\n")
        packages_copy = copy.deepcopy(packages)
        trucks_copy = copy.deepcopy(trucks)
        # Create a Minute object and store it in the simulation_states dictionary
        simulation_states[time] = Minute(time, packages_copy, trucks_copy)
    return simulation_states