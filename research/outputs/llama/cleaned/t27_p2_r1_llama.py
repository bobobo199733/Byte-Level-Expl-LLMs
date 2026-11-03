def trapping_rain_water(heights):
    """
    Compute the total trapped rain water in a given set of building heights.

    Args:
        heights (list): A list of non-negative integers representing building heights.

    Returns:
        int: The total amount of trapped rain water.
    """
    if not heights:
        return 0
    left_max = [0] * len(heights)
    right_max = [0] * len(heights)
    left_max[0] = heights[0]
    for i in range(1, len(heights)):
        left_max[i] = max(left_max[i - 1], heights[i])
    right_max[-1] = heights[-1]
    for i in range(len(heights) - 2, -1, -1):
        right_max[i] = max(right_max[i + 1], heights[i])
    trapped_water = 0
    for i in range(len(heights)):
        trapped_water += min(left_max[i], right_max[i]) - heights[i]
    return trapped_water