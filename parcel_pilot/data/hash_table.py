class HashTable:
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

    def insert(self, pid, address, city, state, zip_code, deadline, weight, status, notes):
        """
        Inserts a package into the hash table.
    
        Parameters:
        pid (str): The package ID.
        address (str): The delivery address.
        deadline (str): The delivery deadline.
        city (str): The delivery city.
        zip_code (str): The delivery zip code.
        weight (str): The package weight.
        status (str): The delivery status.
        """
        if self.count / self.size > 0.7:  # Load factor threshold to trigger the hash table's resize method for self-adjustment
            self._grow()
        index = self._hash(pid)
        # Make sure the bucket is not empty
        if self.table[index] is None:
            self.table[index] = []
        # Check if the PID already exists and update it
        for item in self.table[index]:
            if item[0] == pid: # If the PID already exists, update the package data
                item[1:] = [address, city, state, zip_code, deadline, weight, status, notes]
                return "Updated"
        self.count += 1
        # If PID does not exist, append the new package data
        self.table[index].append([pid, address, city, state, zip_code, deadline, weight, status, notes])
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

# # Example usage
# if __name__ == "__main__":
#     hash_table = HashTable()
#     hash_table.insert("1", "123 Main St", "10:30 AM", "Cityville", "12345", "5 lbs", "at the hub")
#     hash_table.insert("2", "456 Elm St", "12:00 PM", "Townsville", "67890", "10 lbs", "en route")
#     print(hash_table.get("1"))
#     print(hash_table.get("2"))
#     hash_table.remove("1")
#     print(hash_table.get("1"))