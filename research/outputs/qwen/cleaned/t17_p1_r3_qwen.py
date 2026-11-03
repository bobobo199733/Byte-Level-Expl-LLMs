from collections import OrderedDict

def lru_cache(operations, capacity):

    class LRUCache:

        def __init__(self, capacity):
            self.cache = OrderedDict()
            self.capacity = capacity

        def get(self, key):
            if key not in self.cache:
                return -1
            else:
                self.cache.move_to_end(key)
                return self.cache[key]

        def put(self, key, value):
            if key in self.cache:
                self.cache.move_to_end(key)
            self.cache[key] = value
            if len(self.cache) > self.capacity:
                self.cache.popitem(last=False)
    result = []
    cache = LRUCache(capacity)
    for operation in operations:
        if operation[0] == 'get':
            result.append(cache.get(operation[1]))
        elif operation[0] == 'put':
            cache.put(operation[1], operation[2])
    return result