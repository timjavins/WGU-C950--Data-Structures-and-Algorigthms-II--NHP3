Javins


---

# Program Overview

## A. Algorithm Identification
This application uses a self-adjusting “nearest neighbor” algorithm (sometimes referred to as a type of greedy approach) for routing. In 
`distributor.py`, the `Distributor.distribute_packages` method calls `nearness` (or a similar helper) to find the next closest destination. This approach automatically updates routing decisions based on the current set of package destinations, making it suitable for the daily local deliveries problem.

## B. Data Structure Identification
The application makes use of a hash table to record the states of all packages and trucks, every minute of the work day.

A hash-based structure (custom hash tables) is featured throughout the codebase to store and retrieve package data quickly (e.g., storing packages by unique ID in `parcel_pilot/data/package_hash.py`). These hash tables perform key-based lookups efficiently on average, adjusting their underlying structure (hash buckets) for fast operations.

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
- Software: Python 3.x, including libraries such as tkinter (for UI), datetime, csv (for reading input files), heapq (for Dijkstra’s algorithm), and custom modules (for example, parcel_pilot/simulator/time_sim.py). Git for version control.
- Hardware: A 64-bit Windows 11 personal computer with 32 GB of RAM.
- Editor/IDE: Visual Studio Code for editing the Python code, with built-in terminals and testing/debug features.

### C3. Space-Time Complexity Using Big-O Notation
- Main Algorithm (Nearest Neighbor Routing): O(n²) in the worst case for each truck route, because for n destinations, checking each unvisited location can lead to an O(n) step repeated up to n times.  
- Dictionary-Based Lookups for Packages: O(1) average, O(n) worst-case for reads/writes.  
- Overall Program: Each minute (up to 540 minutes from 08:00–17:00) may invoke these operations, but the critical bottleneck is the route construction. The effective complexity remains acceptable for a typical route size (under 20 packages).

### C4. Scalability and Adaptability
The solution scales by:
- Incrementally adding more trucks and drivers or increasing daily package count without redesigning the core logic.
- The custom hash-based data structures resize themselves to store new packages and trucks as the system scales, ensuring efficient lookups and minimal overhead.
- Parsing manifests and tables programmatically, rather than hard-coding data.

While nearest-neighbor performance will degrade as n grows large, the truck capacity limits the max value of n to 16 per route, effectively splitting adversely complex routing problems into manageable sub-routes.

### C5. Software Efficiency and Maintainability
#### Efficiency
- Fast lookups in hash tables ensure minimal overhead.
- The time-managed simulation in `time_sim.py` reduces duplication and error proclivity by precomputing states.
#### Maintainability
- Clear separation of responsibilities—data parsing in `parser.py`, package distribution in `distributor.py`, time simulation in `time_sim.py`, etc.—makes updates straightforward.
- Breaking complex logic into many small, reusable functions enhances maintainability and readability, allowing for easier debugging and testing.
- Well-placed and informative comments throughout the codebase further enhance comprehension and facilitate smoother collaboration among developers.

### C6. Self-Adjusting Data Structures
Strengths:  
- Custom hash tables automatically manage collisions using a self-adjusting hashing scheme, scaling well on average.
- Insertion, deletion, and lookups often perform in O(1) due to efficient collision handling and dynamic resizing.
Weaknesses:  
- Worst-case collisions can degrade performance to O(n) if the hash table becomes too crowded.
- Hashing requires good distribution for efficiency; poor hashing or excessive collisions can slow performance.

### C7. Data Key
We use “package ID” as the key for efficient delivery management because:
- Each package’s ID is unique, ensuring there are no collisions during lookups.
- Using a unique ID allows for consistent and accurate tracking of each package's lifecycle, from intake to delivery.
- The unique ID simplifies the process of updating package statuses and locations, ensuring that each package can be individually managed without ambiguity.

## D. Sources
All code is original to this repository. External references for background:  
- [Python 3 Documentation](https://docs.python.org/3/) – For dictionaries and standard libraries.  
- [Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2009). Introduction to Algorithms.](https://mitpress.mit.edu) – For general knowledge on greedy algorithms and complexity notation.