def trapping_rain_water(heights):
    n = len(heights)
    if n < 3:
        return 0
    left = [0] * n
    right = [0] * n
    max_left = heights[0]
    for i in range(1, n):
        left[i] = max(max_left, heights[i])
        max_left = max(max_left, heights[i])
    max_right = heights[-1]
    for i in range(n - 2, -1, -1):
        right[i] = max(max_right, heights[i])
        max_right = max(max_right, heights[i])
    result = 0
    for i in range(1, n - 1):
        result += min(left[i], right[i]) - heights[i]
    return result