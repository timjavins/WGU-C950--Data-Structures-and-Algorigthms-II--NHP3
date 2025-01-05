from datetime import datetime, timedelta

class TruckManager:
    def __init__(self):
        self.trucks = {}

    def get_truck(self, truck_id):
        if truck_id not in self.trucks:
            self.trucks[truck_id] = Truck(truck_id)
        return self.trucks[truck_id]

class Truck:
    MAX_CAPACITY = 16 # Maximum load capacity of these trucks

    def __init__(self, truck_id):
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

    def add_package(self, package):
        if len(self.packages) < self.MAX_CAPACITY:
            self.packages.append(package)
            package.truck_id = self.truck_id
        else:
            raise ValueError(f"Truck {self.truck_id} is at full capacity")

    def remove_package(self, package):
        self.packages.remove(package)

    def set_route(self, route):
        self.current_location = -1
        self.route = route

    def go(self):
        if self.route:
            if self.packages:
                for package in self.packages:
                    package.location = -1
            self.destination = self.route[0][0]
            self.distance_to_destination = self.route[0][1]
            self.route.pop(0)

    def update_position(self, current_time, map_locations):
        self.trip_minutes += 1 # Increment the time spent on the road, expecting position updates to be exactly once per minute.
        distance_traveled = self.trip_minutes * 0.3  # Trip distance traveled in miles per minute
        # Update the truck's position
        self.distance_from_last_location = distance_traveled - self.mile_marker

        # Check if the truck has reached the destination
        if self.distance_from_last_location >= self.distance_to_destination:
            self.current_location = self.destination
            self.distance_from_last_location = 0.0
            self.destination = None
            self.distance_to_destination = 0.0
            self.total_distance += self.distance_from_last_location
            self.mile_marker = distance_traveled
            # Check all the packages on the truck to deliver the proper package(s)
            for package in self.packages:
                if package.destination == self.current_location:
                    package.status = f"DELIVERED AT {current_time}"
                    package.delivery_time = current_time
                    package.location = self.current_location
                    self.remove_package(package)
            # Log the location and time of arrival
            self.travel_log.append((self.current_location, current_time))
            self.go()
        if self.current_location == 0:
            self.trip_minutes = 0