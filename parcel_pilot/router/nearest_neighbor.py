def nearest_neighbor_algorithm(start_location, packages, distances):
    """
    Determines the order of package deliveries using the nearest neighbor algorithm.

    Parameters:
    start_location (str): The starting location (e.g., the hub).
    packages (list): The list of packages to be delivered.
    distances (dict): The dictionary containing distances between locations.
    map_locations_reverse (dict): The dictionary mapping addresses to location keys.

    Returns:
    list: The ordered list of package deliveries.
    """
    print("NEAREST NEIGHBOR ALGORITHM")

    # Get the keys of the delivery locations by looking up the corresponding value in the map_locations_reverse dictionary
    location_keys = list(set(package.destination for package in packages))

    # Initialize the current location to the start location
    current_location = start_location
    delivery_order = []

    while location_keys:
        # Create a lookup table for the distances from the current location to the delivery locations
        lookup_table = {} # This could be done with arrays by creating an array of size max(location_keys) + 1 and using the location keys as indices to populate the array with corresponding distances (blanks OK)
        for key in location_keys:
            print("Loop Key:", key)
            print("Current Location:", current_location)
            try:
                lookup_table[key] = distances[key][current_location]
            except IndexError:
                lookup_table[key] = distances[current_location][key]
        # Find the nearest location using location_keys as the keys to the lookup_table dictionary
        nearest_location = min(
            location_keys,
            key=lambda item: lookup_table[item]
        )

        # start_location = 0
        # test_location = 3
        # test_distance = distances[test_location][start_location]
        # print(f"Distance from {map_locations[start_location]} to {map_locations[test_location]}: {test_distance}")
        # Add the nearest location to the delivery order
        delivery_order.append(nearest_location)
        # Remove the nearest location from the list of delivery locations
        location_keys.remove(nearest_location)
        # Update the current location to the nearest location
        current_location = nearest_location
    print("Delivery Order:", delivery_order)
    print("")
    return delivery_order