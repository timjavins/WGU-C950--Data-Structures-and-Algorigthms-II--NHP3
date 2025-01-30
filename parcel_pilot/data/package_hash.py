class PackageHashTable:
    def __init__(self, size=40):
        self.size = size
        self.table = [[] for _ in range(size)]
        self.count = 0

    def _hash(self, key):
        """
        Generates a hash for a given key.

        Parameters:
        key (str): The key to hash.

        Returns:
        int: The hash value.
        """
        return sum(ord(char) for char in key) % self.size
    
    def _grow(self):
        """
        Resizes the hash table by increasing its size by about 50%.
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
        Resizes the hash table by decreasing its size by about 25%.
        """
        new_size = self.size // 4 * 3
        new_table = [None] * new_size
        for item in self.table:
            if item is not None:
                new_index = hash(item[0]) % new_size
                new_table[new_index] = item
        self.size = new_size
        self.table = new_table

    def insert(
        self,
        pid,
        address,
        city,
        state,
        zip_code,
        deadline,
        weight,
        status,
        notes,
        priority=-1,
        truck_id=None,
        location=None,
        group=None,
        arrival_time=None,
        destination=None,
        delivery_time=None,
        timely=None
    ):
        """
        Inserts a package into the hash table.
        
        Parameters:
        pid (str): The package ID.
        address (str): The delivery address.
        city (str): The delivery city.
        state (str): The delivery state.
        zip_code (str): The delivery zip code.
        deadline (str): The delivery deadline.
        weight (str): The package weight.
        status (str): The delivery status.
        notes (str): Additional notes.
        priority (int, optional): The priority of the package. Default is -1.
        truck_id (str, optional): The truck ID. Default is None.
        location (str, optional): The location. Default is None.
        group (str, optional): The group. Default is None.
        arrival_time (str, optional): The arrival time. Default is None.
        destination (str, optional): The destination. Default is None.
        delivery_time (str, optional): The delivery time. Default is None.
        timely (bool, optional): Whether the package was delivered on time. Default is None.
        """
        if self.count / self.size > 0.7:  # Load factor threshold to trigger the hash table's resize method for self-adjustment
            self._grow()
        index = self._hash(pid)
        # Make sure the bucket is not empty
        if self.table[index] is None:
            self.table[index] = []
        # Check if the PID already exists and update it
        for item in self.table[index]:
            if item[0] == pid:
                item[1:] = [
                    address,
                    city,
                    state,
                    zip_code,
                    deadline,
                    weight,
                    status,
                    notes,
                    priority,
                    truck_id,
                    location,
                    group,
                    arrival_time,
                    destination,
                    delivery_time,
                    timely
                ]
                return "Updated"
        self.count += 1
        # If PID does not exist, append the new package data
        self.table[index].append([
            pid,
            address,
            city,
            state,
            zip_code,
            deadline,
            weight,
            status,
            notes,
            priority,
            truck_id,
            location,
            group,
            arrival_time,
            destination,
            delivery_time,
            timely
        ])
        return "Inserted"
    
    def get(self, pid):
        """
        Retrieves a package from the hash table by its PID.

        Parameters:
        pid (str): The package ID.

        Returns:
        list: The package data if found, None otherwise.
        """
        index = self._hash(pid)
        for item in self.table[index]:
            if item[0] == pid:
                return item
        return None

    def remove(self, pid):
        """
        Removes a package from the hash table by its PID.
    
        Parameters:
        pid (str): The package ID.
        """
        index = self._hash(pid)
        for i, item in enumerate(self.table[index]):
            if item[0] == pid:
                del self.table[index][i]
                self.count -= 1  # Decrement the count after removing the item
                if self.count / self.size < 0.5:  # Load factor threshold to trigger the hash table's resize method for self-adjustment
                    self._shrink()
                return