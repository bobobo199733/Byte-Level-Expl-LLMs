def generate_parentheses(n):
    """
    Returns all valid parentheses combinations for a given number of pairs.

    :param n: The number of pairs of parentheses.
    :type n: int
    :return: A list of strings, where each string is a valid combination of parentheses.
    :rtype: list[str]
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