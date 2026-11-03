def trapping_rain_water(heights):
    if len(heights) < 3:
        return 0
    left = [0] * len(heights)
    right = [0] * len(heights)
    max_left = heights[0]
    for i in range(1, len(heights)):
        max_left = max(max_left, heights[i])
        left[i] = max_left
    max_right = heights[-1]
    for i in reversed(range(len(heights) - 1)):
        max_right = max(max_right, heights[i + 1])
        right[i] = max_right
    trapped_water = 0
    for i in range(len(heights)):
        trapped_water += min(left[i], right[i]) - heights[i] if min(left[i], right[i]) > heights[i] else 0
    return trapped_water