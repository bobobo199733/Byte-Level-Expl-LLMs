def coin_change(coins, amount):
    """
    Compute the minimum number of coins required to make the target amount.

    Args:
        coins (list): A list of positive integers representing coin values.
        amount (int): The target amount that needs to be formed using coins.

    Returns:
        int: The minimum number of coins required to form the target amount. 
             Returns -1 if it's impossible to form the target amount.
    """
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    for coin in coins:
        for i in range(coin, amount + 1):
            dp[i] = min(dp[i], dp[i - coin] + 1)
    if dp[amount] == float('inf'):
        return -1
    return dp[amount]