from collections import OrderedDict

def lru_cache(operations, capacity):
    """
    Simulate a Least Recently Used cache.

    Args:
        operations (list): A list of tuples containing ("put", key, value) or ("get", key).
        capacity (int): The maximum size of the cache.

    Returns:
        list: A list containing results from all get operations.
    """
    cache = OrderedDict()
    results = []
    for operation in operations:
        op_type, *args = operation
        if op_type == 'put':
            key, value = args
            cache[key] = value
            if len(cache) > capacity:
                cache.popitem(last=False)
        elif op_type == 'get':
            key = args[0]
            result = None
            if key in cache:
                result = cache.pop(key)
                cache[key] = result
                results.append(result)
            else:
                results.append(None)
    return results