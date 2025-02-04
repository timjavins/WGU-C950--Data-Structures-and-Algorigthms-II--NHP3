Timothy Javins

ID 000698100

---

# Program Overview
The purpose of this application is to efficiently and effectively route package deliveries for the local WGUPS depot. The objective of the application is to deliver all packages by their deadlines while meeting all package requirements and performance requirements. The performance requirements include using no more than two trucks from 08:00 to 17:00 and driving less than 140 miles in total.

### F. Package delivery algorithm justification

1. Nearest Neighbor strengths
    - **Efficiency**: The nearest neighbor algorithm is efficient for the given problem size. It quickly finds the closest destination, reducing the overall travel distance, which directly correlates to timely deliveries.
    - **Simplicity**: The algorithm is straightforward to implement and understand. The next destination in the route is always the closest one to the previous location, which simplifies the logic and reduces the likelihood of errors.
    - **Adaptability**: The nearest neighbor algorithm can easily adapt to any combination of destinations. If a new package is added or a destination is removed, the algorithm can quickly recalculate the route without significant overhead.

2. Requirement satisfaction
    - The nearest neighbor algorithm ensures that all packages are delivered by their deadlines by prioritizing the closest destinations first. This minimizes travel time and helps meet the delivery constraints.
    - The algorithm keeps the total distance traveled by all trucks under 140 miles by optimizing the route to reduce unnecessary travel.
    - The nearest neighbor algorithm is a named algorithm.

3. Alternate algorithms
    - **Dijkstra's Algorithm**: This algorithm finds the shortest path between nodes in a graph, which can be used to determine the optimal route for package deliveries. Unlike the nearest neighbor algorithm, which makes greedy decisions based on the current location, Dijkstra's algorithm considers the entire graph and calculates the shortest path to each destination, which ensures the most efficient route but requires more computational resources.
    - **Genetic Algorithm**: This algorithm uses principles of natural selection to find optimal solutions. It evolves a population of routes over time, considering various constraints and optimizing for the best solution. This approach is more complex and computationally intensive than the nearest neighbor algorithm but can handle larger problem sizes and more complex constraints.

### G. Doing it differently

- **Dijkstra's Algorithm**: I would use Dijkstra's algorithm for routing because it may be the mathematically optimal choice. This algorithm calculates the shortest path between nodes in a graph, ensuring the most efficient route for package deliveries.
- **Graph-Based Approach**: I would use a graph representation instead of distance tables for routing. A graph-based approach allows for more flexible and efficient route calculations, as it can easily handle dynamic changes in the network, such as adding or removing nodes and edges. This method also integrates seamlessly with algorithms like Dijkstra's, providing a more robust and scalable solution for package deliveries.
- **User Interface Improvements**: I would develop a more intuitive and user-friendly interface for monitoring and managing deliveries. This could include real-time tracking, an interactive map, package and truck sprites, and detailed analytics to provide better insights into the delivery process.

### H. Data structure verification

The hash table structure ensures each package can be accessed in $O(1)$ average time by mapping its unique identifier. This performance is essential because the application frequently updates `package`, `truck`, and `minute` attributes (e.g., status, destination, location, etc.). As the user accesses package and truck data throughout the day, this efficient lookup capability is crucial for maintaining real-time updates and ensuring that the system can handle the dynamic nature of package deliveries.

By using hash tables, the application can quickly store and retrieve package and truck data, ensuring that the system remains responsive even as the number of packages and trucks increases. The hash tables automatically manage collisions using a self-adjusting hashing scheme, which helps maintain performance as the dataset grows. This approach provides a robust and scalable solution for managing the complex data requirements of the package delivery system.

1. Alternate data structures:
    - **Priority Queue**: This data structure focuses on efficiently managing elements based on their priority, providing $O(log n)$ time complexity for insertion and extraction of the highest-priority elements. It can be used to manage packages by delivery deadlines or other priority criteria, ensuring that the most urgent packages are processed first. Unlike a hash table, which provides $O(1)$ average time complexity for lookups but does not inherently manage element priorities, a priority queue orders items according to their time sensitivity or other relevant factors.
    - **Balanced Binary Search Tree (BST)**: A balanced BST, such as an AVL tree or a Red-Black tree, can provide $O(log n)$ time complexity for insertions, deletions, and lookups by ensuring that the tree remains balanced. Unlike a hash table, which offers $O(1)$ average time complexity for lookups but lacks order, a balanced BST preserves ordering for elements, enabling efficient range queries and sorted traversals.
