def robot_simulator(commands):
    x = 0
    y = 0
    direction = 'N'
    directions = {'F': lambda d: (x, y, d) if d == 'N' else (x, y, 'E') if d == 'S' and y > 0 else (x, y, 'W') if d == 'N' and x > 0 else (x, y, 'S'), 'L': (lambda d: 'N' if d == 'E' else 'W' if d == 'N' else 'S' if d == 'W' else 'E') if direction != 'N' else None, 'R': (lambda d: 'S' if d == 'W' else 'E' if d == 'N' else 'N' if d == 'S' else 'W') if direction != 'N' else None}
    for command in commands:
        if directions[command]:
            [x, y, direction] = directions[command](direction)
        else:
            raise ValueError(f"Invalid command '{command}'")
    return [x, y, direction]