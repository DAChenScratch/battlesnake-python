SPACE = 0
WALL = 1
SNAKE = 2
FOOD = 3
SNAKE_HEAD = 4


def build_map(data):
    # create map and fill with zeros
    print('Height: ' + str(data['height']) + '  Width: ' + str(data['width']))
    map = [ [0 for col in range(data['height'])] for row in range(data['width'])]
    # fill in food locations
    for food in data['food']['data']:
        map[food['y']][food['x']] = FOOD
    return map


def print_map(map, w, h):
    for i in range(h):
        for j in range(w):
            print(str(map[i][j])),
        print('\n')