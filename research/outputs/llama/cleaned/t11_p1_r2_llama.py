def coin_change(coins, amount):
    """
    Returns the minimum number of coins needed to make up the given amount.

    Args:
        coins (list): A list of coin denominations.
        amount (int): The target amount.

    Returns:
        int: The minimum number of coins needed. Returns -1 if it's not possible.
    """
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    for coin in coins:
        for i in range(coin, amount + 1):
            dp[i] = min(dp[i], dp[i - coin] + 1)
    return dp[amount] if dp[amount] != float('inf') else -1