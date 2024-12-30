from datetime import datetime, timedelta

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

def precompute_simulation_states(packages, trucks):
    """
    Precomputes the states of all packages and trucks at each time from 08:00 to 17:00.
    
    Parameters:
    packages (list): The list of packages.
    trucks (list): The list of trucks.
    
    Returns:
    dict: A dictionary where keys are times in 24-hour format (HH:MM) and values are the states of packages and trucks.
    """
    time_list = generate_time_list()
    simulation_states = {}
    
    for time in time_list:
        # Simulate the state of packages and trucks at the given time
        # This is a placeholder for the actual simulation logic
        simulation_states[time] = {
            "packages": packages,
            "trucks": trucks
        }
    
    return simulation_states