def trapping_rain_water(heights):
    if len(heights) <= 2:
        return 0
    left = [None] * len(heights)
    right = [None] * len(heights)
    stack, max_height, left_index = ([], float('-inf'), 0)
    for i in range(len(heights)):
        while stack and heights[stack[-1]] <= heights[i]:
            stack.pop()
        if not stack:
            left[i] = max_height
        else:
            left[i] = stack[-1]
        stack.append(i)
    stack, max_height, right_index = ([], float('-inf'), len(heights) - 1)
    for i in reversed(range(len(heights))):
        while stack and heights[stack[-1]] > heights[i]:
            stack.pop()
        if not stack:
            right[i] = max_height
        else:
            right[i] = stack[-1]
        stack.append(i)
    volume = 0
    for i in range(len(heights)):
        volume += min(left[i], right[i]) - heights[i] if left[i] <= right[i] else 0
    return volume