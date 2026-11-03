def generate_parentheses(n):
    """
    Generate all valid parentheses combinations for n pairs.

    Args:
        n (int): Number of pairs of parentheses.

    Returns:
        list[str]: List of strings representing the valid combinations.
    """

    def backtrack(opened, current_combination, max_depth):
        if len(current_combination) == 2 * n:
            result.append(''.join(current_combination))
            return
        if opened < max_depth:
            current_combination.append('(')
            backtrack(opened + 1, current_combination, max_depth)
            current_combination.pop()
        current_combination.append(')')
        backtrack(opened, current_combination, max_depth)
        current_combination.pop()
    result = []
    backtrack(0, [], n)
    return result