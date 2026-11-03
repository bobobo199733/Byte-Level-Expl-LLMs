from collections import OrderedDict

def lru_cache(operations, capacity):
    cache = OrderedDict()
    accessed = set()
    results = []
    for operation in operations:
        if operation[0] == 'get':
            key, result = cache.get(operation[1], None)
            if key is not None:
                accessed.remove(key)
            results.append(result)
            if len(accessed) < capacity:
                cache[operation[1]] = operation[1]
                accessed.add(operation[1])
            elif key is None:
                least_recently_used = next(iter(accessed))
                del cache[least_recently_used]
                del accessed[least_recently_used]
                cache[operation[1]] = operation[1]
                accessed.add(operation[1])
        elif operation[0] == 'put':
            if len(accessed) >= capacity:
                least_recently_used = next(iter(accessed))
                del cache[least_recently_used]
                del accessed[least_recently_used]
            cache[operation[1]] = operation[2]
            accessed.add(operation[1])
    return results