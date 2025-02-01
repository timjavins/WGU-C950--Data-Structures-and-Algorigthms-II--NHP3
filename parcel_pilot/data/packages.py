class Package:
    """
    A class to represent a package in the delivery system.

    Attributes
    ----------
    pid : int
        The package ID.
    address : str
        The delivery address.
    city : str
        The city of the delivery address.
    state : str
        The state of the delivery address.
    zip_code : str
        The ZIP code of the delivery address.
    deadline : str
        The delivery deadline.
    weight : float
        The weight of the package.
    status : str
        The current status of the package.
    notes : str
        Additional notes about the package.
    priority : int
        The priority of the package.
    truck_id : int or None
        The ID of the truck assigned to deliver the package.
    location : str or None
        The current location of the package.
    group : str or None
        The group to which the package belongs.
    arrival_time : str or None
        The arrival time of the package.
    destination : str or None
        The destination of the package.
    delivery_time : str or None
        The delivery time of the package.
    original : bool
        Indicates if the package is original.
    timely : bool or None
        Indicates if the package was delivered on time.
    """

    def __init__(self, pid, address, city, state, zip_code, deadline, weight, status, notes):
        """
        Constructs all the necessary attributes for the package object.

        Parameters
        ----------
        pid : int
            The package ID.
        address : str
            The delivery address.
        city : str
            The city of the delivery address.
        state : str
            The state of the delivery address.
        zip_code : str
            The ZIP code of the delivery address.
        deadline : str
            The delivery deadline.
        weight : float
            The weight of the package.
        status : str
            The current status of the package.
        notes : str
            Additional notes about the package.
        """
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
        self.arrival_time = None
        self.destination = None
        self.delivery_time = None
        self.original = False
        self.timely = None

    def __str__(self):
        """
        Returns a string representation of the package object.

        Returns
        -------
        str
            A string representation of the package.
        """
        return (f"Package ID: {self.pid}, Address: {self.address}, City: {self.city}, State: {self.state}, "
                f"ZIP: {self.zip_code}, Deadline: {self.deadline}, Weight: {self.weight}, "
                f"Notes: {self.notes}, Status: {self.status}, Priority: {self.priority},"
                f"Truck ID: {self.truck_id}, Location: {self.location}, Group: {self.group},"
                f"Arrival Time: {self.arrival_time}, Destination: {self.destination}, "
                f"Delivery Time: {self.delivery_time}, Original: {self.original}, Timely: {self.timely}")