def coin_change(coins, amount):
    if amount == 0:
        return 0
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    for coin in coins:
        for x in range(coin, amount + 1):
            dp[x] = min(dp[x], dp[x - coin] + 1)
    if dp[amount] == float('inf'):
        return -1
    return dp[amount]