class Minute:
    def __init__(self, time_str, packages, trucks):
        self.time_str = time_str
        self.packages = packages
        self.trucks = trucks

    def __repr__(self):
        return f"Minute(time_str={self.time_str}, packages={len(self.packages)}, trucks={len(self.trucks)})"