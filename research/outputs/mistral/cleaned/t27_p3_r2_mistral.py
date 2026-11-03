def trap_rainwater(heights):
    n = len(heights)
    if n < 3:
        return 0
    left = [0] * n
    right = [0] * n
    max_left = 0
    max_right = 0
    for i in range(1, n):
        left[i] = max(left[i - 1], heights[i - 1]) if heights[i - 1] > left[i - 1] else left[i - 1]
    for i in reversed(range(0, n)):
        right[i] = max(right[i + 1], heights[i + 1]) if heights[i + 1] > right[i + 1] else right[i + 1]
    trapped_water = 0
    for i in range(n):
        water_level = min(left[i], right[i]) - heights[i]
        if water_level > 0:
            trapped_water += water_level
    return trapped_water