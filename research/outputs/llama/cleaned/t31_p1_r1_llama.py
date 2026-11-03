def serialize_tree(root):
    if root is None:
        return 'X,'
    serialized_left = serialize_tree(root.left)
    serialized_right = serialize_tree(root.right)
    return f'{root.val},{serialized_left}{serialized_right}'