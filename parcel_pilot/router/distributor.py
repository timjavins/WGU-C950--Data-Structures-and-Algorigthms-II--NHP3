import re
from data.trucks import Truck
from datetime import datetime, timedelta
from router.nearness import nearness
from router.dijkstras_algorithm import dijkstra
from router.nearest_neighbor import nearest_neighbor_algorithm
import random
import traceback

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
        self.bucket_destinations = {truck.truck_id: [] for truck in self.trucks}
        self.bucket_packages = set() # Track which packages were already added to buckets to avoid duplicates
        self.packages = set() # To track which packages have not yet been distributed

    def distribute_packages(self, all_packages, time_string, next_flight_time, late_packages, distances, graph, algo):
        with open("distributor.txt", "a") as file:
            file.write(f"Package objects at {time_string}: {all_packages}\n")
            file.write(f"all_packages: {[package.pid for package in all_packages]}\n")
        # Late packages is the number of packages arriving on the next flight (potentially for planning or analytics)
        self.late_packages = late_packages

        if self.initializing:
            self.initializing = self.initialize(all_packages)

        today = datetime.today().date()
        if not next_flight_time:
            next_flight_time = "17:00"
        time = datetime.combine(today, datetime.strptime(time_string, "%H:%M").time())
        next_flight_time = datetime.combine(today, datetime.strptime(next_flight_time, "%H:%M").time())
        self.time_constraint = (next_flight_time - time) / timedelta(minutes=1) # Convert to minutes
        
        # If no trucks are at location 0, stop
        available_trucks = [truck.truck_id for truck in self.trucks if truck.current_location == 0]
        with open("distributor.txt", "a") as file:
            file.write(f"Available trucks at {time}: {available_trucks}\n")
        if not available_trucks:
            return
        
        # Clean the package list
        packages = self.clean_package_list(all_packages)\
        # If there are no packages to distribute, stop
        if not packages:
            with open("distributor.txt", "a") as file:
                file.write(f"No packages to distribute at {time}\n")
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


        # Log the packages thus far
        with open("distributor.txt", "a") as file:
            for package in packages:
                file.write(f"Package {package.pid}, priority {package.priority}, original {package.original} | ")
            file.write(f"\n")

        self.check_for_assigned_truck(packages)
        self.check_priority(packages, available_trucks, time) # TODO: remove time after removing logging        
    
        # write the contents of each bucket to log
        for truck_id, bucket in self.buckets.items():
            with open("buckets.txt", "a") as file:
                file.write(f"==========Truck {truck_id} bucket at {time}==========\n")
                for package in bucket:
                    file.write(f"Package {package.pid} - Priority {package.priority} - Destination {package.destination}\n")

        # Now that the buckets are assigned, build the routes for the trucks
        with open("distributor.txt", "a") as file:
            file.write("==================ROUTING==================\n")

        self.process_buckets(distances, graph, algo, time)

    def initialize(self, all_packages):
            self.packages = sorted(set(package.pid for package in all_packages))
            for package in all_packages:
                package.original = True
            # Find the highest priority number
            self.highest_priority_number = max(package.priority for package in all_packages)
            with open("distributor.txt", "w") as file:
                file.write(f"Initial Distributor Packages: {self.packages}\n")
            return False
    
    def clean_package_list(self, all_packages):
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
            return packages
        else:
            return None

    def check_for_assigned_truck(self, packages):
        # For packages with truck requirements, assign them to the truck with the matching truck_id
        for package in packages:
            match = re.search(r'Can only be on truck (\d+)', package.notes)
            if match:
                truck_id = int(match.group(1))
                self.put_in_bucket(package, truck_id)
                self.check_group(package, packages, truck_id)

    def check_group(self, package, packages, truck_id):
        if package.group:
            for pkg in packages:
                if pkg.group == package.group and pkg.pid not in self.bucket_packages:
                    self.put_in_bucket(pkg, truck_id)

    def check_destination(self, package):
        for truck_id, destinations in self.bucket_destinations.items():
            if package.destination in destinations:
                self.put_in_bucket(package, truck_id)
                return True
        return None

    def check_priority(self, packages, available_trucks, time):
        # Load packages into self.buckets by priority rank (1 being the first priority)
        for priority in range(1, self.highest_priority_number + 1):
            for package in packages:
                # If the package.pid is not in self.packages, remove it from the list
                if package.pid not in self.packages:
                    packages.remove(package)
                    continue
                # If the package has the same priority as the current priority, is not in a bucket, and is in the list of packages
                if package.priority == priority and package.pid not in self.bucket_packages and package.pid in self.packages:
                    # Check how many packages are in each bucket. Set truck index to the bucket with the fewest packages
                    truck_index = min(range(len(available_trucks)), key=lambda i: len(self.buckets[available_trucks[i]]))
                    self.check_group(package, packages, available_trucks[truck_index])
                    if self.check_destination(package):
                        continue
                    truck_id = available_trucks[truck_index]
                    self.put_in_bucket(package, truck_id)
                    for package in packages:
                        self.check_destination(package)
                    with open("simulation_states.txt", "a") as file:
                        file.write(f"{time}: Package {package.pid} added to truck {truck_id} with priority {package.priority}\n")

    def put_in_bucket(self, package, truck_id):
        if package.pid not in self.bucket_packages:
            self.buckets[truck_id].append(package)
            self.bucket_destinations[truck_id].append(package.destination) if package.destination not in self.bucket_destinations[truck_id] else None
            self.bucket_packages.add(package.pid)  # Mark package as added
        else:
            with open("distributor.txt", "a") as file:
                file.write(f"Package {package.pid} was already added to a bucket.\n")

    def process_buckets(self, distances, graph, algo, time):
        for truck_id, bucket in self.buckets.items():
            if not self.trucks[truck_id].current_location == 0: # Don't process the bucket for the truck if not at location 0
                with open("distributor.txt", "a") as file:
                    file.write(f"Truck {truck_id} is not at location 0. Skipping.\n")
                continue
            if bucket:
                for package in bucket:
                    # Handle possible duplicate package objects by verifying the package is in self.packages
                    if package.pid not in self.packages:
                        bucket.remove(package)
                with open("distributor.txt", "a") as file:
                    file.write(f"line 143 bucket: {[package.pid for package in bucket]}\n")

                if not bucket: # If all the packages were removed from the bucket, move to the next bucket
                    continue
                
                with open("distributor.txt", "a") as file:
                    file.write(f"====================Routing for truck {truck_id}====================\n")

                if self.process_groups(bucket, truck_id, distances, graph, algo, time):
                    continue

                self.process_ungrouped(bucket, truck_id, distances, graph, algo, time)

    def process_groups(self, bucket, truck_id, distances, graph, algo, time):
        # For one priority level at a time, check if they have a package.group, group them with the same group, send them out
        for priority in range(1, self.highest_priority_number + 1):
            for package in bucket:
                if package.priority == priority:
                    if package.group: # If the package has a group, find all other packages with the same group or destination or priority
                        group_packages = [pkg for pkg in bucket if pkg.group == package.group or pkg.priority == priority] # List of the grouped packages
                        destinations = [pkg.destination for pkg in group_packages] # List of the destinations for this group
                        destinations = set(destinations)  # Remove duplicates
                        group_packages += [pkg for pkg in bucket if pkg.destination in destinations] # Add all packages that match the group's destinations
                        group_packages = set(group_packages) # Ensure there are no duplicates
                        # Get the route for this group of packages
                        route = self.get_route(group_packages, distances, graph, algo, time)
                        # Send the packages out
                        self.send_it(group_packages, truck_id, route, time, distances)
                        return True
        return False
    
    def process_ungrouped(self, bucket, truck_id, distances, graph, algo, time):
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
        with open("distributor.txt", "a") as file:
            file.write(f"{time} -- truck {truck_id} queue: {[package.pid for package in queue]}\n")
        route = self.get_route(queue, distances, graph, algo, time)
        self.send_it(queue, truck_id, route, time, distances)

    def get_route(self, packages, distances, graph, algo, time):
        with open("routing.txt", "a") as file:
            file.write(f"{time}: Getting route for packages {[package.pid for package in packages]}\n")
        routes = {}
        previous_route_end = 0
        already_processed = []
        for priority in range(1, self.highest_priority_number + 1):
            with open("routing.txt", "a") as file:
                file.write(f"Priority: {priority}\n")
            destinations = []
            for package in packages:
                if package.priority == priority and package.destination not in destinations and package.destination not in already_processed:
                    with open("routing.txt", "a") as file:
                        file.write(f"Package {package.pid} priority of {package.priority} matched priority {priority} and has destination: {package.destination}\n")
                    destinations.append(package.destination)
            if not destinations:
                continue
            destinations = set(destinations) # ensure no duplicates
            already_processed += destinations
            with open("routing.txt", "a") as file:
                file.write(f"Destinations: {destinations}\n")
            if algo == "dijkstra":
                route = dijkstra(graph, previous_route_end, destinations)
            else:
                route = nearest_neighbor_algorithm(previous_route_end, destinations, distances)
            # add the route to the routes dictionary with the priority as the key
            routes[priority] = route
            with open("routing.txt", "a") as file:
                file.write(f"Route for priority {priority}: {route}\n")
            try:
                with open("routing.txt", "a") as file:
                    file.write(f"Previous route end: {previous_route_end}. Attempting to change.\n")
                previous_route_end = route[1][-1][0]
            except Exception as e:
                with open("routing.txt", "a") as file:
                    file.write(f"An error occurred: {str(e)}\n")
                    file.write(traceback.format_exc())
                    file.write(f"Previous route end: {previous_route_end}. No change.\n")
                break
        # combine all the routes from the dictionary into final route
        final_route = [0, 0], []
        for priority in sorted(routes.keys()):
            full_route = routes[priority]
            final_route[0][0] += full_route[0][0]  # sum tota`l distances
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
