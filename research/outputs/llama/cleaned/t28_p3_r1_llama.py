def robot_simulator(commands):
    """
    Simulates a robot's movement based on given commands.

    Args:
        commands (str): A string of commands separated by commas.
                        The commands can be 'LEFT', 'RIGHT', 'FORWARD', or 'BACKWARD'.

    Returns:
        tuple: The final position and direction of the robot as a tuple in the format
               (x, y, direction).
    """
    x, y = (0, 0)
    directions = {'NORTH': (0, 1), 'SOUTH': (0, -1), 'EAST': (1, 0), 'WEST': (-1, 0)}
    direction = 'NORTH'
    commands_list = [command.strip() for command in commands.split(',')]
    for command in commands_list:
        if command == 'LEFT':
            global_directions = list(directions.keys())
            current_index = global_directions.index(direction)
            direction = global_directions[(current_index - 1) % 4]
        elif command == 'RIGHT':
            global_directions = list(directions.keys())
            current_index = global_directions.index(direction)
            direction = global_directions[(current_index + 1) % 4]
        else:
            movement = directions[direction]
            if command == 'FORWARD':
                x += movement[0]
                y += movement[1]
            elif command == 'BACKWARD':
                x -= movement[0]
                y -= movement[1]
    return (x, y, direction)