def robot_simulator(commands):
    x, y = (0, 0)
    direction = 0
    for command in commands:
        if command == 'G':
            if direction == 0:
                y += 1
            elif direction == 1:
                x += 1
            elif direction == 2:
                y -= 1
            elif direction == 3:
                x -= 1
        elif command == 'L':
            direction = (direction + 3) % 4
        elif command == 'R':
            direction = (direction + 1) % 4
    return (x, y)