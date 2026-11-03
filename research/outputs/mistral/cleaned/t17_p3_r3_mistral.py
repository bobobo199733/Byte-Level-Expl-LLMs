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
        self.head = Node(0, 0)
        self.tail = Node(0, 0)
        self.head.next = self.tail
        self.tail.prev = self.head

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        self._move_to_head(self.cache[key])
        return self.cache[key].value

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache[key].value = value
            self._move_to_head(self.cache[key])
        else:
            if len(self.cache) >= self.capacity:
                last_node = self.tail.prev
                del self.cache[last_node.key]
                self._remove_node(last_node)
            new_node = Node(key, value)
            self.cache[key] = new_node
            self._add_to_head(new_node)

    def _move_to_head(self, node: Node) -> None:
        self._remove_node(node)
        self._add_to_head(node)

    def _add_to_head(self, node: Node) -> None:
        next_node = self.head.next
        next_node.prev = node
        node.next = next_node
        node.prev = self.head
        self.head.next = node

    def _remove_node(self, node: Node) -> None:
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node