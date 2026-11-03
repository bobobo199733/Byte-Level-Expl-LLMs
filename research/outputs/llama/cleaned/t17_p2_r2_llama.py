from collections import OrderedDict

def lru_cache(operations, capacity):
    """
    Simulates a Least Recently Used cache.

    Args:
        operations (list): A list of tuples such as ("put", key, value) or ("get", key).
        capacity (int): The maximum number of items the cache can hold.

    Returns:
        list: Results from all get operations.
    """
    cache = OrderedDict()
    results = []
    for op, *args in operations:
        if op == 'put':
            key, value = args
            if key in cache:
                del cache[key]
            cache[key] = value
            while len(cache) > capacity:
                cache.popitem(last=False)
        elif op == 'get':
            key = args[0]
            if key in cache:
                value = cache.pop(key)
                cache[key] = value
                results.append(value)
            else:
                results.append(None)
    return results