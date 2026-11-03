def robot_simulator(commands):
    """
    Simulates robot movement based on given commands.

    Args:
        commands (str): Sequence of F, L, R moves.

    Returns:
        list: Final position and direction [x, y, direction] where direction is "N", "E", "S", or "W".
    """
    x, y = (0, 0)
    direction = 'N'
    for command in commands:
        if command == 'F':
            if direction == 'N':
                y += 1
            elif direction == 'S':
                y -= 1
            elif direction == 'E':
                x += 1
            elif direction == 'W':
                x -= 1
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
    return [x, y, direction]