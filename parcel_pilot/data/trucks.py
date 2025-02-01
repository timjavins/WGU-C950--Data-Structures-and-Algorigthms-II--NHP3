"""
This module contains the Truck and TruckManager classes for managing trucks and their operations in the package delivery simulation.

Classes
-------
TruckManager
    A class that manages the creation and retrieval of Truck objects.

Truck
    A class that represents a delivery truck and its operations.

Functions
---------
get_truck(truck_id)
    Retrieves the truck with the given ID, creating it if it does not exist.

add_package(package)
    Adds a package to the truck if it has not reached its maximum capacity.

remove_package(package)
    Removes a package from the truck.

set_route(route)
    Sets the delivery route for the truck.

go()
    Starts the delivery process for the truck.

update_position(current_time)
    Updates the truck's position based on the current time.
"""

class TruckManager:
    """
    A class that manages the creation and retrieval of Truck objects.

    Attributes
    ----------
    trucks : dict
        A dictionary of trucks managed by their IDs.
    """

    def __init__(self):
        """
        Initializes the TruckManager with an empty dictionary of trucks.
        """
        self.trucks = {}

    def get_truck(self, truck_id):
        """
        Retrieves the truck with the given ID, creating it if it does not exist.

        Parameters
        ----------
        truck_id : int
            The ID of the truck to retrieve.

        Returns
        -------
        Truck
            The truck with the given ID.

        Space Complexity
        ---------------
            O(1)

        Time Complexity
        ---------------
            O(1)
        """
        if truck_id not in self.trucks:
            self.trucks[truck_id] = Truck(truck_id)
        return self.trucks[truck_id]

class Truck:
    """
    A class that represents a delivery truck and its operations.

    Attributes
    ----------
    truck_id : int
        The ID of the truck.
    packages : list
        The list of packages on the truck.
    current_location : int
        The current location of the truck.
    distance_from_last_location : float
        The distance traveled from the last location.
    destination : int
        The destination of the truck.
    distance_to_destination : float
        The distance to the destination.
    total_distance : float
        The total distance traveled by the truck.
    travel_log : list
        The log of locations and times visited by the truck.
    route : list
        The delivery route of the truck.
    trip_minutes : int
        The number of minutes spent on the current trip.
    mile_marker : float
        The mile marker for the current trip.
    total_time : int
        The total time spent on the road.
    """

    MAX_CAPACITY = 16  # Maximum load capacity of these trucks

    def __init__(self, truck_id):
        """
        Initializes the Truck with the given ID and default values.

        Parameters
        ----------
        truck_id : int
            The ID of the truck.
        """
        self.truck_id = truck_id
        self.packages = []
        self.current_location = 0  # Hub is location 0
        self.distance_from_last_location = 0.0
        self.destination = None
        self.distance_to_destination = 0.0
        self.total_distance = 0.0
        self.travel_log = []
        self.route = []
        self.trip_minutes = 0
        self.mile_marker = 0
        self.total_time = 0

    def __str__(self):
        """
        Returns a string representation of the Truck object.

        Returns
        -------
        str
            A string representation of the Truck object.

        Space Complexity
        ---------------
            O(1)

        Time Complexity
        ---------------
            O(1)
        """
        return f"Truck ID: {self.truck_id}, Current Location: {self.current_location}, Total Distance: {self.total_distance}, Packages: {[pkg.pid for pkg in self.packages]}"

    def add_package(self, package):
        """
        Adds a package to the truck if it has not reached its maximum capacity.

        Parameters
        ----------
        package : object
            The package object to be added.

        Returns
        -------
        None

        Raises
        ------
        ValueError
            If the truck is at full capacity.

        Space Complexity
        ---------------
            O(1)

        Time Complexity
        ---------------
            O(1)
        """
        if len(self.packages) < self.MAX_CAPACITY:
            self.packages.append(package)
            package.truck_id = self.truck_id
        else:
            raise ValueError(f"Truck {self.truck_id} is at full capacity")

    def remove_package(self, package):
        """
        Removes a package from the truck.

        Parameters
        ----------
        package : object
            The package object to be removed.

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
        self.packages.remove(package)

    def set_route(self, route):
        """
        Sets the delivery route for the truck.

        Parameters
        ----------
        route : list
            The delivery route as a list of tuples (destination, distance).

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
        self.current_location = -1
        self.route = route

    def go(self):
        """
        Starts the delivery process for the truck.

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
        if self.route:
            if self.packages:
                for package in self.packages:
                    package.location = -1
                    package.status = "OUT FOR DELIVERY"
            self.destination = self.route[0][0]  # The destination is the first element in the tuple
            self.distance_to_destination = self.route[0][1]  # The distance to the destination is the second element in the tuple

    def update_position(self, current_time):
        """
        Updates the truck's position based on the current time.

        Parameters
        ----------
        current_time : str
            The current time in 24-hour format (HH:MM).

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
        if self.route:
            if self.current_location != 0:
                self.trip_minutes += 1  # Increment the time spent on the road, expecting position updates to be exactly once per minute.
                self.total_time += 1
            distance_traveled = self.trip_minutes * 0.3  # Trip distance traveled in miles per minute
            # Update the truck's position
            self.distance_from_last_location = distance_traveled - self.mile_marker
    
            # Check if the truck has reached the destination
            if self.distance_from_last_location >= self.distance_to_destination:
                self.total_distance += self.distance_to_destination
                self.current_location = self.destination
                self.distance_from_last_location = 0.0
                self.distance_to_destination = 0.0
                self.mile_marker = distance_traveled
                self.route.pop(0)
                # Create a list of packages to be removed
                packages_to_remove = []
                # Check all the packages on the truck to deliver the proper package(s)
                for package in self.packages:
                    if package.destination == self.current_location:
                        package.status = f"DELIVERED AT {current_time}"
                        package.delivery_time = current_time
                        package.location = self.current_location
                        if package.deadline == "EOD" or  current_time <= package.deadline:
                            package.timely = True
                        else:
                            package.timely = False
                        packages_to_remove.append(package)
                # Remove the packages after the iteration to avoid modifying the list while iterating and skipping packages
                for package in packages_to_remove:
                    self.remove_package(package)
                # Log the location and time of arrival
                self.travel_log.append((self.current_location, current_time))
                self.go()
        if self.current_location == 0 and not self.route:
            self.trip_minutes = 0
            self.mile_marker = 0