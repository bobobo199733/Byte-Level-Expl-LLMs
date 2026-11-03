def robot_simulator(commands):
    """
    Simulate a robot moving on a grid based on given commands.

    Args:
        commands (list): A list of strings representing commands to move the robot.
                         'L' or 'R' to turn, and 'F' or 'B' to move forward or backward respectively.

    Returns:
        tuple: The final position (x, y) and direction ('N', 'S', 'E', 'W') of the robot.
    """
    grid_size = 4
    x, y = (grid_size // 2, grid_size // 2)
    directions = ['N', 'S', 'E', 'W']
    direction_index = 0
    for command in commands:
        if command == 'L':
            direction_index = (direction_index - 1) % 4
        elif command == 'R':
            direction_index = (direction_index + 1) % 4
        elif command == 'F':
            if directions[direction_index] in ['N', 'S']:
                y += -1 if directions[direction_index] == 'N' else 1
            else:
                x += -1 if directions[direction_index] == 'W' else 1
        elif command == 'B':
            if directions[direction_index] in ['N', 'S']:
                y -= -1 if directions[direction_index] == 'N' else 1
            else:
                x -= -1 if directions[direction_index] == 'W' else 1
    return ((x, y), directions[direction_index])