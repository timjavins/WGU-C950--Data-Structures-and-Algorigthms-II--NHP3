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
        package_ids = ", ".join(package.pid for package in packages)
        self.late_packages = late_packages
        today = datetime.today().date()
        if not next_flight_time:
            next_flight_time = "17:00"
        time = datetime.combine(today, datetime.strptime(time_string, "%H:%M").time())
        next_flight_time = datetime.combine(today, datetime.strptime(next_flight_time, "%H:%M").time())
        self.time_constraint = (next_flight_time - time) / timedelta(minutes=1) # Convert to minutes

        if self.initializing:
            # Find the highest priority number
            self.highest_priority_number = max(package.priority for package in packages)
        
        # For organizing the packages before loading them into the trucks
        bucket0 = []
        bucket1 = []
        bucket2 = []
        buckets = [bucket0, bucket1, bucket2]

        # For building the routes for the trucks
        route0 = []
        route1 = []
        route2 = []
        routes = [route0, route1, route2]

        # Load packages by priority rank (1 being the first priority)
        for priority in range(1, self.highest_priority_number + 1):
            i = 0
            for package in packages:
                if package.priority == priority:
                    destination = package.destination # read its destination
                    group = package.group # read its group
                    buckets[i].append(package)
                    for package in packages:
                        if package.destination == destination: # Find other packages with the same destination
                            buckets[i].append(package)
                        if group and package.group == group: # Find other packages with the same group
                            buckets[i].append(package)
            if i == (len(available_trucks) - 1):
                i = 0
            else:
                i += 1

            # Check the notes for truck requirements
            # match = re.search(r'Can only be on truck (\d+)', package.notes)
            # if match:
            #     truck_id = int(match.group(1))
            #     truck = self.trucks[truck_id]
            #     if len(truck.packages) < Truck.MAX_CAPACITY:
            #         package.truck_id = truck_id
            #         print(f"Loading package {package.pid} onto truck {truck_id} - {package.truck_id}")
            #         truck.add_package(package)

        # Load priority 0 packages last
        i = 0
        for package in packages:
            if package.notes == "Wrong address listed":
                # skip this package
                continue
            if package.priority == 0:
                destination = package.destination # read its destination
                group = package.group # read its group
                buckets[i].append(package)
                for package in packages:
                    if package.destination == destination: # Find other packages with the same destination
                        buckets[i].append(package)
                    if group and package.group == group: # Find other packages with the same group
                        buckets[i].append(package)
        if i == (len(available_trucks) - 1):
            i = 0
        else:
            i += 1

        # get the routes for each truck
        i = 0
        for bucket in buckets:
            if bucket:
                for j in range(1, len(bucket[i]) + 1):
                    # Create a sublist of bucket[i] that includes elements from the start up to the current index j
                    sublist = bucket[i][:j]
                    # Create the destinations_list from the sublist
                    destinations_list = [item.destination for item in sublist]
                    if algo == "dijkstra":
                        route = dijkstra(0, destinations_list, distances)
                    else:
                        route = nearest_neighbor_algorithm(0, destinations_list, distances)
                    if route[0][1] < self.time_constraint: # Read the total time of the returned route and compare it to the time constraint
                        routes[i] = route # It will work
                    else:
                        break
                if routes[i]:
                    # get all the packages from bucket[i] that match the destinations in the route
                    packages_to_load = [package for package in bucket[i] if package.destination in [item[0] for item in route]]
                    for package in packages_to_load:
                        self.load_package(package, i)
                self.trucks[i].set_route(routes[i])
                self.trucks[i].go()
            i += 1
        
        self.initializing = False

    def load_package(self, package, i):
        if len(self.trucks[i].packages) < Truck.MAX_CAPACITY:
            package.truck_id = self.trucks[i].truck_id
            print(f"Loading package {package.pid} onto truck {self.trucks[i].truck_id} - {package.truck_id}")
            self.trucks[i].add_package(package)