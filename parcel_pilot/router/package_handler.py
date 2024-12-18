import re

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
        # Find the next package with a priority of -1
        for package in packages:
            if package.priority == -1:
                if package.delivery_deadline == "EOD":
                    package.priority = 0
                else:
                    # Find the lowest text-based time value among all packages with priority -1
                    lowest_deadline = min(
                        (p.delivery_deadline for p in packages if p.priority == -1 and p.delivery_deadline != "EOD"),
                        default=None
                    )
                    if lowest_deadline:
                        # Assign the current priority value to all packages with the same deadline
                        for p in packages:
                            if p.delivery_deadline == lowest_deadline and p.priority == -1:
                                p.priority = i
                        # Increment the priority value
                        i += 1
                break
    return packages