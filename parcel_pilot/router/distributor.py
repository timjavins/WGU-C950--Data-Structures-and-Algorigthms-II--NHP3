import re
from data.trucks import Truck

class Distributor:
    def __init__(self, trucks):
        self.trucks = trucks

    def distribute_packages(self, packages, grouped_packages):
        # Find the highest priority number
        highest_priority = max(package.priority for package in packages)

        # Load packages by priority
        for priority in range(1, highest_priority + 1):
            for package in packages:
                if package.priority == priority:
                    self.load_package(package)

        # Load priority 0 packages last
        for package in packages:
            if package.priority == 0:
                self.load_package(package)

    def load_package(self, package):
        # Check the notes for truck requirements
        match = re.search(r'Can only be on truck (\d+)', package.notes)
        if match:
            truck_id = int(match.group(1))
            truck = self.trucks[truck_id]
            truck.add_package(package)
        else:
            # Load the package into the first available truck with capacity
            for truck in self.trucks:
                if len(truck.packages) < Truck.MAX_CAPACITY:
                    truck.add_package(package)
                    break