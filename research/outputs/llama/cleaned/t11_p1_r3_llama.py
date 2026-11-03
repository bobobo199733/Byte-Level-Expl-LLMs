def coin_change(coins, amount):
    """
    Returns the minimum number of coins needed to make up the given amount.
    
    Parameters:
    coins (list): List of available coin denominations.
    amount (int): Target amount to make up with coins.
    
    Returns:
    int: Minimum number of coins required. Returns -1 if impossible.
    """
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    for coin in coins:
        for i in range(coin, amount + 1):
            dp[i] = min(dp[i], dp[i - coin] + 1)
    return dp[amount] if dp[amount] != float('inf') else -1