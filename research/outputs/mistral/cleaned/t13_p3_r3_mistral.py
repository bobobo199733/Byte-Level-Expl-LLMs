def spiral_order(matrix):
    if not matrix or not matrix:
        return []
    top = 0
    bottom = len(matrix) - 1
    left = 0
    right = len(matrix[0]) - 1
    direction = 'right'
    result = []
    while True:
        if direction == 'right':
            for i in range(left, right + 1):
                result.append(matrix[top][i])
            top += 1
            if top > bottom:
                break
            for i in range(top, bottom + 1):
                result.append(matrix[i][right])
            right -= 1
            if left > right:
                direction = 'down'
        elif direction == 'down':
            for i in range(right, left - 1, -1):
                result.append(matrix[bottom][i])
            bottom -= 1
            if top > bottom:
                direction = 'left'
            for i in range(bottom, top - 1, -1):
                result.append(matrix[i][left])
            left += 1
            if left > right:
                direction = 'right'
        elif direction == 'left':
            for i in range(left - 1, right, -1):
                result.append(matrix[top][i])
            top += 1
            if top > bottom:
                direction = 'up'
        elif direction == 'up':
            for i in range(top, bottom + 1):
                result.append(matrix[i][left])
            left += 1
            if left > right:
                direction = 'left'
    return result