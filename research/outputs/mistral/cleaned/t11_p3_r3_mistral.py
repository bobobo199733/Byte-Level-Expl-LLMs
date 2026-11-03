def coin_change(coins, amount):
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    for i in range(len(coins)):
        for j in range(coins[i], amount + 1):
            dp[j] = min(dp[j], dp[j - coins[i]] + 1)
    if dp[-1] == float('inf'):
        return -1
    else:
        return dp[-1]