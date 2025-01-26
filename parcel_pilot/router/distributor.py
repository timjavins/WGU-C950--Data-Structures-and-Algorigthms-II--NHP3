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
        self.bucket_packages = set() # Track which packages were already added to buckets to avoid duplicates
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
            self.initializing = False
        
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
                if package.priority == priority and package.pid not in self.bucket_packages and package.pid in self.packages:
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
                    self.bucket_packages.add(package.pid)  # Mark package as added
                    for pkg in packages:
                        if pkg.pid != this_package.pid and pkg.pid not in self.bucket_packages:
                            if pkg.destination == destination:  # Find other packages with the same destination
                                self.buckets[truck_id].append(pkg)
                                with open("simulation_states.txt", "a") as file:
                                    file.write(f"Destination match: package {pkg.pid} added to truck {truck_id} with priority {pkg.priority}\n")
                                self.bucket_packages.add(pkg.pid)  # Mark package as added
                            elif group and pkg.group == group:  # Find other packages with the same group
                                self.buckets[truck_id].append(pkg)
                                with open("simulation_states.txt", "a") as file:
                                    file.write(f"Group match: package {pkg.pid} added to truck {truck_id} with priority {pkg.priority}\n")
                                self.bucket_packages.add(pkg.pid)  # Mark package as added
    
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
                for package in bucket:
                    # Handle possible duplicate package objects by verifying the package is in self.packages
                    if package.pid not in self.packages:
                        bucket.remove(package)
                with open("distributor.txt", "a") as file:
                    file.write(f"line 143 bucket: {[package.pid for package in bucket]}\n")

                if not bucket: # If all the packages were removed from the bucket, move to the next bucket
                    continue                      
                
                # Initialize the route variables
                route_dict = {}
                aggregate_time = 0
                aggregate_distance = 0
                previous_route_end = 0
                
                with open("distributor.txt", "a") as file:
                    file.write(f"====================Routing for truck {truck_id}====================\n")
                    file.write(f"previous_route_end before loop: {previous_route_end}\n")

                # # Upgrade grouped packages to the highest priority level among the group
                # group_list = []
                # for package in packages:
                #     if package.group and package.group not in group_list:
                #         group_list.append(package.group)
                # for x in group_list:
                #     this_group = [pkg for pkg in packages if pkg.group == x]
                #     print(f"Group {x}: {[pkg.pid for pkg in this_group]}")
                #     highest_priority = min(pkg.priority for pkg in this_group) # The lower the priority number, the higher the priority
                #     for pkg in this_group:
                #         pkg.priority = highest_priority
                
                # Find packages for each priority level, check if they have a package.group, group them with the same group, send them out
                truck_sent = False
                for priority in range(1, self.highest_priority_number + 1):
                    for package in bucket:
                        if package.priority == priority:
                            group = package.group
                            if group: # If the package has a group, find all other packages with the same group or destination or priority
                                group_packages = [pkg for pkg in bucket if pkg.group == group or pkg.priority == priority]
                                destinations = []
                                destinations += [pkg.destination for pkg in group_packages]
                                destinations = set(destinations)  # Remove duplicates
                                group_packages += [pkg for pkg in bucket if pkg.destination in destinations]
                                group_packages = set(group_packages) # Ensure there are no duplicates
                                # Get the route for this group of packages
                                route = self.get_route(group_packages, distances, algo)
                                # Send the packages out
                                self.send_it(group_packages, truck_id, route, time, distances)
                                truck_sent = True
                                break
                    if truck_sent:
                        break
                if truck_sent:
                    continue
                
                # Handle the remaining packages
                queue = []
                for priority in range(1, self.highest_priority_number + 1):
                    for package in bucket:
                        if package.priority == priority:
                            queue.append(package)
                            if len(queue) == 16:
                                break
                        for pkg in bucket:
                            if pkg.destination == package.destination and pkg not in queue and len(queue) < 16:
                                queue.append(pkg)
                            if len(queue) == 16:
                                break
                    if len(queue) == 16:
                        break
                route = self.get_route(queue, distances, algo)
                self.send_it(queue, truck_id, route, time, distances)

    def get_route(self, packages, distances, algo):
        routes = {}
        previous_route_end = 0
        for priority in range(1, self.highest_priority_number + 1):
            destinations = []
            for package in packages:
                if package.priority == priority and package.destination not in destinations:
                    destinations.append(package.destination)
            destinations = set(destinations) # ensure no duplicates
            if algo == "dijkstra":
                route = dijkstra(previous_route_end, destinations, distances)
            else:
                route = nearest_neighbor_algorithm(previous_route_end, destinations, distances)
            # add the route to the routes dictionary with the priority as the key
            routes[priority] = route
            try:
                previous_route_end = route[1][-1][0]
            except:
                break
        # combine all the routes from the dictionary into final route
        final_route = [0, 0], []
        for priority in sorted(routes.keys()):
            full_route = routes[priority]
            final_route[0][0] += full_route[0][0]  # sum total distances
            final_route[0][1] += full_route[0][1]  # sum total times
            final_route[1].extend(full_route[1])  # concatenate routes
        with open("routing.txt", "a") as file:
            # Log all the variables in this function
            file.write(f"Final Route: {final_route}\n")
        return final_route
    
    def send_it(self, packages, i, route, time, distances):
        # Add destination 0 to the end of the final route
        if route[1]:
            last_destination = route[1][-1][0]
            distance_to_hub = distances[last_destination][0] if last_destination in distances and 0 in distances[last_destination] else distances[0][last_destination]
            route[1].append((0, distance_to_hub))
            route[0][0] += distance_to_hub
            route[0][1] += distance_to_hub / 0.3

            for package in packages:
                self.load_package(package, i, time)
            self.trucks[i].set_route(route[1])
            self.trucks[i].go()
            with open("simulation_states.txt", "a") as file:
                file.write(f"==============Sending Truck {i} at {time}==============\n")
                file.write(f"Truck {i} route: {route}\n")
                file.write(f"Truck {i} packages: {[package.pid for package in self.trucks[i].packages]}\n")
                file.write(f"Truck {i} bucket: {[package.pid for package in self.buckets[i]]}\n")

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
    
    def load_package(self, package, i, time):
        if len(self.trucks[i].packages) < Truck.MAX_CAPACITY:
            with open("package loader.txt", "a") as file:
                file.write(f"Distributor packages at {time}: {self.packages}\n")
                file.write(f"Truck {i} bucket: {[package.pid for package in self.buckets[i]]}\n")
            try:
                self.packages.remove(package.pid) # If it can't be removed, it was already loaded onto the truck once and shouldn't be loaded again.
                self.buckets[i].remove(package)
            except:
                return
            package.truck_id = self.trucks[i].truck_id
            with open("package loader.txt", "a") as file:
                file.write(f"Loading package {package.pid} onto truck {self.trucks[i].truck_id} - p.tid {package.truck_id}, Destination {package.destination}\n")
                file.write(f"Distributor Packages: {self.packages}\n")
                file.write(f"Truck {i} bucket: {[package.pid for package in self.buckets[i]]}\n")
            self.trucks[i].add_package(package)
