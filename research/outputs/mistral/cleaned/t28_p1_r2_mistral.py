def robot_simulator(commands):
    pos = (0, 0)
    direction = 'E'
    for command in commands:
        if command == 'F':
            if direction == 'N':
                pos = (pos[0], pos[1] + 1)
            elif direction == 'S':
                pos = (pos[0], pos[1] - 1)
            elif direction == 'E':
                pos = (pos[0] + 1, pos[1])
            elif direction == 'W':
                pos = (pos[0] - 1, pos[1])
        elif command == 'L':
            if direction == 'N':
                direction = 'W'
            elif direction == 'S':
                direction = 'E'
            elif direction == 'E':
                direction = 'N'
            elif direction == 'W':
                direction = 'S'
        elif command == 'R':
            if direction == 'N':
                direction = 'E'
            elif direction == 'S':
                direction = 'W'
            elif direction == 'E':
                direction = 'S'
            elif direction == 'W':
                direction = 'N'
    return (pos, direction)