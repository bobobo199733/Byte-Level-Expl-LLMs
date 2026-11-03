def robot_simulator(commands):
    x, y, direction = 0, 0, 'N'
    directions = {
        'F': lambda pos, dir: (pos[0], pos[1] + 1 if dir == 'N' else (pos[0] + 1 if dir == 'E' else (pos[0] - 1 if dir == 'W' else pos[1] - 1))),
        'L': lambda pos, dir: ('W' if dir == 'N' else ('S' if dir == 'E' else ('N' if dir == 'W' else 'E'))),
        'R': lambda pos, dir: ('E' if dir == 'N' else ('N' if dir == 'E' else ('W' if dir == 'S' else 'S')),
    }

    for command in commands:
        x, y = directions[command][0](x, y)
        direction = directions[command][1](direction)

    return [x, y, direction]