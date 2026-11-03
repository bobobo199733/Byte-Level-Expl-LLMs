from collections import OrderedDict

def lru_cache(operations, capacity):
    """
    Simulates an LRU (Least Recently Used) cache.
    
    Args:
        operations (list): List of operations. Each operation is a tuple containing the key and the value to be stored or retrieved from the cache.
            The first element in the operation is either 'get' or 'put' depending on whether we are retrieving or storing a value.
            If it's a 'put', then the second element is the key, and the third element is the value. 
            If it's a 'get', then the second element is the key.
        capacity (int): Maximum number of items that can be stored in the cache at any given time.

    Returns:
        list: The cached values corresponding to the input keys. Each item in the returned list corresponds to an operation in the input operations list.
            If the key was not found in the cache, then a None is placed in its corresponding position in the output list.

    """
    cache = OrderedDict()
    results = []
    for op, *args in operations:
        if op == 'get':
            key = args[0]
            if key not in cache:
                results.append(None)
            else:
                value = cache.pop(key)
                cache[key] = value
                results.append(value)
        elif op == 'put':
            key, value = args
            if key in cache:
                del cache[key]
            cache[key] = value
            if len(cache) > capacity:
                cache.popitem(last=False)
    return results