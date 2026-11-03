def trapping_rain_water(heights):
    """
    Calculate the amount of rainwater that can be trapped between bars.

    Args:
        heights (list): A list of integers representing bar heights.

    Returns:
        int: The total amount of rainwater that can be trapped.
    """
    if not heights:
        return 0
    left_max, right_max = ([heights[0]], [heights[-1]])
    for i in range(1, len(heights)):
        left_max.append(max(left_max[i - 1], heights[i]))
    for i in reversed(range(len(heights) - 1)):
        right_max.append(max(right_max[i + 1], heights[i]))
    return sum((min(lmax, rmax) - h for lmax, h, rmax in zip(left_max, heights, reversed(right_max))))