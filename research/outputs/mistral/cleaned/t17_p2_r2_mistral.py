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
                self.head.prev = node.next
                if node.next:
                    node.next.prev = self.head
                else:
                    self.tail = self.head
            node.next = self.head
            node.prev = None
            self.head = node
        return node.value

    def put(self, key, value):
        if key in self.cache:
            node = self.cache[key]
            node.value = value
            if self.head != node:
                if self.head:
                    self.head.prev = node.next
                    if node.next:
                        node.next.prev = self.head
                    else:
                        self.tail = self.head
                node.next = self.head
                node.prev = None
                self.head = node
            return
        if len(self.cache) >= self.capacity:
            evicted_key = self.tail.key
            del self.cache[evicted_key]
            if self.tail.prev:
                self.tail.prev.next = None
                self.tail = self.tail.prev
            else:
                self.head = None
        node = Node(key, value)
        self.cache[key] = node
        if not self.head:
            self.head = node
            self.tail = node
        else:
            node.next = self.head
            self.head.prev = node
            self.head = node

def lru_cache(operations):
    cache = LRUCache(len(operations) // 2 + 1)
    results = []
    for operation in operations:
        if operation[0] == 'put':
            cache.put(operation[1], operation[2])
        elif operation[0] == 'get':
            result = cache.get(operation[1])
            results.append(result)
    return results