def trapping_rain_water(heights):
    """
    Calculate the volume of trapped rainwater in a given array of building heights.

    Args:
        heights (list): A list of integers representing the height of each building.

    Returns:
        int: The total volume of water that can be trapped between buildings.
    """
    left = 0
    right = len(heights) - 1
    max_left = 0
    max_right = 0
    total_water = 0
    while left <= right:
        if heights[left] > max_left:
            max_left = heights[left]
            total_water += (max_left - heights[left]) * (left - 0)
        else:
            total_water += (max_left - heights[left]) * (left - 0)
        if heights[right] > max_right:
            max_right = heights[right]
            total_water += (max_right - heights[right]) * (len(heights) - 1 - right)
        else:
            total_water += (max_right - heights[right]) * (len(heights) - 1 - right)
        if heights[left] < heights[right]:
            left += 1
        else:
            right -= 1
    return total_water