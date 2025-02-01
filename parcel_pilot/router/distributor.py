"""
This module contains the Distributor class, which is responsible for distributing packages to trucks, based on priority and constraints, and determining their delivery routes.

Classes
-------
Distributor
    A class that manages the distribution of packages to trucks and determines their delivery routes.

Functions
---------
distribute_packages(all_packages, time_string, next_flight_time, late_packages, distances, graph, algo)
    Distributes packages to trucks and determines their delivery routes based on the given algorithm.

initialize(all_packages)
    Initializes the Distributor with the given packages.

clean_package_list(all_packages)
    Cleans the package list to include only those packages that are ready for distribution.
"""

import re
from data.trucks import Truck
from datetime import datetime, timedelta
from router.nearness import nearness
from router.dijkstras_algorithm import dijkstra
from router.nearest_neighbor import nearest_neighbor_algorithm

class Distributor:
    """
    A class that manages the distribution of packages to trucks and determines their delivery routes.

    Attributes
    ----------
    trucks : list
        The list of trucks.
    late_packages : int
        The number of late packages.
    time_constraint : int
        The time constraint for the delivery.
    distance_constraint : int
        The distance constraint for the delivery.
    initializing : bool
        Flag to indicate if the distributor is initializing.
    highest_priority_number : int
        The highest priority number among the packages.
    buckets : dict
        A dictionary containing the packages assigned to each truck.
    bucket_destinations : dict
        A dictionary containing the destinations assigned to each truck.
    bucket_packages : set
        A set of packages that have already been added to buckets.
    packages : set
        A set of packages that have not yet been distributed.
    """

    def __init__(self, trucks):
        """
        Initializes the Distributor with the given trucks.

        Parameters
        ----------
        trucks : list
            The list of trucks.
        """
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
        """
        Distributes packages to trucks and determines their delivery routes based on the given algorithm.

        Parameters
        ----------
        all_packages : list
            The list of all packages.
        time_string : str
            The current time in 24-hour format (HH:MM).
        next_flight_time : str
            The time of the next flight in 24-hour format (HH:MM).
        late_packages : int
            The number of late packages.
        distances : dict
            The dictionary containing distances between locations.
        graph : dict
            The graph representation of the delivery locations.
        algo : function
            The algorithm used for routing.

        Returns
        -------
        None

        Space Complexity
        ---------------
            O(n)

        Time Complexity
        ---------------
            O(n^2)
        """
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
        if not available_trucks:
            return
        
        # Clean the package list
        packages = self.clean_package_list(all_packages)
        # If there are no packages to distribute, stop
        if not packages:
            return

        nearest_destinations = nearness(packages, distances) # returns an ordered list of package ids (package.pid)

        # Sort the packages so that they match the order of nearest_destinations
        packages = sorted(packages, key=lambda package: nearest_destinations.index(package.pid))

        self.check_for_assigned_truck(packages)
        self.check_priority(packages, available_trucks)    

        # Now that the buckets are assigned, build the routes for the trucks
        self.process_buckets(distances, graph, algo)

    def initialize(self, all_packages):
        """
        Initializes the Distributor with data from the given packages and marks those packages as original.

        Parameters
        ----------
        all_packages : list
            The list of all packages.

        Returns
        -------
        bool
            False after initialization is complete.

        Space Complexity
        ---------------
            O(n)

        Time Complexity
        ---------------
            O(n)
        """
        self.packages = sorted(set(package.pid for package in all_packages))
        for package in all_packages:
            package.original = True
        # Find the highest priority number
        self.highest_priority_number = max(package.priority for package in all_packages)
        return False
    
    def clean_package_list(self, all_packages):
        """
        Cleans the package list to include only those packages that are ready for distribution.

        Parameters
        ----------
        all_packages : list
            The list of all packages.

        Returns
        -------
        list
            The cleaned list of packages.

        Space Complexity
        ---------------
            O(n)

        Time Complexity
        ---------------
            O(n)
        """
        # Filter the packages to only include those that are at location 0, have a destination, and are not already on a truck
        packages = [package for package in all_packages if 
                    package.truck_id is None and 
                    package.location == 0 and 
                    package.destination and
                    package.pid in self.packages]
        if packages:
            for package in packages:
                if not package.original: # Ensures the package is the original object, not a duplicate
                    packages.remove(package)
            return packages
        else:
            return None

    def check_for_assigned_truck(self, packages):
        """
        Assigns packages with specific truck requirements to the corresponding truck.
    
        Parameters
        ----------
        packages : list
            The list of packages.
    
        Returns
        -------
        None
    
        Space Complexity
        ---------------
            O(n)
    
        Time Complexity
        ---------------
            O(n)
        """
        for package in packages:
            match = re.search(r'Can only be on truck (\d+)', package.notes)
            if match:
                truck_id = int(match.group(1))
                self.put_in_bucket(package, truck_id)
                self.check_group(package, packages, truck_id)
    
    def check_group(self, package, packages, truck_id):
        """
        Assigns all packages in the same group to the specified truck.
    
        Parameters
        ----------
        package : object
            The package object.
        packages : list
            The list of packages.
        truck_id : int
            The ID of the truck.
    
        Returns
        -------
        None
    
        Space Complexity
        ---------------
            O(n)
    
        Time Complexity
        ---------------
            O(n)
        """
        if package.group:
            for pkg in packages:
                if pkg.group == package.group and pkg.pid not in self.bucket_packages:
                    self.put_in_bucket(pkg, truck_id)
    
    def check_destination(self, package):
        """
        Checks if the package's destination is already assigned to a truck.
    
        Parameters
        ----------
        package : object
            The package object.
    
        Returns
        -------
        bool
            True if the package's destination is already assigned to a truck, otherwise False.
    
        Space Complexity
        ---------------
            O(n)
    
        Time Complexity
        ---------------
            O(n)
        """
        for truck_id, destinations in self.bucket_destinations.items():
            if package.destination in destinations:
                self.put_in_bucket(package, truck_id)
                return True
        return None
    
    def check_priority(self, packages, available_trucks):
        """
        Loads packages into trucks based on their priority rank.
    
        Parameters
        ----------
        packages : list
            The list of packages.
        available_trucks : list
            The list of available trucks.
    
        Returns
        -------
        None
    
        Space Complexity
        ---------------
            O(n)
    
        Time Complexity
        ---------------
            O(n^2)
        """
        for priority in range(1, self.highest_priority_number + 1):
            for package in packages:
                if package.pid not in self.packages:
                    packages.remove(package)
                    continue
                if package.priority == priority and package.pid not in self.bucket_packages and package.pid in self.packages:
                    truck_index = min(range(len(available_trucks)), key=lambda i: len(self.buckets[available_trucks[i]]))
                    self.check_group(package, packages, available_trucks[truck_index])
                    if self.check_destination(package):
                        continue
                    truck_id = available_trucks[truck_index]
                    self.put_in_bucket(package, truck_id)
                    for package in packages:
                        self.check_destination(package)

    def put_in_bucket(self, package, truck_id):
        """
        Adds the package to the specified truck's bucket if it has not already been added.
    
        Parameters
        ----------
        package : object
            The package object to be added.
        truck_id : int
            The ID of the truck.
    
        Returns
        -------
        None
    
        Space Complexity
        ---------------
            O(1)
    
        Time Complexity
        ---------------
            O(1)
        """
        if package.pid not in self.bucket_packages:
            self.buckets[truck_id].append(package)
            self.bucket_destinations[truck_id].append(package.destination) if package.destination not in self.bucket_destinations[truck_id] else None
            self.bucket_packages.add(package.pid)  # Mark package as added to a bucket
    
    def process_buckets(self, distances, graph, algo):
        """
        Processes the buckets of packages for each truck and determines their delivery routes.
    
        Parameters
        ----------
        distances : dict
            The dictionary containing distances between locations.
        graph : dict
            The graph representation of the delivery locations.
        algo : function
            The algorithm used for routing.
    
        Returns
        -------
        None
    
        Space Complexity
        ---------------
            O(n)
    
        Time Complexity
        ---------------
            O(n^2)
        """
        for truck_id, bucket in self.buckets.items():
            if not self.trucks[truck_id].current_location == 0: # Don't process the bucket for the truck if not at location 0
                continue
            if bucket:
                for package in bucket:
                    # Handle possible duplicate package objects by verifying the package is in self.packages
                    if package.pid not in self.packages:
                        bucket.remove(package)
    
                if not bucket: # If all the packages were removed from the bucket, move to the next bucket
                    continue
    
                if self.process_groups(bucket, truck_id, distances, graph, algo):
                    continue
    
                self.process_ungrouped(bucket, truck_id, distances, graph, algo)
    
    def process_groups(self, bucket, truck_id, distances, graph, algo):
        """
        Processes grouped packages and assigns them to the specified truck.
    
        Parameters
        ----------
        bucket : list
            The list of packages in the truck's bucket.
        truck_id : int
            The ID of the truck.
        distances : dict
            The dictionary containing distances between locations.
        graph : dict
            The graph representation of the delivery locations.
        algo : function
            The algorithm used for routing.
    
        Returns
        -------
        bool
            True if the group was processed and sent out, otherwise False.
    
        Space Complexity
        ---------------
            O(n)
    
        Time Complexity
        ---------------
            O(n^2)
        """
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
                        route = self.get_route(group_packages, distances, graph, algo)
                        # Send the packages out
                        self.send_it(group_packages, truck_id, route, distances)
                        return True
        return False
    
    def process_ungrouped(self, bucket, truck_id, distances, graph, algo):
        """
        Processes ungrouped packages and assigns them to the specified truck.
    
        Parameters
        ----------
        bucket : list
            The list of packages in the truck's bucket.
        truck_id : int
            The ID of the truck.
        distances : dict
            The dictionary containing distances between locations.
        graph : dict
            The graph representation of the delivery locations.
        algo : function
            The algorithm used for routing.
    
        Returns
        -------
        None
    
        Space Complexity
        ---------------
            O(n)
    
        Time Complexity
        ---------------
            O(n^2)
        """
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
    
        route = self.get_route(queue, distances, graph, algo)
        self.send_it(queue, truck_id, route, distances)

    def get_route(self, packages, distances, graph, algo):
        """
        Determines the delivery route for the given packages using the specified algorithm.
    
        Parameters
        ----------
        packages : list
            The list of packages.
        distances : dict
            The dictionary containing distances between locations.
        graph : dict
            The graph representation of the delivery locations.
        algo : str
            The algorithm used for routing ("dijkstra" or "nearest_neighbor").
    
        Returns
        -------
        tuple
            A tuple containing the total distance, total time, and the ordered list of package deliveries.
    
        Space Complexity
        ---------------
            O(n)
    
        Time Complexity
        ---------------
            O(n^2)
        """
        routes = {}
        previous_route_end = 0
        already_processed = []
        for priority in range(1, self.highest_priority_number + 1):
            destinations = []
            for package in packages:
                if package.priority == priority and package.destination not in destinations and package.destination not in already_processed:
                    destinations.append(package.destination)
            if not destinations:
                continue
            destinations = set(destinations) # ensure no duplicates
            already_processed += destinations
            if algo == "dijkstra":
                route = dijkstra(graph, previous_route_end, destinations)
            else:
                route = nearest_neighbor_algorithm(previous_route_end, destinations, distances)
            # add the route to the routes dictionary with the priority as the key
            routes[priority] = route
            try:
                previous_route_end = route[1][-1][0]
            except Exception as e:
                break
        # combine all the routes from the dictionary into final route
        final_route = [0, 0], []
        for priority in sorted(routes.keys()):
            full_route = routes[priority]
            final_route[0][0] += full_route[0][0]  # sum total distances
            final_route[0][1] += full_route[0][1]  # sum total times
            final_route[1].extend(full_route[1])  # concatenate routes
        return final_route
    
    def send_it(self, packages, truck_id, route, distances):
        """
        Sends the packages out for delivery by assigning them to the specified truck and setting its route.
    
        Parameters
        ----------
        packages : list
            The list of packages.
        truck_id : int
            The ID of the truck.
        route : tuple
            The delivery route.
        distances : dict
            The dictionary containing distances between locations.
    
        Returns
        -------
        None
    
        Space Complexity
        ---------------
            O(n)
    
        Time Complexity
        ---------------
            O(n)
        """
        # Add destination 0 to the end of the final route
        if route[1]:
            last_destination = route[1][-1][0]
            distance_to_hub = distances[last_destination][0] if last_destination in distances and 0 in distances[last_destination] else distances[0][last_destination]
            route[1].append((0, distance_to_hub))
            route[0][0] += distance_to_hub
            route[0][1] += distance_to_hub / 0.3
    
            for package in packages:
                self.load_package(package, truck_id)
            self.trucks[truck_id].set_route(route[1])
            self.trucks[truck_id].go()
    
    def combine_routes(self, old_route, new_route, distance, time):
        """
        Combines the old route with the new route.
    
        Parameters
        ----------
        old_route : list
            The old route.
        new_route : list
            The new route.
        distance : float
            The total distance of the combined route.
        time : float
            The total time of the combined route.
    
        Returns
        -------
        list
            The combined route.
    
        Space Complexity
        ---------------
            O(n)
    
        Time Complexity
        ---------------
            O(n)
        """
        combined_route = old_route + new_route
        route = [[distance, time], combined_route]
        return route
    
    def load_package(self, package, truck_id):
        """
        Loads the package onto the specified truck.
    
        Parameters
        ----------
        package : object
            The package object to be loaded.
        truck_id : int
            The ID of the truck.
    
        Returns
        -------
        None
    
        Space Complexity
        ---------------
            O(1)
    
        Time Complexity
        ---------------
            O(1)
        """
        if len(self.trucks[truck_id].packages) < Truck.MAX_CAPACITY:
            try:
                self.packages.remove(package.pid) # If it can't be removed, it was already loaded onto the truck once and shouldn't be loaded again.
                self.buckets[truck_id].remove(package)
            except:
                return
            package.truck_id = self.trucks[truck_id].truck_id
            self.trucks[truck_id].add_package(package)