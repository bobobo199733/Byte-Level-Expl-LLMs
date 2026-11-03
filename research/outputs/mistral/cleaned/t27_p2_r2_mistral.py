def trapping_rain_water(heights):
    if not heights:
        return 0
    n = len(heights)
    left = [0] * n
    right = [0] * n
    left[0] = heights[0]
    for i in range(1, n):
        left[i] = max(left[i - 1], heights[i])
    right[-1] = heights[-1]
    for i in reversed(range(n - 1)):
        right[i] = max(right[i + 1], heights[i])
    total_trapped = 0
    for i in range(n):
        total_trapped += min(left[i], right[i]) - heights[i] if min(left[i], right[i]) > heights[i] else 0
    return total_trapped