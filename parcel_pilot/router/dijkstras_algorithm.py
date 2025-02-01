import heapq

def dijkstra(graph, initial_node, destinations):
    # Ensure initial is a single node identifier
    if isinstance(initial_node, list) or isinstance(initial_node, tuple):
        initial = initial_node[0]  # Use the node ID as the identifier
    else:
        initial = initial_node
    with open("dijkstra.txt", "w") as file:
        file.write("Dijkstra's Algorithm\n")
        file.write(f"Graph edges: {graph.edges}\n")
        file.write(f"Passed initial node: {initial}\n")
        file.write(f"Initial node: {initial}\n")
        file.write(f"Destinations: {destinations}\n")

    shortest_paths = {initial: (None, 0)}
    priority_queue = [(0, initial)]
    visited = set()
    reached_destinations = set()

    while priority_queue and len(reached_destinations) < len(destinations):
        current_weight, current_node = heapq.heappop(priority_queue)
        if current_node in visited:
            continue
        visited.add(current_node)

        # Log current node and its neighbors
        with open("dijkstra.txt", "a") as file:
            file.write(f"Current node: {current_node}\n")
            file.write(f"Visited nodes: {visited}\n")

        if current_node not in graph.edges:
            with open("dijkstra.txt", "a") as file:
                file.write(f"Error: Node {current_node} not found in graph.edges\n")
            raise KeyError(current_node)

        destinations = graph.edges[current_node]
        weight_to_current_node = shortest_paths[current_node][1]

        for next_node in destinations:
            weight = graph.weights[(current_node, next_node)] + weight_to_current_node
            if next_node not in shortest_paths or weight < shortest_paths[next_node][1]:
                shortest_paths[next_node] = (current_node, weight)
                heapq.heappush(priority_queue, (weight, next_node))

        if current_node in destinations:
            reached_destinations.add(current_node)

    # Reconstruct the shortest path to each destination
    total_distance = 0
    route = []
    for destination in destinations:
        if destination in shortest_paths:
            path = []
            current_node = destination
            while current_node is not None:
                path.append(current_node)
                next_node = shortest_paths[current_node][0]
                if next_node is not None:
                    total_distance += graph.weights[(next_node, current_node)]
                current_node = next_node
            route.append((path[::-1], total_distance))

    total_time = total_distance / 0.3  # Assuming time is proportional to distance for simplicity
    with open("dijkstra.txt", "a") as file:
        for node in shortest_paths:
            file.write(f"Node: {node}, Path: {shortest_paths[node]}\n")
        file.write(f"Total distance: {total_distance}, Total time: {total_time}\n")
        file.write(f"Route: {route}\n")
        file.write(f"Returned: {[total_distance, total_time], route}\n")

    return [[total_distance, total_time], route]