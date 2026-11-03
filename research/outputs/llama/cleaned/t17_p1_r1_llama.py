from collections import OrderedDict

class LRUCache:

    def __init__(self, capacity):
        """
        Initialize an LRU cache with a specified capacity.
        
        :param capacity: The maximum number of items that can be stored in the cache.
        """
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key):
        """
        Retrieve a value from the cache by its key. If the key is not found, return -1.
        
        :param key: The key to retrieve from the cache.
        :return: The value associated with the key if it exists in the cache; otherwise, -1.
        """
        if key in self.cache:
            value = self.cache.pop(key)
            self.cache[key] = value
            return value
        else:
            return -1

    def set(self, key, value):
        """
        Insert or update a key-value pair in the cache.
        
        :param key: The key to insert or update in the cache.
        :param value: The value associated with the key.
        """
        if key in self.cache:
            self.cache.pop(key)
        elif len(self.cache) >= self.capacity:
            self.cache.popitem(last=False)
        self.cache[key] = value

def lru_cache(operations, capacity):
    """
    Simulate an LRU cache and return the outputs of all get operations.
    
    :param operations: A list of lists representing cache operations (see documentation above).
    :param capacity: The maximum number of items that can be stored in the cache.
    :return: A list of values retrieved by get operations, or -1 if a key is not found.
    """
    cache = LRUCache(capacity)
    results = []
    for operation in operations:
        op_type = operation[0]
        if op_type == 'get':
            key = operation[1]
            result = cache.get(key)
            results.append(result)
        elif op_type == 'set':
            key, value = (operation[1], operation[2])
            cache.set(key, value)
    return results