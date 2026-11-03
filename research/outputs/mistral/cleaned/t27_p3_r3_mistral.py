def trapping_rain_water(heights):
    n = len(heights)
    if n < 3:
        return 0
    left, right = ([0] * n, [0] * n)
    max_left = [0] * n
    max_right = [0] * n
    for i in range(1, n):
        max_left[i] = max(max_left[i - 1], heights[i - 1])
    for i in reversed(range(n - 1)):
        max_right[i] = max(max_right[i + 1], heights[i + 1])
    total = 0
    for i in range(n):
        min_height = min(max_left[i], max_right[i])
        if min_height > heights[i]:
            total += min_height - heights[i]
    return total