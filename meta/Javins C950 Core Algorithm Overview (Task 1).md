Timothy Javins

ID 000698100

---

# Program Overview
The purpose of this application is to efficiently and effectively route package deliveries for the local WGUPS depot. The objective of the application is to deliver all packages by their deadlines while meeting all package requirements and performance requirements. The performance requirements include using no more than two trucks from 08:00 to 17:00 and driving less than 140 miles in total.


## A. Algorithm Identification
This application will use a “nearest neighbor” algorithm (a type of greedy approach) for routing. The nearest neighbor algorithm will first find the closest destination to the current location. When the closest destination is identified, it becomes the current location and is removed from the list of destinations. The process iterates sequentially through the list of destinations until all destinations are included in the route. This approach automatically makes routing decisions based on the current set of package destinations, making it suitable for the daily local deliveries problem.

## B. Data Structure Identification
The application makes use of hash tables to record the states of all packages and trucks, every minute of the work day.

A hash-based structure (custom hash tables) will be featured throughout the codebase to store and retrieve package and truck data quickly. These hash tables perform key-based lookups efficiently on average, adjusting their underlying structure (hash buckets) to optimize for fast operations.

### B1. Explanation of Data Structure
The hash table structure ensures each package can be accessed in $O(1)$ average time by mapping its unique identifier. This performance is essential because the application frequently updates `package`, `truck`, and `minute` attributes (e.g., status, destination, location, etc.). For instance, the routing logic in `distributor` will reference packages by ID to load them into a truck, and the time simulator will update truck and package states each minute.

## C. Program Overview

### C1. Algorithm’s Logic (Pseudocode)
The logic for routing and scheduling in this application can be summarized:

```plaintext
function PRECOMPUTE SIMULATION STATES(packages, trucks, map):
    simulation_states = []
    time_list = generate_time_list(08:00 to 17:00)

    for each minute in time_list:
        intake_packages(packages, time):
            for each package, set current location to hub if not delayed past current time and current location is None

        call DISTRIBUTOR(packages, trucks, map, time)

        for truck in trucks:
            update truck position

        p.hash = HASH PACKAGES(packages)
        t.hash = HASH TRUCKS(trucks)

        store p.hash and t.hash in a minute object

        simulation_states += minute

    return simulation_states

function DISTRIBUTOR(packages, trucks, map, time):
    if available trucks:
        create queues for each truck
        organize packages(packages):
            for each package at hub:
                if truck requirement, put package in specified truck queue
                else, put package in smallest truck queue
                for each remaining package, put package in same truck queue if destination or group matches queued package

        distribute packages(truck queue):
            while truck load < 16:
                for each package in truck queue:
                    load if earliest deadline
                    load if grouped with earliest deadline package
                    load if destination matches earliest deadline package
                    mark as "out for delivery" if loaded
        
        get route(loaded packages):
            route = []
            current_location = hub
            for deadline in package deadlines:
                list destinations of current deadline packages
                call NEAREST NEIGHBOR(current location, destinations, map)
                append NEAREST NEIGHBOR result to route
                current location = last destination in route
            append hub return trip to route

        send trucks(route)
            send the truck on its route

function NEAREST NEIGHBOR(current location, destinations, map):
    determine closest destination
    update current location to closest destination
    remove current location from destinations
    repeat until all destinations are routed
    return route

function HASH PACKAGES(packages):
    Initialize a hash table with a default size of 40

    function _hash(package ID):
        Convert the package ID to a string
        Calculate the sum of the ASCII values of the characters in the key
        Return the sum modulo the size of the hash table

    function _grow():
        Calculate the new size as 1.5 times the current size
        Initialize a new table with the new size
        Rehash all items from the old table into the new table
        Update the size and table to the new values

    function _shrink():
        Calculate the new size as 0.75 times the current size
        Initialize a new table with the new size
        Rehash all items from the old table into the new table
        Update the size and table to the new values

    function insert(package):
        If the load factor exceeds 0.7, call _grow()
        Calculate the index using _hash(package ID)
        If the bucket at the index is empty, initialize it as an empty list
        If the package ID already exists in the bucket, update the package data
        Otherwise, append the new package data to the bucket
        Increment the count of items in the hash table

    function get(package ID):
        Calculate the index using _hash(package ID)
        If the bucket at the index contains the package ID, return the package data
        Otherwise, return None

    function remove(package ID):
        Calculate the index using _hash(package ID)
        If the bucket at the index contains the package ID, remove the package data
        Decrement the count of items in the hash table
        If the load factor falls below 0.5, call _shrink()

    Return the hash table


function HASH TRUCKS(trucks):
    Initialize a hash table with a default size of 10

    function _hash(key):
        Convert the key to a string
        Calculate the sum of the ASCII values of the characters in the key
        Return the sum modulo the size of the hash table

    function _grow():
        Calculate the new size as 1.5 times the current size
        Initialize a new table with the new size
        Rehash all items from the old table into the new table
        Update the size and table to the new values

    function _shrink():
        Calculate the new size as 0.75 times the current size
        Initialize a new table with the new size
        Rehash all items from the old table into the new table
        Update the size and table to the new values

    function insert(trucks):
        If the load factor exceeds 0.7, call _grow()
        Calculate the index using _hash(truck ID)
        If the bucket at the index is empty, initialize it as an empty list
        If the truck ID already exists in the bucket, update the truck data
        Otherwise, append the new truck data to the bucket
        Increment the count of items in the hash table

    function get(truck ID):
        Calculate the index using _hash(truck ID)
        If the bucket at the index contains the truck ID, return the truck data
        Otherwise, return None

    function remove(truck ID):
        Calculate the index using _hash(truck ID)
        If the bucket at the index contains the truck ID, remove the truck data
        Decrement the count of items in the hash table
        If the load factor falls below 0.5, call _shrink()

    Return the hash table
```

