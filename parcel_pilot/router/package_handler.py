import re
from helpers import convert_to_24_hour_format

def link_packages(packages):
    linked_packages = {}
    for package in packages:
        if package.notes.startswith('Must be delivered with'):
            # extract the linked package IDs by looking for numbers in the notes via regex
            links = re.findall(r'\d+', package.notes)
            # add the PID to the list of linked packages
            if package.pid not in linked_packages:
                linked_packages[package.pid] = links
    print("Linked Packages:", linked_packages)
    return linked_packages

def group_linked_packages(linked_packages):
    groups = []
    for key, values in linked_packages.items():
        # Create a new array with the key and each value inside the key's corresponding array
        new_group = [key] + values
        # If groups is empty, append the new group to groups
        if not groups:
            groups.append(new_group)
        else:
            # Check if any of the values in new_group are already in any existing group
            added_to_existing_group = False
            for group in groups:
                if any(item in group for item in new_group):
                    group.extend(item for item in new_group if item not in group)
                    added_to_existing_group = True
                    break
            # If the new group was not added to any existing group, append it as a new group
            if not added_to_existing_group:
                groups.append(new_group)
    print("Linked Package Groups:", groups)
    return groups

def prioritize_packages(packages):
    # Initialize the priority value
    i = 1
    # Assign priorities based on deadlines
    while any(package.priority == -1 for package in packages):
        # Find the next package with a priority of -1, which means not prioritized yet
        for package in packages:
            if package.priority == -1:
                # Assign priority 0 to packages with a deadline of EOD
                if package.deadline == "EOD":
                    package.priority = 0
                else:
                    # Find the lowest text-based time value among all packages with priority -1
                    lowest_deadline = min(
                        (p.deadline for p in packages if p.priority == -1 and p.deadline != "EOD"),
                        default=None
                    )
                    if lowest_deadline:
                        # Assign the current priority value to all packages with the same deadline
                        for p in packages:
                            if p.deadline == lowest_deadline and p.priority == -1:
                                p.priority = i
                        # Increment the priority value
                        i += 1
                break
    return packages

def intake_packages(packages, time):
    # Update the location of the packages based on the current time
    for package in packages:
        # Case 1: Package is delayed
        if package.notes.startswith('Delayed on flight'):
            # Delayed packages have no location until they arrive at the hub
            match = re.search(r'Delayed on flight---will not arrive to depot until (\d{1,2}:\d{2} [APap][Mm])', package.notes)
            if match:
                note_time = match.group(1)
                arrival_time = convert_to_24_hour_format(note_time)
                if time < arrival_time:
                    package.location = None  # Delayed packages have no location
                    package.status = f"IN TRANSIT - EXPECTED AT {arrival_time}"
                else:
                    package.location = 0
                    package.status = "AT DESTINATION HUB"
            else:
                package.location = None  # Delayed packages have no location
                package.status = "IN TRANSIT - DELAYED"
        # Case 2: Package is already at the hub
        else:
            package.location = 0  # Default to the hub location
            package.status = "AT DESTINATION HUB"
    return packages