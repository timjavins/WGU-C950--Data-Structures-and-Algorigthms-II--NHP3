### Summary and Plan of Action

#### Objective:
The objective of this project is to create an algorithm to determine an efficient route and delivery distribution for the Western Governors University Parcel Service (WGUPS) daily local deliveries. The goal is to ensure that all 40 packages are delivered on time while meeting each package’s requirements and keeping the combined total distance traveled under 140 miles for all trucks.

#### Requirements:
1. Implement an algorithm to route delivery trucks.
2. Ensure all packages are delivered on time.
3. Meet specific package requirements.
4. Keep the combined total distance traveled under 140 miles.
5. Provide detailed comments and justifications for the code.

#### Plan of Action:
1. **Data Parsing:**
   - Parse the `WGUPS Distance Table.csv` to get the distances between delivery locations.
   - Parse the `WGUPS Package File.csv` to get the package details, including addresses and special requirements.

2. **Algorithm Selection:**
   - Use Dijkstra's algorithm to find the shortest path between delivery locations.

3. **Implementation Steps:**
   - Create a graph representation of the delivery locations and distances.
   - Implement Dijkstra's algorithm to determine the shortest path for deliveries.
   - Incorporate package requirements (e.g., delivery deadlines, special notes) into the routing logic.
   - Ensure the total distance traveled by all trucks is under 140 miles.

4. **Validation:**
   - Validate the solution against the requirements specified in the `C950 Task 1 Rubric.md`.
   - Ensure the algorithm meets the space-time complexity requirements using Big-O notation.
   - Evaluate the scalability and adaptability of the solution.
   - Discuss the efficiency and maintainability of the software design.
   - Justify the choice of data structures and keys used in the implementation.

#### Next Steps:
1. Implement the Python script for parsing the CSV files.
2. Create the graph representation of the delivery locations.
3. Implement Dijkstra's algorithm for routing.
4. Incorporate package requirements into the routing logic.
5. Validate the solution against the rubric.