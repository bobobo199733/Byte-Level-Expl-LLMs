from collections import OrderedDict

def lru_cache(operations, capacity):
    """
    Simulates an LRU Cache.
    
    Args:
        operations (list): A list of strings representing cache operations. 
                           Each string is either "set key value" or "get key".
        capacity (int): The maximum number of items the cache can hold.

    Returns:
        dict: A dictionary containing the results of each operation in the order they were performed.
              For 'get' operations, the result will be the value if the key exists, otherwise -1.
              For 'set' operations, no return value.
    """
    cache = OrderedDict()
    results = []
    for op in operations:
        if 'get' in op:
            key = int(op.split()[1])
            if key in cache:
                results.append(cache[key])
                del cache[key]
                cache[key] = key
            else:
                results.append(-1)
        elif 'set' in op:
            key, value = map(int, op.split()[1:])
            if len(cache) >= capacity:
                cache.popitem(last=False)
            cache[key] = value
    return results