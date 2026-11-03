from collections import OrderedDict

class LRUCache:

    def __init__(self, capacity):
        """
        Initialize the LRU cache with the given capacity.
        
        :param capacity: Maximum number of items to store in the cache.
        """
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key):
        """
        Retrieve a value from the cache by its key. If the key exists, move it to the end and return the value.
        
        :param key: Key of the item to retrieve.
        :return: Value associated with the key if it exists in the cache; None otherwise.
        """
        if key in self.cache:
            value = self.cache.pop(key)
            self.cache[key] = value
            return value
        else:
            return None

    def put(self, key, value):
        """
        Add or update a key-value pair in the cache. If the cache is at capacity and the key does not exist, remove the least recently used item.
        
        :param key: Key of the item to add or update.
        :param value: Value associated with the key.
        """
        if key in self.cache:
            self.cache.pop(key)
        elif len(self.cache) >= self.capacity:
            self.cache.popitem(last=False)
        self.cache[key] = value

def lru_cache(operations, capacity):
    """
    Simulate an LRU cache by performing operations on it.
    
    :param operations: List of tuples containing the operation type ('get' or 'put') and its arguments.
    :param capacity: Maximum number of items to store in the cache.
    :return: Resulting values after executing all operations.
    """
    lru = LRUCache(capacity)
    results = {}
    for op, *args in operations:
        if op == 'get':
            result = lru.get(*args)
            results[args[0]] = result
        elif op == 'put':
            lru.put(*args)
    return results