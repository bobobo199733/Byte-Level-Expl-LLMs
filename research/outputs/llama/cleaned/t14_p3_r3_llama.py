def generate_parentheses(n):
    """
    Generates all possible combinations of well-formed parentheses.

    Args:
        n (int): The number of pairs of parentheses.

    Returns:
        list: A list of strings representing valid combinations.
    """

    def backtrack(open_count, close_count, current_combination):
        if len(current_combination) == 2 * n:
            result.append(''.join(current_combination))
            return
        if open_count < n:
            current_combination.append('(')
            backtrack(open_count + 1, close_count, current_combination)
            current_combination.pop()
        if close_count < open_count:
            current_combination.append(')')
            backtrack(open_count, close_count + 1, current_combination)
            current_combination.pop()
    result = []
    backtrack(0, 0, [])
    return result