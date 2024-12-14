## **Fibonacci heap** as a self-adjusting data structure for **Dijkstra's Algorithm**

### Fibonacci Heap:
- **Amortized Efficiency**: The Fibonacci heap offers excellent amortized time complexities for key operations used in Dijkstra's algorithm. For example, it allows for constant time insertions and amortized logarithmic time for decrease-key and delete operations, which are critical in Dijkstra's algorithm.
- **Improved Decrease-Key Operation**: Since Dijkstra's algorithm often requires updating the distances of adjacent nodes, the efficiency of the decrease-key operation in Fibonacci heaps can significantly improve the overall performance of the algorithm.
- **Lazy Merging**: The structure of Fibonacci heaps allows for lazy merging of trees, which can lead to better performance in practical scenarios compared to strict binary heaps.

### Example Usage:
- **Priority Queue**: In Dijkstra's algorithm, a priority queue manages the nodes to be explored. A Fibonacci heap can efficiently handle the priority queue operations, ensuring that the algorithm runs as smoothly and quickly as possible, especially for dense graphs or graphs with a large number of nodes and edges. In practice, Fibbonaci heaps are known to worsen performance until scaled up to a point of performance equilibrium, at which point larger-scale systems will begin to see performance improvements over other data structures as the systems continue to scale up.

### Other Considerations:
- **Splay Trees**: While splay trees are another self-adjusting structure, their amortized time complexity is less suitable for the frequent decrease-key operations required by Dijkstra's algorithm compared to Fibonacci heaps.

## Dictionary with nested lists as a table

```
table = {
    0: ["Name", "Age", "City"],
    1: ["Alice", 28, "New York"],
    2: ["Bob", 34, "Los Angeles"],
    3: ["Charlie", 22, "Chicago"]
}
```
# Accessing a specific cell
print(table[1][2])  # Output: "New York"

# Printing the entire table
for row in table.values():
    print(row)
