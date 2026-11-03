def robot_simulator(commands):
    """
    Simulates a robot's movement based on a list of commands.

    Args:
        commands (list): A list of strings representing the commands to execute.
            Valid commands are 'L' (left), 'R' (right), and 'A', 'D' (forward and backward, respectively).
            The third element in each command is optional and represents the distance to move.

    Returns:
        tuple: A tuple containing two integers representing the final coordinates of the robot.
    """
    x = 0
    y = 0
    for command in commands:
        if len(command) == 1 or (len(command) == 3 and command[2].isdigit()):
            action, *distance = command
        else:
            continue
        if action in ['L', 'R']:
            directions = {'L': -1, 'R': 1}
            x += directions[action] * distance[0] % 360
        elif action in ['A', 'D']:
            directions = {'A': -90, 'D': 90}
            if len(command) == 3:
                distance = int(distance[0])
            x += directions[action] * distance[0] // 360
    return (x, y)