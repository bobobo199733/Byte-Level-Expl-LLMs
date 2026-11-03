class Node:

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}
        self.head = None
        self.tail = None

    def get(self, key):
        if key not in self.cache:
            return None
        node = self.cache[key]
        if self.head != node:
            if self.head:
                self.head.prev = node.prev
            else:
                self.tail = node
            if node.next:
                node.next.prev = node.prev
            else:
                self.head = node
            node.prev, node.next = (self.head, self.head.next)
            self.head.next = node
        return self.cache[key]['value']

    def put(self, key, value):
        if key in self.cache:
            self.cache[key]['value'] = value
            node = self.cache[key]
            if self.head != node:
                if self.head:
                    self.head.prev = node.prev
                else:
                    self.tail = node
                if node.next:
                    node.next.prev = node.prev
                else:
                    self.head = node
                node.prev, node.next = (self.head, self.head.next)
                self.head.next = node
        else:
            if len(self.cache) >= self.capacity:
                evicted_key = self.tail.key
                del self.cache[evicted_key]
                if self.head == self.tail:
                    self.head = None
                else:
                    self.tail = self.tail.prev
                    self.tail.next = None
            self.cache[key] = {'value': value}
            node = Node(key, value)
            if not self.head:
                self.head = node
                self.tail = node
            else:
                node.next = self.head
                self.head.prev = node
                self.head = node

def lru_cache(operations, capacity):
    cache = LRUCache(capacity)
    results = []
    for operation in operations:
        if operation[0] == 'put':
            cache.put(operation[1], operation[2])
        elif operation[0] == 'get':
            results.append(cache.get(operation[1]))
    return results