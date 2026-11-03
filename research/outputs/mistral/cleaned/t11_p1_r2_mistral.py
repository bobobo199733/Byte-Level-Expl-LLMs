def coin_change(coins, amount):
    if not coins or amount < 1:
        return -1
    dp = [0] + [float('inf')] * amount
    for c in coins:
        for i in range(c, amount + 1):
            dp[i] = min(dp[i], dp[i - c] + 1)
    if dp[-1] == float('inf'):
        return -1
    return dp[-1]