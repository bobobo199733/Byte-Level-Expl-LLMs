from collections import OrderedDict

def lru_cache(operations, capacity):
    cache = OrderedDict()
    results = []
    for op in operations:
        if op[0] == 'put':
            key = op[1]
            value = op[2]
            if key in cache:
                cache.move_to_end(key)
            cache[key] = value
            if len(cache) > capacity:
                oldest_key = next(iter(cache))
                del cache[oldest_key]
        elif op[0] == 'get':
            key = op[1]
            if key in cache:
                results.append(cache[key])
                cache.move_to_end(key)
            else:
                results.append(-1)
    return results