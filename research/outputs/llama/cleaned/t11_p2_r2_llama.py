def coin_change(coins, amount):
    """
    Compute the minimum number of coins required to make the target amount.
    
    Args:
        coins (list): A list of positive integers representing coin denominations.
        amount (int): The target amount to be made up with coins.
        
    Returns:
        int: The minimum number of coins required. Returns -1 if it's impossible to form the target amount.
    """
    if amount < 0:
        return -1
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    for coin in coins:
        for i in range(coin, amount + 1):
            dp[i] = min(dp[i], dp[i - coin] + 1)
    return dp[amount] if dp[amount] != float('inf') else -1