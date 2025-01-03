import re
from data.trucks import Truck
from datetime import datetime, timedelta

class Distributor:
    def __init__(self, trucks):
        self.trucks = trucks
        self.late_packages = 0
        self.time_constraint = 0
        self.distance_constraint = 0
        self.trucks.pop(0) # Ignore truck 0 since there are only two drivers

    def distribute_packages(self, packages, grouped_packages, delivery_order, time_string, next_flight_time, late_packages):
        # Late packages is the number of packages arriving on the next flight
        # If no trucks are at location 0, stop
        if not any(truck.current_location == 0 for truck in self.trucks):
            return
        print(f"Time: {time_string}")
        print(f"Next flight time: {next_flight_time}")
        print(f"Late packages: {late_packages}")
        self.late_packages = late_packages
        if not next_flight_time:
            next_flight_time = datetime.strptime("17:00", "%H:%M")
        time = datetime.strptime(time_string, "%H:%M")
        print(f"New Time: {time}")
        next_flight_time = datetime.strptime(next_flight_time, "%H:%M")
        self.time_constraint = (next_flight_time - time) / timedelta(minutes=1) # Convert to minutes
        print(f"Next flight time: {next_flight_time}, Time constraint: {self.time_constraint} minutes")

        # Find the highest priority number
        highest_priority_number = max(package.priority for package in packages)

        # Load packages by priority rank (1 being the first priority)
        for priority in range(1, highest_priority_number + 1):
            for package in packages:
                if package.priority == priority:
                    # read its destination
                    destination = package.destination
                    # read its group
                    group = package.group
                    self.load_package(package)
                # Find other packages with the same destination
                for package in packages:
                    if package.destination == destination:
                        self.load_package(package)

        # Load priority 0 packages last
        for package in packages:
            if package.priority == 0:
                self.load_package(package)

    def load_package(self, package):
        # Check if any trucks are at location 0
        available_trucks = [truck for truck in self.trucks if truck.current_location == 0]
        if available_trucks:
            # Check the notes for truck requirements
            match = re.search(r'Can only be on truck (\d+)', package.notes)
            if match:
                truck_id = int(match.group(1))
                truck = self.trucks[truck_id]
                if len(truck.packages) < Truck.MAX_CAPACITY:
                    truck.add_package(package)
            else:
                # Load the package into the first available truck with capacity
                for truck in [self.trucks[1], self.trucks[2]]:
                    if len(truck.packages) < Truck.MAX_CAPACITY:
                        truck.add_package(package)
                        break