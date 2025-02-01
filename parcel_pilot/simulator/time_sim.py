"""
This module contains functions for simulating time-based events in the package delivery environment.

A highlight of this module is the creation and storage of hash tables for every minute of the simulation.

Functions
---------
calculate_time(minutes_after_8am)
    Calculates the current time based on the number of minutes after 8:00 AM.

calculate_minutes(current_time_str)
    Calculates the number of minutes after 8:00 AM based on the current time.

generate_time_list()
    Generates a list of all times from 08:00 to 17:00 in one-minute increments.

precompute_simulation_states(all_packages, trucks, distances, graph, algo)
    Precomputes the states of all packages and trucks at each time from 08:00 to 17:00.
    Creates hash tables for all packages and trucks at each minute of the simulation.
"""

from datetime import datetime, timedelta
from router.distributor import Distributor
from router.package_handler import intake_packages, prioritize_packages
from simulator.minutes import Minute
from data.package_hash import PackageHashTable
from data.truck_hash import TruckHashTable

def calculate_time(minutes_after_8am):
    """
    Calculates the current time based on the number of minutes after 8:00 AM.
    
    Parameters
    ----------
    minutes_after_8am : int
        The number of minutes after 8:00 AM.
    
    Returns
    -------
    tuple
        A tuple containing the current time in 24-hour format (HH:MM) and the minutes passed.

    Space Complexity
    ---------------
        O(1)

    Time Complexity
    ---------------
        O(1)
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
    
    Parameters
    ----------
    current_time_str : str
        The current time in 24-hour format (HH:MM).
    
    Returns
    -------
    int
        The number of minutes after 8:00 AM.

    Space Complexity
    ---------------
        O(1)

    Time Complexity
    ---------------
        O(1)
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
    
    Returns
    -------
    list
        A list of times in 24-hour format (HH:MM) from 08:00 to 17:00.

    Space Complexity
    ---------------
        O(n)

    Time Complexity
    ---------------
        O(n)
    """
    start_time = datetime.strptime("08:00", "%H:%M")
    end_time = datetime.strptime("17:00", "%H:%M")
    time_list = []
    
    current_time = start_time
    while current_time <= end_time:
        time_list.append(current_time.strftime("%H:%M"))
        current_time += timedelta(minutes=1)
    
    return time_list

def precompute_simulation_states(all_packages, trucks, distances, graph, algo):
    """
    Precomputes the states of all packages and trucks at each time from 08:00 to 17:00.
    
    Parameters
    ----------
    all_packages : list
        The list of packages.
    trucks : list
        The list of trucks.
    distances : dict
        The dictionary containing distances between locations.
    graph : dict
        The graph representation of the delivery locations.
    algo : function
        The algorithm used for routing.
    
    Returns
    -------
    dict
        A dictionary where keys are times in 24-hour format (HH:MM) and values are Minute objects.

    Space Complexity
    ---------------
        O(n)

    Time Complexity
    ---------------
        O(n)
    """
    time_list = generate_time_list()
    simulation_states = {}
    packages = prioritize_packages(all_packages)

    # Instantiate the Distributor class in order to use it to distribute packages to trucks
    distributor = Distributor(trucks)
    
    # Simulate the state of packages and trucks at the given times
    for time in time_list:
        if time == "10:20":
            for package in packages:
                if package.pid == "9":
                    package.notes = "Address updated at 10:20"
                    package.address = "410 S State St"
                    package.city = "Salt Lake City"
                    package.state = "UT"
                    package.zip_code = "84111"
                    package.destination = 19
                    break
        # Iterate through the packages and get the next flight time
        next_flight_time = None
        arrival_times = []
        late_packages = 0
        pkgs = [pkg for pkg in packages if pkg.truck_id is None]
        intake_packages(pkgs, time)
        for pkg in pkgs:
            if pkg.arrival_time and pkg.arrival_time > time: 
                arrival_times.append(pkg.arrival_time)
        if arrival_times:
            next_flight_time = min(arrival_times)
            late_packages = len([time for time in arrival_times if time == next_flight_time])
        distributor.distribute_packages(pkgs, time, next_flight_time, late_packages, distances, graph, algo)
        for truck in trucks:
            truck.update_position(time)
        package_table = PackageHashTable() # Create a new hash table for packages
        for pkg in packages:
            package_table.insert(
                pkg.pid,
                pkg.address,
                pkg.city,
                pkg.state,
                pkg.zip_code,
                pkg.deadline,
                pkg.weight,
                pkg.status,
                pkg.notes,
                pkg.priority,
                pkg.truck_id,
                pkg.location,
                pkg.group,
                pkg.arrival_time,
                pkg.destination,
                pkg.delivery_time,
                pkg.timely
            )
        truck_table = TruckHashTable() # Create a new hash table for trucks
        for truck in trucks:
            package_ids = [pkg.pid for pkg in truck.packages]  # Extract only the package IDs
            truck_table.insert(
                truck.truck_id,
                package_ids,
                truck.current_location,
                truck.distance_from_last_location,
                truck.destination,
                truck.distance_to_destination,
                truck.total_distance,
                truck.travel_log,
                truck.route,
                truck.trip_minutes,
                truck.mile_marker,
                truck.total_time
            )

        # Create a Minute object and store it in the simulation_states dictionary
        simulation_states[time] = Minute(time, package_table, truck_table)
    return simulation_states