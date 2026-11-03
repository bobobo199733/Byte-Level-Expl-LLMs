def serialize_tree(root):

    def helper(node):
        if node is None:
            return 'None,'
        else:
            return f'{node.val},'
    result = ''
    stack = [root]
    while stack:
        current_node = stack.pop()
        if current_node == 'None':
            continue
        result += helper(current_node)
        stack.append(helper(current_node.right))
        stack.append(helper(current_node.left))
    return result.strip(',')