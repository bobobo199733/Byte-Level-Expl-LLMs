def knapsack_01(weights, values, capacity):
    """
    Compute the maximum value that can be obtained without exceeding the capacity.
    
    Args:
        weights (list): List of item weights.
        values (list): List of item values corresponding to the weights.
        capacity (int): Maximum capacity of the knapsack.
        
    Returns:
        int: The optimal total value for the 0/1 knapsack problem.
    """
    if not weights or not values:
        return 0
    dp = [[0] * (capacity + 1) for _ in range(len(weights) + 1)]
    for i in range(1, len(weights) + 1):
        for j in range(1, capacity + 1):
            if weights[i - 1] <= j:
                dp[i][j] = max(values[i - 1] + dp[i - 1][j - weights[i - 1]], dp[i - 1][j])
            else:
                dp[i][j] = dp[i - 1][j]
    return dp[-1][-1]