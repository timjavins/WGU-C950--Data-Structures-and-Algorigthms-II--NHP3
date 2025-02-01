"""
This module contains a function for sorting packages based on their nearness to a specific location.

Functions
---------
nearness(packages, distances)
    Returns a list of package IDs, sorted by their nearness to location 0.
"""

def nearness(packages, distances):
    """
    Returns a list of package IDs, sorted by their nearness to location 0.

    Steps
    -----
    1. Filter the packages to only include those with status "AT DESTINATION HUB".
    2. For each package, read package.pid and package.destination.
    3. Use package.destination as the key to look up the corresponding list in 'distances'.
    4. The nearness value is the first element of that list (distances[destination][0]).
    5. Sort the packages by this nearness value.
    6. Return the sorted list of package IDs.

    Parameters
    ----------
    packages : list
        The list of packages.
    distances : dict
        The dictionary containing distances between locations.

    Returns
    -------
    list
        A list of package IDs sorted by their nearness to location 0.

    Space Complexity
    ---------------
        O(n)

    Time Complexity
    ---------------
        O(n log n)
    """
    # Filter packages with status "AT DESTINATION HUB"
    filtered_packages = [package for package in packages if package.status == "AT DESTINATION HUB"]

    # Create a list of tuples (packageID, nearnessValue).
    package_nearness = []
    for package in filtered_packages:
        nearness_value = distances[package.destination][0]
        package_nearness.append((package.pid, nearness_value))

    # Sort the list by the nearness value (smallest to greatest).
    package_nearness.sort(key=lambda x: x[1])

    # Extract only the package IDs in sorted order.
    sorted_pids = [pid for pid, _ in package_nearness]
    return sorted_pids