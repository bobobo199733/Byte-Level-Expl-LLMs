def robot_simulator(commands):
    """
    Simulates a robot moving on a grid.

    Args:
        commands (str): A string of space-separated commands ('LEFT', 'RIGHT', 'UP', 'DOWN', 'FORWARD').

    Returns:
        tuple: The final position and direction of the robot as a tuple (x, y, direction).
    """
    x, y = (0, 0)
    directions = ['north', 'east', 'south', 'west']
    offsets = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    direction_index = 0
    for command in commands.split():
        if command == 'FORWARD':
            x += offsets[direction_index][0]
            y += offsets[direction_index][1]
        elif command == 'LEFT':
            direction_index = (direction_index - 1) % 4
        elif command == 'RIGHT':
            direction_index = (direction_index + 1) % 4
    return (x, y, directions[direction_index])