"""
This module contains helper functions used in the package delivery simulation.

Functions
---------
find_partial_match(locations, partial_string)
    Finds a partial match in the locations array and returns the matched value.

array_to_dict(array)
    Converts an array into a dictionary with integer-based keys starting from 0.

reverse_dict(dictionary)
    Reverses the keys and values of a dictionary.

convert_to_24_hour_format(time_str)
    Converts a time string from 12-hour format to 24-hour format.
"""

from datetime import datetime

def find_partial_match(locations, partial_string):
    """
    Finds a partial match in the locations array and returns the matched value.
    
    Parameters
    ----------
    locations : list
        The list of location strings.
    partial_string : str
        The partial string to search for.
    
    Returns
    -------
    str
        The matched value, otherwise None.

    Space Complexity
    ---------------
        O(1)

    Time Complexity
    ---------------
        O(n)
    """
    for location in locations:
        if partial_string.lower() in location.lower():
            return location
    return None

def array_to_dict(array):
    """
    Converts an array into a dictionary with integer-based keys starting from 0.
    
    Parameters
    ----------
    array : list
        The input array to be converted into a dictionary.
    
    Returns
    -------
    dict
        A dictionary with integer keys and array elements as values.

    Space Complexity
    ---------------
        O(n)

    Time Complexity
    ---------------
        O(n)
    """
    return {i: array[i] for i in range(len(array))}

def reverse_dict(dictionary):
    """
    Reverses the keys and values of a dictionary.
    
    Parameters
    ----------
    dictionary : dict
        The dictionary to reverse.
    
    Returns
    -------
    dict
        A new dictionary with keys and values swapped.

    Space Complexity
    ---------------
        O(n)

    Time Complexity
    ---------------
        O(n)
    """
    return {value: key for key, value in dictionary.items()}

def convert_to_24_hour_format(time_str):
    """
    Converts a time string from 12-hour format to 24-hour format.

    Parameters
    ----------
    time_str : str
        The time string in 12-hour format.

    Returns
    -------
    str
        The time string in 24-hour format.

    Space Complexity
    ---------------
        O(1)

    Time Complexity
    ---------------
        O(1)
    """
    return datetime.strptime(time_str, "%I:%M %p").strftime("%H:%M")