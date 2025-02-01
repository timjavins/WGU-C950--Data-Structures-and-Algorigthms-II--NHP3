"""
This module defines the Minute class, which represents the state of packages and trucks at a specific minute in the package delivery simulation.

Classes
-------
Minute
    A class which represents the state of packages and trucks at a specific minute in the simulation.
"""

class Minute:
    """
    A class which represents the state of packages and trucks at a specific minute in the simulation.

    Attributes
    ----------
    time_str : str
        The time in 24-hour format (HH:MM).
    packages : dict
        A dictionary containing the state of all packages.
    trucks : dict
        A dictionary containing the state of all trucks.
    """

    def __init__(self, time_str, packages, trucks):
        """
        Initializes the Minute object with the given time, packages, and trucks.

        Parameters
        ----------
        time_str : str
            The time in 24-hour format (HH:MM).
        packages : dict
            A dictionary containing the state of all packages.
        trucks : dict
            A dictionary containing the state of all trucks.
        """
        self.time_str = time_str
        self.packages = packages
        self.trucks = trucks

    def __repr__(self):
        """
        Returns a string representation of the Minute object.

        Returns
        -------
        str
            A string representation of the Minute object, including the time, number of packages, and number of trucks.

        Space Complexity
        ---------------
            O(1)

        Time Complexity
        ---------------
            O(1)
        """
        return f"Minute(time_str={self.time_str}, packages={len(self.packages)}, trucks={len(self.trucks)})"