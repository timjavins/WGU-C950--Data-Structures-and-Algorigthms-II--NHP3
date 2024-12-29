from datetime import datetime, timedelta

class TruckManager:
    def __init__(self):
        self.trucks = {}

    def get_truck(self, truck_id):
        if truck_id not in self.trucks:
            self.trucks[truck_id] = Truck(truck_id)
        return self.trucks[truck_id]

class Truck:
    def __init__(self, truck_id):
        self.truck_id = truck_id
        self.packages = []
        self.current_location = 0  # Hub is location 0
        self.distance_from_last_location = 0.0
        self.destination = None
        self.distance_to_destination = 0.0
        self.total_distance = 0.0
        self.travel_log = []

    def add_package(self, package):
        self.packages.append(package)

    def set_destination(self, destination, distance):
        self.destination = destination
        self.distance_to_destination = distance

    def update_position(self, current_time, map_locations):
        # Calculate the distance traveled based on the time elapsed
        time_elapsed = (current_time - self.start_time).total_seconds() / 60.0  # Convert to minutes
        distance_traveled = time_elapsed * 0.3  # Distance traveled in miles

        # Update the truck's position
        self.distance_from_last_location += distance_traveled
        self.total_distance += distance_traveled

        # Check if the truck has reached the destination
        if self.distance_from_last_location >= self.distance_to_destination:
            self.current_location = self.destination
            self.distance_from_last_location = 0.0
            self.destination = None
            self.distance_to_destination = 0.0

            # Log the location and time of arrival
            self.travel_log.append((self.current_location, current_time))