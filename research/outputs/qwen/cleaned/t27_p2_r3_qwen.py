def trapping_rain_water(heights):
    if not heights:
        return 0
    left, right = (0, len(heights) - 1)
    max_left, max_right = (0, 0)
    trapped_water = 0
    while left < right:
        if heights[left] <= heights[right]:
            if heights[left] >= max_left:
                max_left = heights[left]
            else:
                trapped_water += max_left - heights[left]
            left += 1
        else:
            if heights[right] >= max_right:
                max_right = heights[right]
            else:
                trapped_water += max_right - heights[right]
            right -= 1
    return trapped_water