In words:
1. Generate a list of times (08:00–17:00).
2. Pass the packages to the package intake each minute.
3. For each minute, call the distributor to order, distribute, route, and load the packages, and send the trucks when appropriate.
4. Update the truck positions each minute.
5. Store a snapshot of the package and truck states in a `minute` object so the UI can retrieve the package and truck states at any given time of day.

### C2. Development Environment
- Software: Python 3.x, including libraries such as tkinter (for UI), datetime, csv (for reading input files), heapq (for Dijkstra’s algorithm), and custom modules (for example, parcel_pilot/simulator/time_sim.py). Git for version control.
- Hardware: A 64-bit Windows 11 personal computer with 32 GB of RAM.
- Editor/IDE: Visual Studio Code for editing the Python code, with built-in terminals and testing/debug features.
Below is a concise list of imported modules and packages across the files, along with brief descriptions of each dependency.

While the application will use no third-party libraries, there will be some imports from the Python Standard Library. The `datetime` module provides date and time manipulation via `datetime` and `timedelta` classes. The `re` module allows for regular expression matching and parsing, which is important for handling package requirements and time dynamics. The `csv` module enables reading and writing CSV-format data. The `tkinter` package is the Standard Python GUI toolkit for creating windows, dialogs, and other interface elements.

### C3. Space-Time Complexity Using Big-O Notation
- Named Algorithm (Nearest Neighbor Routing): $O(n²)$ in the worst case for each truck route, because for n destinations, checking each unvisited location can lead to an $O(n)$ step repeated up to n times.  
- Hash-Based Lookups for Packages: $O(1)$ average, $O(n)$ worst-case for reads/writes.  
- Overall Program: Each minute (up to 540 minutes from 08:00–17:00) may invoke hash lookup operations, but only at the user's request. The worst-case writing and reading hash tables would be $O(M*n+u*n)$ where M = 540 minutes in the work day (creating hash tables) and u = the number of user lookup requests (reading hash tables). However, the critical bottleneck is the route construction at $O(n²)$. The effective complexity remains acceptable for a typical route size, which is under 20 packages.

### C4. Scalability and Adaptability
The solution scales by:
- gracefully handling incremental count increases in trucks, drivers, or daily packages without the need to redesign the logic.
- utilizing the custom hash-based data structures to resize themselves in order to store new packages and trucks as the system scales, ensuring efficient lookups and minimal overhead.
- parsing manifests and tables programmatically, rather than hard-coding data, ensuring that any manifest or distances table will not require changes in the code.
- employing the nearest neighbor algorithm, which will function for destination lists of all sizes, including lists for trucks with larger capacities, although with commensurate increases in runtime.

While nearest-neighbor performance will degrade as n grows large, the current truck capacity limits the max value of n to 16 per route, effectively splitting adversely complex routing problems into manageable sub-routes.

### C5. Software Efficiency and Maintainability
#### Efficiency
- Fast lookups in hash tables ensure minimal overhead.
- The time-managed simulation in `time_sim.py` reduces duplication and error proclivity by precomputing states.
#### Maintainability
- Clear separation of responsibilities—data parsing in `parser.py`, package distribution in `distributor.py`, time simulation in `time_sim.py`, etc.—makes updates straightforward.
- Breaking complex logic into many small, reusable functions and modules enhances maintainability and readability, allowing for easier debugging and testing. Changes in one module will minimally affect the rest.
- Well-placed and informative comments throughout the codebase further enhance comprehension and facilitate smoother collaboration among developers.
- Clearly defined interfaces and docstrings 

### C6. Self-Adjusting Data Structures
Strengths:  
- Custom hash tables automatically manage collisions using a self-adjusting hashing scheme, scaling well on average.
- Insertion, deletion, and lookups often perform in $O(1)$ due to efficient collision handling and dynamic resizing.
Weaknesses:  
- Worst-case collisions can degrade performance to $O(n)$ if the hash table becomes too crowded.
- Hashing requires good distribution for efficiency, meaning poor hashing or excessive collisions can slow performance.

### C7. Data Key
The application will use the package ID as the keys for efficient delivery management because:
- each ID is unique in its own context, ensuring there are no collisions during lookups.
- using a unique ID allows for consistent and accurate tracking of each package object's lifecycle, from intake to delivery.
- the system can locate, update, or remove package data via the relevant, singular identifier, ensuring that each package is individually managed efficiently and without ambiguity.

The application will replicate this for trucks by using unique truck IDs.

## D. Sources
All code is original to this repository. External references for background:  
- [Python 3 Documentation](https://docs.python.org/3/) – For dictionaries and standard libraries.  
- [Morin, P. (2013). Open Data Structures.](https://opendatastructures.org) – For general knowledge on data structures, hashing, algorithms, and complexity notation.