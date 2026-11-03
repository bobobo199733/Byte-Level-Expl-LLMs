from collections import OrderedDict

def lru_cache(operations, capacity):
    cache = OrderedDict()
    outputs = []
    for operation in operations:
        key, value = operation
        if key in cache:
            cache.move_to_end(key)
        cache[key] = value
        if isinstance(operation, tuple) and len(operation) == 2:
            outputs.append(cache.get(key, None))
    return outputs