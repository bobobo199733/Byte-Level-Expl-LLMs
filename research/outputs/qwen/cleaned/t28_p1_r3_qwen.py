def robot_simulator(commands):
    """
    Simulates a robot movement on a 2D grid based on given commands.
    
    Parameters:
        commands (list of str): A list of commands where 'U' means move up, 'D' means move down,
                                'L' means move left, and 'R' means move right.
    
    Returns:
        tuple: The final position (x, y) and direction ('N', 'S', 'W', 'E') of the robot as a tuple.
    """
    x, y = (0, 0)
    direction = 'N'
    directions = ['N', 'E', 'S', 'W']
    for command in commands:
        if command == 'U':
            y += 1
        elif command == 'D':
            y -= 1
        elif command == 'L':
            x -= 1
        elif command == 'R':
            x += 1
        turns = directions.index(direction) + commands.count('R') - commands.count('L')
        turns %= 4
        direction = directions[turns]
    return ((x, y), direction)