from collections import OrderedDict

def lru_cache(operations, capacity):
    cache = OrderedDict()
    result = []

    def get(key):
        if key not in cache:
            result.append(-1)
            return -1
        else:
            value = cache.pop(key)
            result.append(value)
            cache[key] = value
            return value

    def set(key, value):
        nonlocal capacity
        if key in cache:
            cache.pop(key)
        elif len(cache) == capacity:
            cache.popitem(last=False)
        cache[key] = value
    for operation in operations:
        if isinstance(operation, tuple):
            key, value = operation
            result.append(set(key, value))
        else:
            result.append(get(operation))
    return result