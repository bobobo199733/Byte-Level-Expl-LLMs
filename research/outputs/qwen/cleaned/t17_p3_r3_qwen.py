from collections import OrderedDict

def lru_cache(operations, capacity):
    """
    Simulates an LRU Cache.

    :param operations: A list of strings representing the operations on the cache.
                       Each string is either "get" or "put" followed by two integers.
                       Example: ["put 1 2", "put 2 3", "get 1", "put 3 4", "get 2"]
    :param capacity: An integer representing the maximum number of items the cache can hold.

    :return: A list of results for each get operation. Each result is the value associated with
             the key if it exists, otherwise -1.
    """
    cache = OrderedDict()
    results = []
    for operation in operations:
        op, *args = operation.split()
        key, value = (int(args[0]), args[1])
        if op == 'put':
            if len(cache) >= capacity:
                cache.popitem(last=False)
            cache[key] = value
        elif op == 'get':
            if key in cache:
                results.append(cache.pop(key))
                cache[key] = value
            else:
                results.append(-1)
    return results