from collections import OrderedDict

def lru_cache(operations, capacity):
    """
    Simulates an LRU cache and returns the outputs of all get operations.

    Args:
        operations (list): A list of tuples containing operation type ('get' or 'put') and key.
        capacity (int): The maximum size of the cache.

    Returns:
        list: A list of results from all 'get' operations in the order they were accessed.
    """
    cache = OrderedDict()
    results = []
    for op, key in operations:
        if op == 'get':
            if key in cache:
                del cache[key]
                cache[key] = None
                results.append(key)
            elif len(cache) >= capacity:
                cache.popitem(last=False)
            else:
                cache[key] = None
        elif op == 'put':
            if len(cache) >= capacity:
                cache.popitem(last=False)
            cache[key] = None
    return results