import re
from data.trucks import Truck
from datetime import datetime, timedelta
from router.nearness import nearness
from router.dijkstras_algorithm import dijkstra
from router.nearest_neighbor import nearest_neighbor_algorithm

class Distributor:
    def __init__(self, trucks):
        self.trucks = trucks
        self.late_packages = 0
        self.time_constraint = 0
        self.distance_constraint = 0
        self.trucks[0].current_location = -1 # Ignore truck 0 since there are only two drivers
        self.initializing = True
        self.highest_priority_number = 0
        self.buckets = {truck.truck_id: [] for truck in self.trucks}
        self.loaded_packages = set() # Track which packages were already added to buckets to avoid duplicates
        self.packages = set() # To track which packages have not yet been distributed

    def distribute_packages(self, all_packages, time_string, next_flight_time, late_packages, distances, algo):
        with open("distributor packages.txt", "a") as file:
            file.write(f"Package objects at {time_string}: {all_packages}\n")
        # Late packages is the number of packages arriving on the next flight

        if self.initializing:
            self.packages = sorted(set(package.pid for package in all_packages))
            for package in all_packages:
                package.original == True
            # Find the highest priority number -- this only needs to run once
            self.highest_priority_number = max(package.priority for package in all_packages)
            with open("distributor packages.txt", "w") as file:
                file.write(f"Initial Distributor Packages: {self.packages}\n")
        
        # If no trucks are at location 0, stop
        available_trucks = [truck.truck_id for truck in self.trucks if truck.current_location == 0]
        if not available_trucks:
            return
        packages = [package for package in all_packages if 
                    package.truck_id is None and 
                    package.location == 0 and 
                    package.destination and
                    package.pid in self.packages]
        if packages:
            for package in packages:
                if not package.original:
                    packages.remove(package)
        else:
            return
        nearest_destinations = nearness(packages, distances) # returns an ordered list of package ids (package.pid)
        # Sort the packages so that they match the order of nearest_destinations
        packages = sorted(packages, key=lambda package: nearest_destinations.index(package.pid))
        self.late_packages = late_packages
        today = datetime.today().date()
        if not next_flight_time:
            next_flight_time = "17:00"
        time = datetime.combine(today, datetime.strptime(time_string, "%H:%M").time())
        next_flight_time = datetime.combine(today, datetime.strptime(next_flight_time, "%H:%M").time())
        self.time_constraint = (next_flight_time - time) / timedelta(minutes=1) # Convert to minutes

        # Load packages by priority rank (1 being the first priority)
        for priority in range(1, self.highest_priority_number + 1):
            # Check how many packages are in each bucket. Set truck index to the bucket with the fewest packages
            truck_index = min(range(len(available_trucks)), key=lambda i: len(self.buckets[available_trucks[i]]))
            for package in packages:
                # If the package.pid is not in self.packages, remove it from the list
                if package.pid not in self.packages:
                    packages.remove(package)
                    continue
                if package.priority == priority and package.pid not in self.loaded_packages and package.pid in self.packages:
                    this_package = package
                    # Check the notes for truck requirements
                    match = re.search(r'Can only be on truck (\d+)', package.notes)
                    if match:
                        truck_id = int(match.group(1))
                    else:
                        truck_id = available_trucks[truck_index]
                    destination = package.destination  # read its destination
                    group = package.group  # read its group
                    self.buckets[truck_id].append(package)
                    self.loaded_packages.add(package.pid)  # Mark package as added
                    for pkg in packages:
                        if pkg.pid != this_package.pid and pkg.pid not in self.loaded_packages:
                            if pkg.destination == destination:  # Find other packages with the same destination
                                self.buckets[truck_id].append(pkg)
                                self.loaded_packages.add(pkg.pid)  # Mark package as added
                            elif group and pkg.group == group:  # Find other packages with the same group
                                self.buckets[truck_id].append(pkg)
                                self.loaded_packages.add(pkg.pid)  # Mark package as added
                truck_index = min(range(len(available_trucks)), key=lambda i: len(self.buckets[available_trucks[i]]))

        
        # Load priority 0 packages last
        for package in packages:
            # Check how many packages are in each bucket. Set truck index to the bucket with the fewest packages
            truck_index = min(range(len(available_trucks)), key=lambda i: len(self.buckets[available_trucks[i]]))            # If the package.pid is not in self.packages, remove it from the list
            if package.pid not in self.packages:
                packages.remove(package)
                continue
            if package.notes == "Wrong address listed":
                # skip this package
                continue
            if package.priority == 0 and package.pid not in self.loaded_packages and package.pid in self.packages:
                this_package = package
                # Check the notes for truck requirements
                match = re.search(r'Can only be on truck (\d+)', package.notes)
                if match:
                    truck_id = int(match.group(1))
                else:
                    truck_id = available_trucks[truck_index]
                destination = package.destination  # read its destination
                group = package.group  # read its group
                self.buckets[truck_id].append(package)
                self.loaded_packages.add(package.pid)  # Mark package as added
                for pkg in packages:
                    if pkg.pid != this_package.pid and pkg.pid not in self.loaded_packages:
                        if pkg.destination == destination:  # Find other packages with the same destination
                            self.buckets[truck_id].append(pkg)
                            self.loaded_packages.add(pkg.pid)  # Mark package as added
                        elif group and pkg.group == group:  # Find other packages with the same group
                            self.buckets[truck_id].append(pkg)
                            self.loaded_packages.add(pkg.pid)  # Mark package as added
                # Move to the next truck, alternating between indexes 0 and 1
                truck_index = min(range(len(available_trucks)), key=lambda i: len(self.buckets[available_trucks[i]]))  
    
        # print the contents of each bucket
        for truck_id, bucket in self.buckets.items():
            with open("simulation_states.txt", "a") as file:
                file.write(f"Truck {truck_id} bucket:\n")
                for package in bucket:
                    file.write(f"Package {package.pid} - {package.destination}\n")
    
    ###### TODO: Turn this into a stand-alone function so that we can double-check the route after loading all the packages.
    ###### TODO: This will allow for verifying that the route matches the packages loaded onto the truck.
    ###### TODO: Justification: If the number of packages on the route was greater than MAX_CAPACITY, the route will be too long.
        # For building the routes for the trucks
        routes = {truck.truck_id: None for truck in self.trucks}
        
        for truck_id, bucket in self.buckets.items():
            if bucket:
                # Group destinations by priority levels
                priority_destinations = {}
                for package in bucket:
                    # Handle possible duplicate package objects by making sure the package is in self.packages
                    if package.pid not in self.packages:
                        bucket.remove(package)
                    
                    if package.priority not in priority_destinations:
                        priority_destinations[package.priority] = []
                    priority_destinations[package.priority].append(package.destination)

                if not bucket: # If all the packages were removed from the bucket, move to the next bucket
                    continue                
                # Get the top priority level in the bucket, excluding priority 0
                non_zero_priorities = [package.priority for package in bucket if package.priority != 0]
                if non_zero_priorities:
                    top_priority_level = min(non_zero_priorities)
                else:
                    top_priority_level = 0  # Default to 0 if no non-zero priorities are found
                
                # Determine the initial previous_route_end using the nearness function on the top priority packages
                top_priority_packages = [package for package in bucket if package.priority == top_priority_level]
                if top_priority_packages:
                    print(f"top_priority_packages: {top_priority_packages}")
                    nearest_destinations = nearness(top_priority_packages, distances)
                    print(f"nearest_destinations: {nearest_destinations}")
                    if not nearest_destinations:
                        previous_route_end = top_priority_packages[0].destination
                        print(f"No nearest destinations found. Setting previous_route_end to {previous_route_end}")
                    # Match nearest_destinations[0] to a package.pid in the bucket and get its package.destination
                    else:
                        for package in bucket:
                            if nearest_destinations and package.pid == nearest_destinations[0]:
                                previous_route_end = package.destination
                                break
                        
                
                # Initialize the complete route
                complete_route = []

                # Create a sublist of destinations for each priority level
                for priority, destinations in sorted(priority_destinations.items()):
                    sublist = list(set(destinations))  # Remove duplicates
                    # Create a route for each sublist of destinations
                    for j in range(1, len(sublist) + 1):
                        sublist_j = sublist[:j]
                        if algo == "dijkstra":
                            route = dijkstra(previous_route_end, sublist_j, distances)
                        else:
                            route = nearest_neighbor_algorithm(previous_route_end, sublist_j, distances)
                        if route[0][1] < self.time_constraint:  # Read the total time at index route[0][1] of the returned route and compare it to the time constraint
                            complete_route.extend(route[1])  # Append the route to the complete route
                            previous_route_end = route[1][-1][0]  # Set the end of this route as the start for the next sublist
                            continue
                        else:
                            break
                
                if complete_route:
                    # Get all the packages from the bucket that match any destination in the complete route
                    packages_to_load = [package for package in bucket if package.destination in [dest[0] for dest in complete_route]]
                    for package in packages_to_load:
                        self.load_package(package, truck_id)
                    self.trucks[truck_id].set_route(complete_route)
                    self.trucks[truck_id].go()

        self.initializing = False

    def load_package(self, package, i):
        if len(self.trucks[i].packages) < Truck.MAX_CAPACITY:
            try:
                self.packages.remove(package.pid) # If it can't be removed, it was already loaded onto the truck once and shouldn't be loaded again.
            except:
                return
            package.truck_id = self.trucks[i].truck_id
            with open("distributor packages.txt", "a") as file:
                file.write(f"Loading package {package.pid} onto truck {self.trucks[i].truck_id} - {package.truck_id}, Destination {package.destination}\n")
                file.write(f"Distributor Packages: {self.packages}\n")
            self.trucks[i].add_package(package)
