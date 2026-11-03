def knapsack_01(weights, values, capacity):
    """
    Solves the 0/1 knapsack problem using dynamic programming.

    Parameters:
        weights (list): list of item weights
        values (list): list of item values
        capacity (int): maximum weight capacity

    Returns:
        int: maximum achievable value
    """
    dp = [[0 for _ in range(capacity + 1)] for _ in range(len(weights) + 1)]
    for i in range(1, len(weights) + 1):
        for w in range(1, capacity + 1):
            if weights[i - 1] <= w:
                dp[i][w] = max(values[i - 1] + dp[i - 1][w - weights[i - 1]], dp[i - 1][w])
            else:
                dp[i][w] = dp[i - 1][w]
    return dp[-1][-1]