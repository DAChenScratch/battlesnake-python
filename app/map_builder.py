SPACE = 0
WALL = 1
SNAKE = 2
FOOD = 3
SNAKE_HEAD = 4


def build_map(data):
    map = [ [0 for col in range(data['height'])] for row in range(data['width'])]

    for food in data['food']['data']:
        map[food[0]][food[1]] = FOOD

    return map


def print_map(map):

    for i in map:
        for j in i:
            print(str(map[i][j]) + ' ')