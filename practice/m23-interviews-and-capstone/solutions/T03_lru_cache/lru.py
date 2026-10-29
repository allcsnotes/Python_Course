"""Task 3 - a least-recently-used cache with O(1) get and put."""
from collections import OrderedDict


class LRUCache:
    def __init__(self, capacity: int):
        if capacity < 1:
            raise ValueError("capacity must be at least 1")
        self.capacity = capacity
        self._data: OrderedDict = OrderedDict()
        self.hits = 0
        self.misses = 0

    def get(self, key, default=None):
        if key not in self._data:
            self.misses += 1
            return default
        self.hits += 1
        self._data.move_to_end(key)             # most recently used goes last
        return self._data[key]

    def put(self, key, value):
        if key in self._data:
            self._data.move_to_end(key)
        self._data[key] = value
        if len(self._data) > self.capacity:
            self._data.popitem(last=False)      # drop the least recently used

    def __len__(self):
        return len(self._data)

    def __contains__(self, key):               # does not count as a use
        return key in self._data

    def keys(self):
        """Keys from least to most recently used."""
        return list(self._data)
