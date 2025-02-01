"""
This module contains functions for handling packages in the package delivery simulation.

Functions
---------
intake_packages(packages, time)
    Updates the location and status of packages based on the current time.

prioritize_packages(packages)
    Assigns priority values to packages based on their delivery deadlines.

link_packages(packages)
    Identifies and returns linked packages based on their notes.

group_linked_packages(linked_packages, packages)
    Groups linked packages and assigns group numbers to them.
"""

import re
from helpers import convert_to_24_hour_format

def intake_packages(packages, time):
    """
    Updates the location and status of packages based on the current time.
    
    Parameters
    ----------
    packages : list
        The list of packages.
    time : str
        The current time in 24-hour format (HH:MM).
    
    Returns
    -------
    list
        The updated list of packages.

    Space Complexity
    ---------------
        O(n)

    Time Complexity
    ---------------
        O(n)
    """
    for package in packages:
        if package.truck_id is None:
            if package.notes.startswith('Wrong address listed'):
                continue
            if package.notes.startswith('Delayed'):
                match = re.search(r'Delayed on flight---will not arrive to depot until (\d{1,2}:\d{2} [APap][Mm])', package.notes)
                if match:
                    note_time = match.group(1)
                    arrival_time = convert_to_24_hour_format(note_time)
                    if time < arrival_time:
                        package.location = None
                        package.status = f"IN TRANSIT - EXPECTED AT {arrival_time}"
                        package.arrival_time = arrival_time
                    else:
                        package.location = 0
                        package.status = "AT DESTINATION HUB"
                        package.notes = f"Arrived to depot at {note_time}"
                else:
                    package.location = None
                    package.status = "IN TRANSIT - DELAYED"
            else:
                package.location = 0
                package.status = "AT DESTINATION HUB"
    return packages

def prioritize_packages(packages):
    """
    Assigns priority values to packages based on their delivery deadlines.
    
    Parameters
    ----------
    packages : list
        The list of packages.
    
    Returns
    -------
    list
        The list of packages with assigned priorities.

    Space Complexity
    ---------------
        O(n)

    Time Complexity
    ---------------
        O(n^2)
    """
    i = 1
    while any(package.priority == -1 for package in packages):
        for package in packages:
            if package.priority == -1:
                lowest_deadline = min(
                    (p.deadline for p in packages if p.priority == -1 and p.deadline != "EOD"),
                    default=None
                )
                if lowest_deadline:
                    for p in packages:
                        if p.deadline == lowest_deadline and p.priority == -1:
                            p.priority = i
                    i += 1
                elif package.deadline == "EOD":
                    package.priority = i
    return packages

def link_packages(packages):
    """
    Identifies and returns linked packages based on their notes.
    
    Parameters
    ----------
    packages : list
        The list of packages.
    
    Returns
    -------
    dict
        A dictionary where keys are package IDs and values are lists of linked package IDs.

    Space Complexity
    ---------------
        O(n)

    Time Complexity
    ---------------
        O(n)
    """
    linked_packages = {}
    for package in packages:
        if package.notes.startswith('Must be delivered with'):
            links = re.findall(r'\d+', package.notes)
            if package.pid not in linked_packages:
                linked_packages[package.pid] = links
    return linked_packages

def group_linked_packages(linked_packages, packages):
    """
    Groups linked packages and assigns group numbers to them.
    
    Parameters
    ----------
    linked_packages : dict
        A dictionary where keys are package IDs and values are lists of linked package IDs.
    packages : list
        The list of packages.
    
    Returns
    -------
    list
        A list of groups, where each group is a list of linked package IDs.

    Space Complexity
    ---------------
        O(n)

    Time Complexity
    ---------------
        O(n^2)
    """
    groups = []
    package_dict = {package.pid: package for package in packages}

    for key, values in linked_packages.items():
        new_group = [key] + values
        if not groups:
            groups.append(new_group)
        else:
            added_to_existing_group = False
            for group in groups:
                if any(item in group for item in new_group):
                    group.extend(item for item in new_group if item not in group)
                    added_to_existing_group = True
                    break
            if not added_to_existing_group:
                groups.append(new_group)

    for index, group in enumerate(groups):
        group_key = index + 1
        for package_id in group:
            package_dict[package_id].group = group_key

    return groups