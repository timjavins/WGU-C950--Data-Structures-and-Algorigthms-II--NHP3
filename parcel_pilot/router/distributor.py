import re
from data.trucks import Truck
from datetime import datetime, timedelta

class Distributor:
    def __init__(self, trucks):
        self.trucks = trucks
        self.late_packages = 0
        self.time_constraint = 0
        self.distance_constraint = 0
        self.trucks[0].current_location = -1 # Ignore truck 0 since there are only two drivers
        self.initializing = True
        self.highest_priority_number = 0

    def distribute_packages(self, all_packages, time_string, next_flight_time, late_packages, algo):
        # Late packages is the number of packages arriving on the next flight
        # If no trucks are at location 0, stop
        if not any(truck.current_location == 0 for truck in self.trucks):
            return
        packages = [package for package in all_packages if package.truck_id is None]
        if not packages:
            return
        print(f"Time: {time_string}")
        print(f"Next flight time: {next_flight_time}")
        print(f"Late packages: {late_packages}")
        self.late_packages = late_packages
        today = datetime.today().date()
        if not next_flight_time:
            next_flight_time = "17:00"
        time = datetime.combine(today, datetime.strptime(time_string, "%H:%M").time())
        print(f"New Time: {time}")
        next_flight_time = datetime.combine(today, datetime.strptime(next_flight_time, "%H:%M").time())
        self.time_constraint = (next_flight_time - time) / timedelta(minutes=1) # Convert to minutes
        print(f"Next flight time: {next_flight_time}, Time constraint: {self.time_constraint} minutes")

        if self.initializing:
            # Find the highest priority number
            self.highest_priority_number = max(package.priority for package in packages)

        # Load packages by priority rank (1 being the first priority)
        for priority in range(1, self.highest_priority_number + 1):
            for package in packages:
                if package.priority == priority:
                    print(f"Reading package {package.pid}")
                    # read its destination
                    destination = package.destination
                    # read its group
                    group = package.group
                    self.load_package(package)
                    # Find other packages with the same destination
                    for package in packages:
                        print(f"Reading package {package.pid}")
                        if package.destination == destination:
                            self.load_package(package)

        # Load priority 0 packages last
        # TODO: Write logic in package_handler.py for updating the package notes when correct address is received
        for package in packages:
            if package.notes == "Wrong address listed":
                # skip this package
                continue
            if package.priority == 0:
                self.load_package(package)
        # TODO: Get the routes
        # TODO: Make the trucks move
        # TODO: Set the truck location to -1 when it leaves the hub
        self.initializing = False

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
                    package.truck_id = truck_id
                    print(f"Loading package {package.pid} onto truck {truck_id} - {package.truck_id}")
                    truck.add_package(package)
            else:
                # Load the package into the first available truck with capacity
                for truck in available_trucks:
                    if len(truck.packages) < Truck.MAX_CAPACITY:
                        package.truck_id = truck.truck_id
                        print(f"Loading package {package.pid} onto truck {truck.truck_id} - {package.truck_id}")
                        truck.add_package(package)
                        break