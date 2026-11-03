def robot_simulator(commands):
    x = 0
    y = 0
    for command in commands:
        if command == 'U':
            y += 1
        elif command == 'D':
            y -= 1
        elif command == 'L':
            x -= 1
        elif command == 'R':
            x += 1
    return (x, y)