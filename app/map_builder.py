SPACE = 0
WALL = 1
SNAKE = 2
FOOD = 3
SNAKE_HEAD = 4


def build_map(data):
    # create map and fill with zeros
    map = [ [0 for col in range(data['width'])] for row in range(data['height'])]
    # fill in food locations
    for food in data['food']['data']:
        map[food['x']][food['y']] = FOOD
    return map


def print_map(map):
    for i in map:
        for j in i:
            print(str(j) + ' '),
        print('\n')