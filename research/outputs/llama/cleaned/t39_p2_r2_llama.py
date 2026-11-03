def knapsack_01(weights, values, capacity):
    """
    Compute the optimal value for the 0/1 knapsack problem.

    Parameters:
        weights (list): List of item weights.
        values (list): List of corresponding item values.
        capacity (int): Maximum weight capacity.

    Returns:
        int: Optimal total value.

    Raises:
        ValueError: If input lists are not of the same length or if capacity is negative.
    """
    if len(weights) != len(values):
        raise ValueError('Input lists must be of the same length')
    if capacity < 0:
        raise ValueError('Capacity cannot be negative')
    if not weights or not values:
        return 0
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, capacity + 1):
            if weights[i - 1] <= j:
                dp[i][j] = max(values[i - 1] + dp[i - 1][j - weights[i - 1]], dp[i - 1][j])
            else:
                dp[i][j] = dp[i - 1][j]
    return dp[n][capacity]