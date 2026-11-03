def serialize_tree(root):

    def _serialize_tree(node, visited):
        if node:
            visited.append(str(node.val))
            _serialize_tree(node.left, visited)
            _serialize_tree(node.right, visited)
        else:
            visited.append('#')

    def _deserialize_tree(nodes, index):
        if index >= len(nodes) or nodes[index] == '#':
            return None
        node = TreeNode(int(nodes[index]))
        node.left = _deserialize_tree(nodes, 2 * index + 1)
        node.right = _deserialize_tree(nodes, 2 * index + 2)
        return node
    if not root:
        return ''
    visited = []
    _serialize_tree(root, visited)
    serialized = '[' + ','.join(visited) + ']'
    deserialized_tree = _deserialize_tree(serialized[1:-1].split(','), 0)
    return serialized if root.val == deserialized_tree.val else None