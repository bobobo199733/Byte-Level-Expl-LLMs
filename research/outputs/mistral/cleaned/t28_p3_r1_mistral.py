def robot_simulator(commands):
    directions = {'N': [0, 1], 'E': [1, 0], 'S': [0, -1], 'W': [-1, 0]}
    position = (0, 0)
    for command in commands:
        position = tuple(map(sum, zip(position, directions[command])))
    return position