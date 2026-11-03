def robot_simulator(commands):
    """
    Simulate a robot's movement based on given commands.

    Args:
        commands (list): A list of strings containing the robot's commands. Each string is either 'UP', 'DOWN', 'LEFT', or 'RIGHT'.

    Returns:
        tuple: The final position of the robot as a tuple in the format (x, y).
    """
    x, y = (0, 0)
    for command in commands:
        if command == 'UP':
            y += 1
        elif command == 'DOWN':
            y -= 1
        elif command == 'LEFT':
            x -= 1
        elif command == 'RIGHT':
            x += 1
    return (x, y)