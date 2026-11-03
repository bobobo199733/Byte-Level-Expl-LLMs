def robot_simulator(commands):
    x, y = (0, 0)
    dir = 'N'
    for c in commands:
        if c == 'F':
            if dir == 'N':
                y += 1
            elif dir == 'E':
                x += 1
            elif dir == 'S':
                y -= 1
            else:
                x -= 1
        elif c == 'L':
            if dir == 'N':
                dir = 'W'
            elif dir == 'W':
                dir = 'S'
            elif dir == 'S':
                dir = 'E'
            else:
                dir = 'N'
        elif dir == 'N':
            dir = 'E'
        elif dir == 'E':
            dir = 'S'
        elif dir == 'S':
            dir = 'W'
        else:
            dir = 'N'
    return [x, y, dir]