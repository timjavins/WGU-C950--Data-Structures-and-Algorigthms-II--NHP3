"""
This module contains the TruckHashTable class for managing truck data in a hash table.

Classes
-------
TruckHashTable
    A class that represents a hash table for storing and retrieving truck data.

Functions
---------
insert(truck_id, packages, current_location, distance_from_last_location, destination, distance_to_destination, total_distance, travel_log, route, trip_minutes, mile_marker, total_time)
    Inserts or updates the truck data in the hash table.

get(key)
    Retrieves the truck data for the given key.

remove(key)
    Removes the truck data for the given key.
"""

class TruckHashTable:
    """
    A class that represents a hash table for storing and retrieving truck data.

    Attributes
    ----------
    size : int
        The size of the hash table.
    table : list
        The hash table implemented as a list of lists.
    count : int
        The number of items in the hash table.
    """

    def __init__(self, size=10):
        """
        Initializes the TruckHashTable with the given size.

        Parameters
        ----------
        size : int, optional
            The size of the hash table (default is 10).
        """
        self.size = size
        self.table = [[] for _ in range(size)]
        self.count = 0

    def _hash(self, key):
        """
        Generates a hash for the given key.

        Parameters
        ----------
        key : str
            The key to be hashed.

        Returns
        -------
        int
            The hash value of the key.

        Space Complexity
        ---------------
            O(1)

        Time Complexity
        ---------------
            O(n)
        """
        key = str(key)  # Ensure the key is a string
        return sum(ord(char) for char in key) % self.size

    def insert(
        self,
        truck_id,
        packages,
        current_location,
        distance_from_last_location,
        destination,
        distance_to_destination,
        total_distance,
        travel_log,
        route,
        trip_minutes,
        mile_marker,
        total_time
    ):
        """
        Inserts or updates the truck data in the hash table.

        Parameters
        ----------
        truck_id : int
            The ID of the truck.
        packages : list
            The list of packages on the truck.
        current_location : int
            The current location of the truck.
        distance_from_last_location : float
            The distance traveled from the last location.
        destination : int
            The destination of the truck.
        distance_to_destination : float
            The distance to the destination.
        total_distance : float
            The total distance traveled by the truck.
        travel_log : list
            The log of locations and times visited by the truck.
        route : list
            The delivery route of the truck.
        trip_minutes : int
            The number of minutes spent on the current trip.
        mile_marker : float
            The mile marker for the current trip.
        total_time : int
            The total time spent on the road.

        Returns
        -------
        str
            "Inserted" if the truck data was inserted, "Updated" if the truck data was updated.

        Space Complexity
        ---------------
            O(1)

        Time Complexity
        ---------------
            O(1)
        """
        if self.count / self.size > 0.7:
            self._grow()
        index = self._hash(truck_id)
        truck_data = {
            'packages': packages,
            'current_location': current_location,
            'distance_from_last_location': distance_from_last_location,
            'destination': destination,
            'distance_to_destination': distance_to_destination,
            'total_distance': total_distance,
            'travel_log': travel_log,
            'route': route,
            'trip_minutes': trip_minutes,
            'mile_marker': mile_marker,
            'total_time': total_time
        }
        for item in self.table[index]:
            if item[0] == truck_id:
                item[1] = truck_data
                return "Updated"
        self.table[index].append([truck_id, truck_data])
        self.count += 1
        return "Inserted"

    def get(self, key):
        """
        Retrieves the truck data for the given key.

        Parameters
        ----------
        key : str
            The key to retrieve the truck data for.

        Returns
        -------
        dict or None
            The truck data if found, otherwise None.

        Space Complexity
        ---------------
            O(1)

        Time Complexity
        ---------------
            O(1)
        """
        index = self._hash(key)
        for item in self.table[index]:
            if item[0] == key:
                return item[1]
        return None

    def remove(self, key):
        """
        Removes the truck data for the given key.
    
        Parameters
        ----------
        key : str
            The key to remove the truck data for.
    
        Returns
        -------
        None
    
        Space Complexity
        ---------------
            O(1)
    
        Time Complexity
        ---------------
            O(1)
        """
        index = self._hash(key)
        for i, item in enumerate(self.table[index]):
            if item[0] == key:
                del self.table[index][i]
                self.count -= 1
                if self.count / self.size < 0.5:
                    self._shrink()
                return
    
    def _grow(self):
        """
        Grows the hash table to a larger size when the load factor exceeds a threshold.
    
        Returns
        -------
        None
    
        Space Complexity
        ---------------
            O(n)
    
        Time Complexity
        ---------------
            O(n)
        """
        new_size = self.size * 2 // 4 * 3
        new_table = [None] * new_size
        for bucket in self.table:
            if bucket is not None:
                for item in bucket:
                    new_index = self._hash(item[0]) % new_size
                    if new_table[new_index] is None:
                        new_table[new_index] = []
                    new_table[new_index].append(item)
        self.size = new_size
        self.table = new_table
    
    def _shrink(self):
        """
        Shrinks the hash table to a smaller size when the load factor falls below a threshold.
    
        Returns
        -------
        None
    
        Space Complexity
        ---------------
            O(n)
    
        Time Complexity
        ---------------
            O(n)
        """
        new_size = self.size // 4 * 3
        new_table = [None] * new_size
        for item in self.table:
            if item is not None:
                new_index = hash(item[0]) % new_size
                new_table[new_index] = item
        self.size = new_size
        self.table = new_table