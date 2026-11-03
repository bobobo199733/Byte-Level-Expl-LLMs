def knapsack_01(weights, values, capacity):
    """
    Solve the 0/1 Knapsack problem.

    Args:
        weights (list): List of item weights.
        values (list): List of item values.
        capacity (int): Maximum weight capacity of the knapsack.

    Returns:
        int: The maximum possible value that can be put in the knapsack.

    Example:
        >>> weights = [2, 3, 4]
        >>> values = [5, 6, 7]
        >>> capacity = 10
        >>> print(knapsack_01(weights, values, capacity))
        14
    """
    n = len(values)
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]
    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            if weights[i - 1] <= w:
                include = values[i - 1] + dp[i - 1][w - weights[i - 1]]
                exclude = dp[i - 1][w]
                dp[i][w] = max(include, exclude)
            else:
                dp[i][w] = dp[i - 1][w]
    return dp[n][capacity]