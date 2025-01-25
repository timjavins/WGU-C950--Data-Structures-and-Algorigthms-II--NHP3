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

    # Initialize the current location to the start location
    current_location = start_location
    route = []
    delivery_distance = 0

    while destinations_list:
        # Create a lookup table for the distances from the current location to the delivery locations
        lookup_table = {}
        for destination in destinations_list:
            try:
                lookup_table[destination] = distances[destination][current_location]
            except IndexError:
                lookup_table[destination] = distances[current_location][destination]
        # Find the nearest location using destinations_list as the keys to the lookup_table dictionary
        nearest_location = min(
            destinations_list,
            key=lambda item: lookup_table[item]
        )
        distance = lookup_table[nearest_location]
        delivery_distance += distance
        # Add the nearest location and its distance to the delivery order
        route.append((nearest_location, distance))
        # Update the current location to the nearest location
        current_location = nearest_location
        # Remove the nearest location from the list of delivery locations
        destinations_list.remove(nearest_location)

    # Add the return to beginning
    total_distance = delivery_distance + distances[current_location][0]
    route.append((0, distances[current_location][0]))
    delivery_time = delivery_distance / 0.3
    total_time = total_distance / 0.3
    full_route = [total_distance, total_time, delivery_distance, delivery_time], route
    return full_route