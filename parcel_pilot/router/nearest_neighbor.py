def nearest_neighbor_algorithm(start_location, destinations_list, distances):
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
    print("Destinations List:", destinations_list)

    # Initialize the current location to the start location
    current_location = start_location
    route = []
    total_distance = 0

    while destinations_list:
        # Create a lookup table for the distances from the current location to the delivery locations
        lookup_table = {}
        for key in destinations_list:
            try:
                lookup_table[key] = distances[key][current_location]
            except IndexError:
                lookup_table[key] = distances[current_location][key]
        # Find the nearest location using destinations_list as the keys to the lookup_table dictionary
        nearest_location = min(
            destinations_list,
            key=lambda item: lookup_table[item]
        )
        distance = lookup_table[nearest_location]
        total_distance += distance
        # Add the nearest location and its distance to the delivery order
        route.append((nearest_location, distance))
        # Update the current location to the nearest location
        current_location = nearest_location
        # Remove the nearest location from the list of delivery locations
        destinations_list.remove(nearest_location)

    # Add the return to beginning
    total_distance += distances[current_location][0]
    route.append((0, distances[current_location][0]))
    total_time = total_distance / 0.3
    full_route = [total_distance, total_time], route

    print("Route:", route)
    print("Total Distance:", total_distance)
    print("Total Time:", total_time)
    print(f"full_route: {full_route}")
    print("")
    return full_route