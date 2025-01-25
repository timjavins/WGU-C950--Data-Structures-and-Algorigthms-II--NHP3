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

    def __str__(self):
        return f"Truck ID: {self.truck_id}, Current Location: {self.current_location}, Total Distance: {self.total_distance}, Packages: {[pkg.pid for pkg in self.packages]}"
    
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
                    package.status = "OUT FOR DELIVERY"
            self.destination = self.route[0][0] # The destination is the first element in the tuple
            self.distance_to_destination = self.route[0][1] # The distance to the destination is the second element in the tuple

    def update_position(self, current_time):
        if self.route:
            self.trip_minutes += 1  # Increment the time spent on the road, expecting position updates to be exactly once per minute.
            distance_traveled = self.trip_minutes * 0.3  # Trip distance traveled in miles per minute
            # Update the truck's position
            self.distance_from_last_location = distance_traveled - self.mile_marker
            with open("truck states.txt", "a") as file:
                file.write(f"Time: {current_time}\n")
                file.write(f"Truck {self.truck_id} at {self.current_location} - {self.distance_from_last_location} miles from last location\n")
                file.write(f"Truck {self.truck_id} route: {self.route}\n")
                file.write(f"Truck {self.truck_id} packages: {[package.pid for package in self.packages]}\n")
    
            # Check if the truck has reached the destination
            if self.distance_from_last_location >= self.distance_to_destination:
                self.route.pop(0)
                self.current_location = self.destination
                self.distance_from_last_location = 0.0
                self.distance_to_destination = 0.0
                self.total_distance += self.distance_from_last_location
                self.mile_marker = distance_traveled
                # Create a list of packages to be removed
                packages_to_remove = []
                # Check all the packages on the truck to deliver the proper package(s)
                for package in self.packages:
                    if package.destination == self.current_location:
                        package.status = f"DELIVERED AT {current_time}"
                        package.delivery_time = current_time
                        package.location = self.current_location
                        packages_to_remove.append(package)
                        with open("simulation_states.txt", "a") as file:
                            file.write(f"Package {package.pid} delivered at {current_time} (Deadline was {package.deadline})\n")
                # Remove the packages after the iteration to avoid modifying the list while iterating and skipping packages
                for package in packages_to_remove:
                    self.remove_package(package)
                # Log the location and time of arrival
                self.travel_log.append((self.current_location, current_time))
                self.go()
        if self.current_location == 0 and not self.route:
            self.trip_minutes = 0
