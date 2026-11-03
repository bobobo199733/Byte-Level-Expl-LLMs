def coin_change(coins, amount):
    """
    Finds the smallest number of coins needed to make the given amount.

    Args:
        coins (list): A list of available coin denominations.
        amount (int): The target amount.

    Returns:
        int: The minimum number of coins required. Returns -1 if impossible.
    """
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    for coin in coins:
        for i in range(coin, amount + 1):
            dp[i] = min(dp[i], dp[i - coin] + 1)
    return dp[amount] if dp[amount] != float('inf') else -1