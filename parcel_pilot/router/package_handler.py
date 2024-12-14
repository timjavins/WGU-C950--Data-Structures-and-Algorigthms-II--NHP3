import re

def link_packages(packages):
    linked_packages = {}
    for package in packages:
        if package['Notes'].startswith('Must be delivered with'):
            # extract the linked package IDs by looking for numbers in the notes via regex
            links = re.findall(r'\d+', package['Notes'])
            # add the PID to the list of linked packages
            if package['PID'] not in linked_packages:
                linked_packages[package['PID']] = links
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
    # Create a dictionary to store the priority of each package
    priority_dict = {}
    for package in packages:
        # Extract the priority number from the notes field
        priority = re.search(r'\d+', package['Notes'])
        # If a priority number is found, assign it to the package ID in the dictionary
        if priority:
            priority_dict[package['PID']] = int(priority.group())
    # Sort the packages based on priority, with higher priority packages first
    sorted_packages = sorted(packages, key=lambda x: priority_dict.get(x['PID'], 0), reverse=True)
    return sorted_packages