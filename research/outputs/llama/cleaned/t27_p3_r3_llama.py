def trapping_rain_water(heights):
    """
    Calculate the amount of trapped rainwater in a given list of heights.

    Args:
        heights (list): A list of integers representing the height of each building.

    Returns:
        int: The total amount of trapped rainwater.
    """
    left = 0
    right = len(heights) - 1
    max_left = 0
    max_right = 0
    total_water = 0
    while left < right:
        if heights[left] < heights[right]:
            max_left = max(heights[left], max_left)
            total_water += max_left - heights[left]
            left += 1
        else:
            max_right = max(heights[right], max_right)
            total_water += max_right - heights[right]
            right -= 1
    return total_water