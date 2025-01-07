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

    def distribute_packages(self, all_packages, time_string, next_flight_time, late_packages, distances, algo):
        # Late packages is the number of packages arriving on the next flight
        # If no trucks are at location 0, stop
        available_trucks = [truck.truck_id for truck in self.trucks if truck.current_location == 0]
        if not available_trucks:
            return
        packages = [package for package in all_packages if package.truck_id is None and package.location == 0 and package.destination]
        if not packages:
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

        if self.initializing:
            # Find the highest priority number -- this only needs to run once
            self.highest_priority_number = max(package.priority for package in packages)

        # For organizing the packages before loading them into the trucks
        buckets = {truck.truck_id: [] for truck in self.trucks}

        # Load packages by priority rank (1 being the first priority)
        for priority in range(1, self.highest_priority_number + 1):
            truck_index = 0
            for package in packages:
                if package.priority == priority:
                    this_package = package
                    # Check the notes for truck requirements
                    match = re.search(r'Can only be on truck (\d+)', package.notes)
                    if match:
                        truck_id = int(match.group(1))
                    else:
                        truck_id = available_trucks[truck_index]
                    destination = package.destination  # read its destination
                    group = package.group  # read its group
                    buckets[truck_id].append(package)
                    for package in (pkg for pkg in packages if pkg.pid != this_package.pid):  # exclude the current package
                        if package.destination == destination:  # Find other packages with the same destination
                            buckets[truck_id].append(package)
                        if group and package.group == group:  # Find other packages with the same group
                            buckets[truck_id].append(package)
                    # Move to the next truck
                    truck_index = (truck_index + 1) % len(available_trucks)

            # buckets = [bucket for bucket in buckets if bucket]

        # Load priority 0 packages last
        for package in packages:
            truck_index = 0
            if package.notes == "Wrong address listed":
                # skip this package
                continue
            if package.priority == 0:
                this_package = package
                # Check the notes for truck requirements
                match = re.search(r'Can only be on truck (\d+)', package.notes)
                if match:
                    truck_id = int(match.group(1))
                else:
                    truck_id = available_trucks[truck_index]
                destination = package.destination # read its destination
                group = package.group # read its group
                buckets[truck_id].append(package)
                for package in (pkg for pkg in packages if pkg.pid != this_package.pid):
                    if package.destination == destination: # Find other packages with the same destination
                        buckets[truck_id].append(package)
                    if group and package.group == group: # Find other packages with the same group
                        buckets[truck_id].append(package)
                # Move to the next truck
                truck_index = (truck_index + 1) % len(available_trucks)

        # print the contents of each bucket
        for truck_id, bucket in buckets.items():
            print(f"Bucket {truck_id}:")
            for package in bucket:
                print(package)

###### TODO: Turn this into a stand-alone function so that we can double-check the route after loading all the packages.
###### TODO: This will allow for verifying that the route matches the packages loaded onto the truck.
###### TODO: Justification: If the number of packages on the route was greater than MAX_CAPACITY, the route will be too long.
        # For building the routes for the trucks
        routes = {truck.truck_id: None for truck in self.trucks}
        
        for truck_id, bucket in buckets.items():
            if bucket:
                # Create the destinations_list from the sublist. The set() function removes duplicates.
                destinations_list = list(set(item.destination for item in bucket))
                for j in range(1, len(destinations_list) + 1):
                    # Create a sublist of destinations_list that includes from the first element up to index j
                    sublist = destinations_list[:j]
                    if algo == "dijkstra":
                        route = dijkstra(0, destinations_list, distances)
                    else:
                        route = nearest_neighbor_algorithm(0, destinations_list, distances)
                    if route[0][1] < self.time_constraint:  # Read the total time of the returned route and compare it to the time constraint
                        routes[truck_id] = route[1]  # It will work (route[0] is meta data while route[1] is the actual route)
                        continue
                    else:
                        break
                if routes[truck_id]:
                    # Get all the packages from the bucket that match any destination in the route
                    packages_to_load = [package for package in bucket if package.destination in [dest[0] for dest in routes[truck_id]]]
                    for package in packages_to_load:
                        self.load_package(package, truck_id)
                    self.trucks[truck_id].set_route(routes[truck_id])
                    self.trucks[truck_id].go()
###### TODO: End of stand-alone function

        self.initializing = False

    def load_package(self, package, i):
        if len(self.trucks[i].packages) < Truck.MAX_CAPACITY:
            package.truck_id = self.trucks[i].truck_id
            print(f"Loading package {package.pid} onto truck {self.trucks[i].truck_id} - {package.truck_id}")
            self.trucks[i].add_package(package)