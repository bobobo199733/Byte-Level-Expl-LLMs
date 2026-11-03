def trapping_rain_water(heights):
    if not heights:
        return 0
    n = len(heights)
    left, right = ([0] * n, [0] * n)
    left[1] = heights[0]
    for i in range(2, n):
        left[i] = max(left[i - 1], heights[i])
    right[-1] = heights[-1]
    for i in range(n - 2, -1, -1):
        right[i] = max(right[i + 1], heights[i])
    result = 0
    for i in range(n):
        result += min(left[i], right[i]) - heights[i]
    return result