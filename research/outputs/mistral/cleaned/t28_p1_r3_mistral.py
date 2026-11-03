def robot_simulator(commands):
    directions = {'L': (0, -1), 'R': (0, 1), 'F': (1, 0)}
    position = (0, 0)
    direction = (0, 1)
    for command in commands:
        if command not in directions:
            raise ValueError(f"Invalid command '{command}'")
        else:
            new_position = tuple(map(sum, zip(position, directions[command])))
            position = new_position
            direction = directions[command]
    return (position, direction)