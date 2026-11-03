from collections import OrderedDict

def lru_cache(operations, capacity):
    """
    Simulates an LRU cache.

    Args:
        operations (list): A list of operations to perform on the cache.
            Each operation is a tuple of (key, value).
        capacity (int): The maximum size of the cache.

    Returns:
        dict: The contents of the cache after all operations have been performed.
    """
    cache = OrderedDict()
    for key, value in operations:
        if key in cache:
            del cache[key]
            cache[key] = value
        elif len(cache) >= capacity:
            cache.popitem(last=False)
        cache[key] = value
    return dict(cache)