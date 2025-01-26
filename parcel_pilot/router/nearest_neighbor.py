def nearest_neighbor_algorithm(start_location, destinations_list, distances):
    """
    Determines the order of package deliveries using the nearest neighbor algorithm.

    Parameters:
    start_location (str): The starting location (e.g., the hub).
    packages (list): The list of packages to be delivered.
    distances (dict): The dictionary containing distances between locations.
    map_locations_reverse (dict): The dictionary mapping addresses to location destinations.

    Returns:
    list: The ordered list of package deliveries.
    """

    # Initialize the current location to the start location
    current_location = start_location
    route = []
    total_distance = 0

    while destinations_list:
        # Create a lookup table for the distances from the current location to the delivery locations
        lookup_table = {}
        for destination in destinations_list:
            try:
                lookup_table[destination] = distances[destination][current_location]
            except IndexError:
                lookup_table[destination] = distances[current_location][destination]
        # Find the nearest location using destinations_list as the destinations to the lookup_table dictionary
        nearest_location = min(
            destinations_list,
            key=lambda item: lookup_table[item]
        )
        # If the nearest location is the current location, remove it from the list of delivery locations
        if nearest_location == current_location:
            destinations_list.remove(nearest_location)
            continue # Start over with the current location removed from destinations_list
        distance = lookup_table[nearest_location]
        total_distance += distance
        # Add the nearest location and its distance to the delivery order
        route.append((nearest_location, distance))
        # Update the current location to the nearest location
        current_location = nearest_location
        # Remove the nearest location from the list of delivery locations
        destinations_list.remove(nearest_location)

    total_time = total_distance / 0.3
    full_route = [total_distance, total_time], route

    with open("routing.txt", "a") as file:
        file.write(f"Start location: {start_location} | Destinations list: {destinations_list} | Route: {full_route}\n")

    return full_route