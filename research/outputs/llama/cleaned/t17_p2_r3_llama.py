from collections import OrderedDict

class LRUCache:

    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key):
        if key in self.cache:
            value = self.cache.pop(key)
            self.cache[key] = value
            return value
        else:
            return -1

    def put(self, key, value):
        if key in self.cache:
            self.cache.pop(key)
        elif len(self.cache) >= self.capacity:
            self.cache.popitem(last=False)
        self.cache[key] = value

def lru_cache(operations, capacity):
    cache = LRUCache(capacity)
    results = []
    for operation in operations:
        op_type, key, *value = operation
        if op_type == 'get':
            result = cache.get(key)
            results.append(result)
        elif op_type == 'put':
            value = value[0]
            cache.put(key, value)
    return results