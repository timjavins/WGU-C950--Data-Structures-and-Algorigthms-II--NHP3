class TruckHashTable:
    def __init__(self, size=10):
        self.size = size
        self.table = [[] for _ in range(size)]
        self.count = 0

    def _hash(self, key):
        key = str(key) # Ensure the key is a string
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
        index = self._hash(key)
        for item in self.table[index]:
            if item[0] == key:
                return item[1]
        return None

    def remove(self, key):
        index = self._hash(key)
        for i, item in enumerate(self.table[index]):
            if item[0] == key:
                del self.table[index][i]
                self.count -= 1
                if self.count / self.size < 0.5:
                    self._shrink()
                return

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
        new_size = self.size // 4 * 3
        new_table = [None] * new_size
        for item in self.table:
            if item is not None:
                new_index = hash(item[0]) % new_size
                new_table[new_index] = item
        self.size = new_size
        self.table = new_table
