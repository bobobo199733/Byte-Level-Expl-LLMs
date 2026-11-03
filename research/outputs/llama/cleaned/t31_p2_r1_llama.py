def serialize_tree(root):
    """
    Serialize a binary tree into a string representation.
    
    This function performs a pre-order traversal of the binary tree, 
    where each node's value is appended to the result string along with its children (null or empty if not present).
    
    The resulting string can be used to reconstruct the original tree using deserialize_tree().

    Args:
        root: The root of the binary tree.

    Returns:
        A string representation of the binary tree.
    """

    def helper(node):
        """
        Helper function for serialization.
        
        This recursive function appends each node's value and its children (null or empty if not present) 
        to the result string in a pre-order manner.
        """
        if node is None:
            helper_str += 'X'
        else:
            helper_str += str(node.val)
            if node.left is not None:
                helper_str += ',' + str(node.left.val)
            else:
                helper_str += ',#'
            if node.right is not None:
                helper_str += ',' + str(node.right.val)
            else:
                helper_str += '#'
        return helper_str
    result = ''
    if root:
        result = helper(root)
    if len(result) > 0 and result[-1] == ',':
        result = result[:-1]
    return result