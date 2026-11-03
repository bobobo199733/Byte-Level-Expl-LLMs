from collections import OrderedDict

def lru_cache(operations, capacity):
    """
    Simulates an LRU Cache.

    :param operations: A list of operations where each operation is a string in the format "put key value" or "get key".
    :param capacity: The maximum number of items that the cache can hold.
    :return: A list containing the result of each 'get' operation, with -1 indicating that the key was not found.
    """
    cache = OrderedDict()

    def get(key):
        if key in cache:
            value = cache.pop(key)
            cache[key] = value
            return value
        else:
            return -1

    def put(key, value):
        if key in cache:
            cache.pop(key)
        elif len(cache) == capacity:
            cache.popitem(last=False)
        cache[key] = value
    results = []
    for operation in operations:
        if 'get' in operation:
            _, key = operation.split()
            result = get(int(key))
            results.append(result)
        elif 'put' in operation:
            key, value = map(int, operation[5:].split())
            put(key, value)
    return results