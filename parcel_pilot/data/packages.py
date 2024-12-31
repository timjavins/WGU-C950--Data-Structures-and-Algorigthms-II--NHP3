class Package:
    def __init__(self, pid, address, city, state, zip_code, deadline, weight, status, notes):
        self.pid = pid
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.deadline = deadline
        self.weight = weight
        self.notes = notes
        self.status = status
        self.priority = -1  # Default priority
        self.truck_id = None
        self.location = None
        self.group = None


    def __str__(self): # The __str__ method is useful for debugging and logging.
        return (f"Package ID: {self.pid}, Address: {self.address}, City: {self.city}, State: {self.state}, "
                f"ZIP: {self.zip_code}, Deadline: {self.deadline}, Weight: {self.weight}, "
                f"Notes: {self.notes}, Status: {self.status}, Priority: {self.priority},"
                f"Truck ID: {self.truck_id}, Location: {self.location}, Group: {self.group}")