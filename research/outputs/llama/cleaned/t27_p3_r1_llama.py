def trapping_rain_water(heights):
    """
    Calculate the total amount of rain water that can be trapped between bars in a histogram.

    Args:
        heights (list): A list of integers representing the height of each bar in the histogram.

    Returns:
        int: The total amount of rain water that can be trapped.
    """
    left = 0
    right = len(heights) - 1
    max_left = heights[left]
    max_right = heights[right]
    total_water = 0
    while left <= right:
        if max_left < max_right:
            total_water += max(0, max_left - heights[left]) * (right - left)
            left += 1
            max_left = max(heights[left], max_left)
        else:
            total_water += max(0, max_right - heights[right]) * (right - left)
            right -= 1
            max_right = max(heights[right], max_right)
    return total_water