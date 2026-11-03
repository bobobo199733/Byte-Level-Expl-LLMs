def coin_change(coins, amount):
    """
    Returns the minimum number of coins needed to make up the given amount.

    Args:
        coins (list): A list of coin denominations available.
        amount (int): The target amount we want to reach.

    Returns:
        int: The minimum number of coins needed. Returns -1 if impossible.
    """
    min_coins = [float('inf')] * (amount + 1)
    min_coins[0] = 0
    for coin in coins:
        for i in range(coin, amount + 1):
            min_coins[i] = min(min_coins[i], min_coins[i - coin] + 1)
    return min_coins[amount] if min_coins[amount] != float('inf') else -1