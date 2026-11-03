def coin_change(coins, amount):
    """
    Finds the smallest number of coins needed to make the given amount.

    Args:
        coins (list): A list of available coin denominations.
        amount (int): The target amount to reach.

    Returns:
        int: The minimum number of coins required. -1 if impossible.
    """
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i and dp[i - coin] + 1 < dp[i]:
                dp[i] = dp[i - coin] + 1
    return dp[amount] if dp[amount] != float('inf') else -1