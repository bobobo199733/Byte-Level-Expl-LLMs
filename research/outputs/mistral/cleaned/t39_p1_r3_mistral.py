def knapsack_01(weights, values, capacity):
    n = len(weights)
    dp = [[-1] * (capacity + 1) for _ in range(n)]

    def helper(i, w):
        if i == n or w == 0:
            return 0
        if dp[i][w] != -1:
            return dp[i][w]
        include = 0
        if weights[i] <= w:
            include = values[i] + helper(i + 1, w - weights[i])
        exclude = helper(i + 1, w)
        dp[i][w] = max(include, exclude)
        return dp[i][w]
    return helper(0, capacity)