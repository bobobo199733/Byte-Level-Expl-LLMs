def coin_change(coins, amount):
    dp = [0] + [float('inf')] * amount
    for c in coins:
        for i in range(c, amount + 1):
            dp[i] = min(dp[i], dp[i - c] + 1)
    if dp[-1] == float('inf'):
        return -1
    else:
        return dp[-1]