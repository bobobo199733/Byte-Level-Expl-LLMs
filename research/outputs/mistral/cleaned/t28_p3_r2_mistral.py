def robot_simulator(commands):
    direction = 'E'
    position = [0, 0]
    moves = {'F': lambda: (position[0], position[1] + 1), 'B': lambda: (position[0], position[1] - 1), 'L': lambda deg: (position[0] - int(deg / 90), position[1]), 'R': lambda deg: (position[0] + int(deg / 90), position[1])}
    for command in commands:
        if command not in moves:
            raise ValueError('Invalid command')
        position = moves[command]()
        angle = (direction == 'N') - (direction == 'S')
        direction = turns(angle, int((deg for cmd in ['L', 'R'] if command == cmd))[0])[1]
    return position

def turns(angle, degree):
    directions = {N: ('E', 'S'), S: ('W', 'N'), E: ('N', 'W'), W: ('S', 'E')}
    for direction, valid_degrees in directions.items():
        if all((degree % 90 == dg for dg in valid_degrees)):
            return (direction, degree // 90)