import re
from data.trucks import Truck
from datetime import datetime, timedelta
from router.nearness import nearness
from router.dijkstras_algorithm import dijkstra
from router.nearest_neighbor import nearest_neighbor_algorithm
import random

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
        with open("distributor.txt", "a") as file:
            file.write(f"Package objects at {time_string}: {all_packages}\n")
            file.write(f"all_packages: {[package.pid for package in all_packages]}\n")
        # Late packages is the number of packages arriving on the next flight
        if self.initializing:
            self.packages = sorted(set(package.pid for package in all_packages))
            for package in all_packages:
                package.original = True
            # Find the highest priority number -- this only needs to run once
            self.highest_priority_number = max(package.priority for package in all_packages)
            with open("distributor.txt", "w") as file:
                file.write(f"Initial Distributor Packages: {self.packages}\n")
        
        # If no trucks are at location 0, stop
        available_trucks = [truck.truck_id for truck in self.trucks if truck.current_location == 0]
        if not available_trucks:
            return
        
        # Filter the packages to only include those that are at location 0, have a destination, and are not already on a truck
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
        # Write the filtered packages to the log file
        with open("distributor.txt", "a") as file:
            file.write(f"filtered packages: {[package.pid for package in packages]}\n")

        nearest_destinations = nearness(packages, distances) # returns an ordered list of package ids (package.pid)
        # Write the list to the log file
        with open("distributor.txt", "a") as file:
            file.write(f"Nearest Destinations: {nearest_destinations}\n")
        # Sort the packages so that they match the order of nearest_destinations
        packages = sorted(packages, key=lambda package: nearest_destinations.index(package.pid))
        # Write the package.pid values of the sorted list to the log file
        with open("distributor.txt", "a") as file:
            file.write(f"Sorted Packages: {[package.pid for package in packages]}\n")

        self.late_packages = late_packages
        today = datetime.today().date()
        if not next_flight_time:
            next_flight_time = "17:00"
        time = datetime.combine(today, datetime.strptime(time_string, "%H:%M").time())
        next_flight_time = datetime.combine(today, datetime.strptime(next_flight_time, "%H:%M").time())
        self.time_constraint = (next_flight_time - time) / timedelta(minutes=1) # Convert to minutes

        # Log the packages thus far
        with open("distributor.txt", "a") as file:
            for package in packages:
                file.write(f"Package {package.pid}, priority {package.priority}, original {package.original} | ")
            file.write(f"\n")

        # Load packages into self.buckets by priority rank (1 being the first priority)
        for priority in range(1, self.highest_priority_number + 1):
            for package in packages:
                # If the package.pid is not in self.packages, remove it from the list
                if package.pid not in self.packages:
                    packages.remove(package)
                    continue
                if package.priority == priority and package.pid not in self.loaded_packages and package.pid in self.packages:
                    this_package = package
                    # Check how many packages are in each bucket. Set truck index to the bucket with the fewest packages
                    truck_index = min(range(len(available_trucks)), key=lambda i: len(self.buckets[available_trucks[i]]))
                    # Check the notes for truck requirements
                    match = re.search(r'Can only be on truck (\d+)', package.notes)
                    if match:
                        truck_id = int(match.group(1))
                    else:
                        truck_id = available_trucks[truck_index]
                    destination = package.destination  # read its destination
                    group = package.group  # read its group
                    self.buckets[truck_id].append(package)
                    with open("simulation_states.txt", "a") as file:
                        file.write(f"Package {package.pid} added to truck {truck_id} with priority {package.priority}\n")
                    self.loaded_packages.add(package.pid)  # Mark package as added
                    for pkg in packages:
                        if pkg.pid != this_package.pid and pkg.pid not in self.loaded_packages:
                            if pkg.destination == destination:  # Find other packages with the same destination
                                self.buckets[truck_id].append(pkg)
                                with open("simulation_states.txt", "a") as file:
                                    file.write(f"Destination match: package {pkg.pid} added to truck {truck_id} with priority {pkg.priority}\n")
                                self.loaded_packages.add(pkg.pid)  # Mark package as added
                            elif group and pkg.group == group:  # Find other packages with the same group
                                self.buckets[truck_id].append(pkg)
                                with open("simulation_states.txt", "a") as file:
                                    file.write(f"Group match: package {pkg.pid} added to truck {truck_id} with priority {pkg.priority}\n")
                                self.loaded_packages.add(pkg.pid)  # Mark package as added
    
        # write the contents of each bucket to log
        for truck_id, bucket in self.buckets.items():
            with open("buckets.txt", "a") as file:
                file.write(f"==========Truck {truck_id} bucket at {time}==========\n")
                for package in bucket:
                    file.write(f"Package {package.pid} - Priority {package.priority} - Destination {package.destination}\n")
    
    ###### TODO: Turn this into a stand-alone function so that we can double-check the route after loading all the packages.
    ###### TODO: This will allow for verifying that the route matches the packages loaded onto the truck.
    ###### TODO: Justification: If the number of packages on the route was greater than MAX_CAPACITY, the route will be too long.
        # For building the routes for the trucks
        routes = {truck.truck_id: None for truck in self.trucks}
        with open("distributor.txt", "a") as file:
            file.write("==================ROUTING==================\n")
        for truck_id, bucket in self.buckets.items():
            if bucket:
                # Group destinations by priority levels
                priority_destinations = {}
                for package in bucket:
                    # Handle possible duplicate package objects by verifying the package is in self.packages
                    if package.pid not in self.packages:
                        bucket.remove(package)
                    if package.priority not in priority_destinations:
                        priority_destinations[package.priority] = []
                    priority_destinations[package.priority].append(package.destination)
                with open("distributor.txt", "a") as file:
                    file.write(f"line 143 bucket: {[package.pid for package in bucket]}\n")
                    file.write(f"line 144 priority_destinations: {priority_destinations}\n")

                if not bucket: # If all the packages were removed from the bucket, move to the next bucket
                    continue                      
                
                # Initialize the route variables
                delivery_route = [[0, 0], [(0, 0.0)]]
                complete_route = []
                candidate_route = []
                previous_route_end = 0
                aggregate_time = 0
                aggregate_distance = 0
                
                with open("distributor.txt", "a") as file:
                    file.write(f"====================Routing for truck {truck_id}====================\n")
                    file.write(f"previous_route_end before loop: {previous_route_end}\n")
                
                # Create a sublist of destinations for each priority level
                for priority, destinations in sorted(priority_destinations.items()):
                    sublist = list(set(destinations))  # Remove duplicates
                    # Create a route for each sublist of destinations
                    with open("distributor.txt", "a") as file:
                        file.write(f"Priority {priority} destinations sublist: {sublist}\n")
                    for j in range(1, len(sublist) + 1):
                        sublist_j = sublist[:j]
                        if algo == "dijkstra":
                            new_route = dijkstra(previous_route_end, sublist_j, distances)
                        else:
                            new_route = nearest_neighbor_algorithm(previous_route_end, sublist_j, distances)
                        check_time = aggregate_time + delivery_route[0][1] + new_route[0][1]
                        with open("distributor.txt", "a") as file:
                            file.write(f"Priority {priority} round {j} new route: {new_route}\n")
                            file.write(f"Priority {priority} round {j} delivery route: {delivery_route}\n")
                            file.write(f"Priority {priority} round {j} complete route: {complete_route}\n")
                            file.write(f"Priority {priority} round {j} check time: {check_time}\n")
                        if check_time < self.time_constraint:
                            delivery_distance = delivery_route[0][0] + new_route[0][2]
                            complete_route = self.combine_routes(delivery_route[1], new_route[1], (delivery_route[0][0] + new_route[0][0]), check_time)  # Append the route to the complete route
                            delivery_route = self.combine_routes(delivery_route[1], new_route[1][0:-2], delivery_distance, (delivery_route[0][1] + new_route[0][3]))  # Update the delivery route
                            previous_route_end = delivery_route[1][-1][0]  # Set the end of this route (excluding return to hub) as the start for the next sublist
                            with open("distributor.txt", "a") as file:
                                file.write(f"Route time of {new_route[0][1]} is less than the time constraint of {self.time_constraint}\n")
                                file.write(f"delivery route: {delivery_route}\n")
                                file.write(f"complete route: {complete_route}\n")
                                file.write(f"new previous_route_end: {previous_route_end}\n")
                        else:
                            break  # Stop if the time constraint is exceeded
                    if complete_route:
                        if complete_route[1][0] == (0, 0.0):
                            complete_route[1].pop(0)
                            with open("distributor.txt", "a") as file:
                                file.write(f"Line 192 Removed the hub from the route: {complete_route}\n")
                        candidate_route += complete_route[1]
                    aggregate_distance += delivery_route[0][0]
                    aggregate_time += delivery_route[0][1]
                    print(f"aggregate_time: {aggregate_time}, aggregate_distance: {aggregate_distance}, candidate_route: {candidate_route}")
                
                # Combine all the routes together
                final_route = [[aggregate_distance, aggregate_time], candidate_route]
                print(f"Final route: {final_route}")
                
                with open("distributor.txt", "a") as file:
                    file.write(f"line 199 complete route: {complete_route}\n")
                if complete_route:
                    # Get all the packages from the bucket that match any destination in the complete route
                    packages_to_load = [package for package in bucket if package.destination in [dest[0] for dest in complete_route]]
                    print(f"packages_to_load: {packages_to_load}")
                    for package in packages_to_load:
                        self.load_package(package, truck_id)
                    self.trucks[truck_id].set_route(complete_route[1])
                    self.trucks[truck_id].go()

        self.initializing = False

    # def get_route
    
    def combine_routes(self, old_route, new_route, distance, time):
        identifier = random.randint(0, 1000)
        # Combine the old route with the new route
        combined_route = old_route + new_route
        route = [[distance, time], combined_route]
        with open("route combinator.txt", "a") as file:
            file.write(f"{identifier} Old route: {old_route}\n")
            file.write(f"{identifier} New route: {new_route}\n")
            file.write(f"{identifier} Combined route: {combined_route}\n")
            file.write(f"{identifier} Route {route}\n")
        return route
    
    def load_package(self, package, i):
        print("Running package loader")
        if len(self.trucks[i].packages) < Truck.MAX_CAPACITY:
            try:
                self.packages.remove(package.pid) # If it can't be removed, it was already loaded onto the truck once and shouldn't be loaded again.
            except:
                return
            package.truck_id = self.trucks[i].truck_id
            with open("package loader.txt", "a") as file:
                file.write(f"Loading package {package.pid} onto truck {self.trucks[i].truck_id} - p.tid {package.truck_id}, Destination {package.destination}\n")
                file.write(f"Distributor Packages: {self.packages}\n")
            self.trucks[i].add_package(package)
