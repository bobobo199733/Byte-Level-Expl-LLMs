def knapsack_01(weights, values, capacity):
    """
    Compute the optimal value for the 0/1 knapsack problem.

    Parameters:
        weights (list): Weights of each item.
        values (list): Values of each item.
        capacity (int): Maximum weight capacity of the knapsack.

    Returns:
        int: The maximum total value that can be carried without exceeding capacity.
    """
    if not weights or not values:
        return 0
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            if weights[i - 1] <= w:
                dp[i][w] = max(values[i - 1] + dp[i - 1][w - weights[i - 1]], dp[i - 1][w])
            else:
                dp[i][w] = dp[i - 1][w]
    return dp[n][capacity]