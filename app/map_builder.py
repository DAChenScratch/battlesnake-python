SPACE = 0
WALL = 1
SNAKE = 2
FOOD = 3
SNAKE_HEAD = 4


def build_map(data):
    # create map and fill with zeros
    print('Height: ' + data['height'] + '  Width: ' + data['width'])
    map = [ [0 for col in range(data['height'])] for row in range(data['width'])]
    # fill in food locations
    for food in data['food']['data']:
        map[food['y']][food['x']] = FOOD
    return map


def print_map(map):
    for y in map:
        for x in y:
            print(str(x) + ' '),
        print('\n')