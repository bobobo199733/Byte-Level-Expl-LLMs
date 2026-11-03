from collections import OrderedDict

def lru_cache(operations, capacity):
    cache = OrderedDict()
    accessed = set()
    for op in operations:
        if op[0] == 'get':
            if not cache or op[1] not in cache:
                print(f'Miss: {op[1]}')
            else:
                cache.move_to_end(op[1])
                print(f'Hit: {op[1]}')
            result = cache.get(op[1], None)
        elif op[0] == 'put':
            if op[1] in cache:
                cache.move_to_end(op[1])
                accessed.discard(op[1])
            elif len(cache) >= capacity:
                least_recently_used = cache.popitem(last=False)
                print(f'Eviction: {least_recently_used[0]}')
            cache[op[1]] = op[2]
            accessed.add(op[1])
            print(f'Put: {op[1]}')
        yield result