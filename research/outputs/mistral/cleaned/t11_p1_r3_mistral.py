def coin_change(coins, amount):
    dp = [float('inf')] + [0] * amount
    for c in coins:
        for j in range(c, amount + 1):
            dp[j] = min(dp[j], dp[j - c] + 1)
    if dp[-1] >= amount:
        return -1
    else:
        return dp[-1]