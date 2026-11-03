from collections import OrderedDict
import time

def lru_cache(operations, capacity):
    """
    Simulates an LRU cache and returns the outputs of all get operations.
    
    Parameters:
    operations (list): A list of tuples where each tuple contains a key-value pair to be inserted or updated in the cache, 
                       followed by a key for which the most recent value is to be retrieved from the cache. If the key 
                       exists in the cache, its value will be returned; otherwise None will be returned.
    capacity (int): The maximum number of items that can be stored in the cache.

    Returns:
    list: A list of the outputs of all get operations.
    """
    cache = OrderedDict()
    outputs = []
    for op in operations:
        if len(op) == 3:
            key, value = (op[0], op[1])
            cache[key] = value
            if len(cache) > capacity:
                cache.popitem(last=False)
        else:
            key = op[0]
            if key in cache:
                outputs.append(cache[key])
                cache.move_to_end(key)
    return outputs