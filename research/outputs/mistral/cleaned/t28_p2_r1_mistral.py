def robot_simulator(commands):
    x, y, direction = (0, 0, 'N')
    moves = {'F': lambda: (x, y, _get_direction(direction)), 'L': lambda: (_turn_left(direction), (x, y)), 'R': lambda: (_turn_right(direction), (x, y))}
    for cmd in commands:
        move = moves.get(cmd)
        if move is None:
            raise ValueError(f"Invalid command '{cmd}'.")
        x, y, direction = move()
    return [x, y, direction]

def _turn_left(direction):
    directions = {'N': 'W', 'E': 'N', 'S': 'E', 'W': 'S'}
    return directions[direction]

def _get_direction(direction):
    if direction == 'N':
        return 'North'
    elif direction == 'E':
        return 'East'
    elif direction == 'S':
        return 'South'
    else:
        return 'West'