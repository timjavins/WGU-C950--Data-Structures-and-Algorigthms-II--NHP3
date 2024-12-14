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