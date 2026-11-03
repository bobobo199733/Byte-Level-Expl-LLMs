class Node:

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = None
        self.size = 0

    def get(self, key):
        if not self.cache or key not in {node.key for node in self.cache}:
            return None
        node = None
        for current_node in self.cache:
            if current_node.key == key:
                node = current_node
                break
        if self.cache:
            if node.prev:
                node.prev.next = node.next
            else:
                self.cache = node.next
            if node.next:
                node.next.prev = node.prev
            else:
                self.cache = None
            last_node = self.cache[-1]
            last_node.next = node
            node.prev = last_node
            node.next = None
            last_node.next = None
        return node.value if node else None

    def put(self, key, value):
        if self.get(key):
            self.put_without_eviction(key, value)
            return
        if self.size >= self.capacity:
            evicted_key = self.cache[0].key
            self.cache.pop(0)
            self.size -= 1
        new_node = Node(key, value)
        if not self.cache:
            self.cache = [new_node]
        else:
            last_node = self.cache[-1]
            new_node.next = None
            new_node.prev = last_node
            last_node.next = new_node
            self.cache.append(new_node)
        self.size += 1

    def put_without_eviction(self, key, value):
        for node in self.cache:
            if node.key == key:
                node.value = value
                last_node = self.cache[-1]
                node.next = None
                node.prev = last_node
                last_node.next = node
                node.next = None
                last_node.next = None
                return
        new_node = Node(key, value)
        if not self.cache:
            self.cache = [new_node]
        else:
            last_node = self.cache[-1]
            new_node.next = None
            new_node.prev = last_node
            last_node.next = new_node
            self.cache.append(new_node)