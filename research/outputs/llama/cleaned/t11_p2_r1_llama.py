def coin_change(coins, amount):
    """
    Computes the minimum number of coins required to make the target amount.

    Args:
        coins (list): A list of positive integers representing the available coin denominations.
        amount (int): The target amount we want to achieve.

    Returns:
        int: The minimum number of coins needed. Returns -1 if it's impossible to form the target amount.
    """
    if amount == 0:
        return 0
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    for coin in coins:
        if coin <= amount:
            for i in range(coin, amount + 1):
                dp[i] = min(dp[i], dp[i - coin] + 1)
    if dp[amount] == float('inf'):
        return -1
    return dp[amount]