import heapq

def dijkstra(graph, initial):
    shortest_paths = {initial: (None, 0)}
    priority_queue = [(0, initial)]
    visited = set()

    while priority_queue:
        current_weight, current_node = heapq.heappop(priority_queue)
        if current_node in visited:
            continue
        visited.add(current_node)
        destinations = graph.edges[current_node]
        weight_to_current_node = shortest_paths[current_node][1]

        for next_node in destinations:
            weight = graph.weights[(current_node, next_node)] + weight_to_current_node
            if next_node not in shortest_paths or weight < shortest_paths[next_node][1]:
                shortest_paths[next_node] = (current_node, weight)
                heapq.heappush(priority_queue, (weight, next_node))

    return shortest_paths