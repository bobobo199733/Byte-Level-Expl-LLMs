def knapsack_01(weights, values, capacity):
    """
    Solves the 0/1 Knapsack problem.

    Args:
        weights (list): List of item weights.
        values (list): List of item values corresponding to weights.
        capacity (int): Maximum weight capacity of the knapsack.

    Returns:
        int: Maximum achievable value.
    """
    n = len(values)
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]
    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            if weights[i - 1] <= w:
                dp[i][w] = max(values[i - 1] + dp[i - 1][w - weights[i - 1]], dp[i - 1][w])
            else:
                dp[i][w] = dp[i - 1][w]
    return dp[n][capacity]