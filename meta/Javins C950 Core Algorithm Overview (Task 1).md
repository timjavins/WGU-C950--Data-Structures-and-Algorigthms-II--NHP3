Javins


---

# Program Overview

## A. Algorithm Identification
This application uses a self-adjusting “nearest neighbor” algorithm (sometimes referred to as a type of greedy approach) for routing. In 
`distributor.py`, the `Distributor.distribute_packages` method calls `nearness` (or a similar helper) to find the next closest destination. This approach automatically updates routing decisions based on the current set of package destinations, making it suitable for the daily local deliveries problem.

## B. Data Structure Identification
The application makes use of a hash table to record the states of all packages and trucks, every minute of the work day.

A hash-based structure (Python dictionaries) is featured throughout the codebase to store and retrieve package data quickly (e.g., storing packages by unique ID in parcel_pilot/data/packages.py). Python dictionaries perform key-based lookups efficiently on average, adjusting their underlying structure (hash buckets) for fast operations.

### B1. Explanation of Data Structure
The dictionary structure ensures each package can be accessed in O(1) average time by its unique identifier. This relationship is essential because the application frequently updates packages (e.g., status, destination, or group). For instance, the routing logic in `distributor.py` references packages by ID to load them into a truck at a specific time, and the scheduler in `time_sim.py` updates truck and package states each minute.

## C. Program Overview

### C1. Algorithm’s Logic (Pseudocode)
The logic for routing and scheduling in this application can be summarized:

```plaintext
function PRECOMPUTE_SIMULATION_STATES(packages, trucks, distances, algo):
    time_list = generate_time_list(08:00 to 17:00)
    simulation_states = {}
    prioritize_packages(packages)
    distributor = new Distributor(trucks)

    for time in time_list:
        # Intake newly arrived packages
        intake_packages(packages, time)

        # Distribute packages to trucks using nearest-neighbor or chosen algo
        distributor.distribute_packages(packages, time, next_flight_time, late_packages, distances, algo)

        # Update truck positions
        for truck in trucks:
            truck.update_position(time)

        # Store copy of package & truck states for later retrieval
        simulation_states[time] = Minute(time, packages.copy(), trucks.copy())

    return simulation_states
```

In words:
1. Generate a list of times (08:00–17:00).
2. For each minute, bring in newly available packages, call the distributor to load and schedule packages, then update truck positions.
3. Store a snapshot of the day’s state in a “minute object” so the UI can retrieve package/truck status.

### C2. Development Environment
- Software: Python 3.x, leveraging libraries such as tkinter (for UI), datetime, and potentially custom modules (e.g., parcel_pilot/simulator/time_sim.py).  
- Hardware: Any environment supporting Python 3 (Windows, macOS, Linux) with sufficient memory (e.g., 4GB+) and CPU to run Python scripts efficiently.  
- Editor/IDE: Visual Studio Code for editing the Python code, with built-in terminals and debug features.

### C3. Space-Time Complexity Using Big-O Notation
- Main Algorithm (Nearest Neighbor Routing): O(n²) in the worst case for each truck route, because for n destinations, checking each unvisited location can lead to an O(n) step repeated up to n times.  
- Dictionary-Based Lookups for Packages: O(1) average, O(n) worst-case for reads/writes.  
- Overall Program: Each minute (up to 540 minutes from 08:00–17:00) may invoke these operations, but the critical bottleneck is the route construction. Thus, the effective complexity remains acceptable for a typical route size (under 50 packages).

### C4. Scalability and Adaptability
The solution scales by:
- Incrementally adding more trucks or reorganizing packages without redesigning the core logic.  
- Reusing the dictionary structure to store newly added packages.  
- Adding or modifying the distance matrix for new cities in `WGUPS Distance Table.csv`.  

Because nearest-neighbor performance will degrade as n grows large, it may still be adapted by splitting deliveries into smaller sub-routes or integrating more advanced optimizations.

### C5. Software Efficiency and Maintainability
- Efficiency: Fast lookups in dictionaries ensure minimal overhead. The time-managed simulation in `time_sim.py` reduces duplication by precomputing states.
- Maintainability: Clear separation of responsibilities—data parsing in `parser.py`, distribution logic in `distributor.py`, and time simulation in `time_sim.py`—makes updates straightforward. Comments in code further facilitate understanding.

### C6. Self-Adjusting Data Structures
Strengths:  
- Python dictionaries automatically manage collisions using a hashing scheme, scaling well on average.  
- Insertion, deletion, and lookups often perform in O(1).  
Weaknesses:  
- Worst-case collisions can degrade performance to O(n).  
- Hashing requires good distribution for efficiency; poor hashing or excessive collisions slow performance.

### C7. Data Key
We use “package ID” as the dictionary key because:  
- Each package’s ID is unique, avoiding collisions for lookups.  
- Consistent lookups are needed to track the lifecycle of each package, and referencing by a unique ID ensures accurate updates.

## D. Sources
All code is original to this repository. External references for background:  
- [Python 3 Documentation](https://docs.python.org/3/) – For dictionaries and standard libraries.  
- [Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2009). Introduction to Algorithms.](https://mitpress.mit.edu) – For general knowledge on greedy algorithms and complexity notation.