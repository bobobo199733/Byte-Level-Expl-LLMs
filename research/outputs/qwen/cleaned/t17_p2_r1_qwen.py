class Node:

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:

    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}
        self.head = Node(0, 0)
        self.tail = Node(0, 0)
        self.head.next = self.tail
        self.tail.prev = self.head

    def _add_node(self, node):
        """Add a new node right after the head."""
        next_node = self.head.next
        self.head.next = node
        node.prev = self.head
        node.next = next_node
        next_node.prev = node

    def _remove_node(self, node):
        """Remove an existing node from the linked list."""
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node

    def _move_to_head(self, node):
        """Move a specified node in-between to the head position."""
        self._remove_node(node)
        self._add_node(node)

    def _pop_tail(self):
        """Remove and return the node at the tail. This is the least recently used key."""
        res = self.tail.prev
        self._remove_node(res)
        return res

    def get(self, key):
        if key in self.cache:
            self._move_to_head(self.cache[key])
            return self.cache[key].value
        return -1

    def put(self, key, value):
        if key in self.cache:
            old_node = self.cache[key]
            self._remove_node(old_node)
        new_node = Node(key, value)
        self.cache[key] = new_node
        self._add_node(new_node)
        if len(self.cache) > self.capacity:
            tail_node = self._pop_tail()
            del self.cache[tail_node.key]

def lru_cache(operations, capacity):
    cache = LRUCache(capacity)
    results = []
    for operation in operations:
        if operation[0] == 'get':
            result = cache.get(operation[1])
            results.append(result)
        elif operation[0] == 'put':
            cache.put(operation[1], operation[2])
    return results