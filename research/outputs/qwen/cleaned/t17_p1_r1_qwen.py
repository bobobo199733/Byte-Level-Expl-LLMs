from collections import OrderedDict

def lru_cache(operations, capacity):
    cache = OrderedDict()
    outputs = []

    def get(key):
        if key not in cache:
            return -1
        value = cache.pop(key)
        cache[key] = value
        outputs.append(value)
        return value

    def put(key, value):
        if key in cache:
            cache.pop(key)
        elif len(cache) == capacity:
            cache.popitem(last=False)
        cache[key] = value
        outputs.append(value)
    for operation in operations:
        if isinstance(operation, tuple):
            op, key = operation
            if op == 'get':
                result = get(key)
                outputs.append(result)
            elif op == 'put':
                put(*operation[1:])
    return outputs