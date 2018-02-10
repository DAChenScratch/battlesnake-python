SPACE = 0
WALL = 1
FOOD = 2
SNAKE = 3
SNAKE_HEAD = 4


def build_map(data):
    # create map and fill with zeros
    print('Height: ' + str(data['height']) + '  Width: ' + str(data['width']))
    map = [ [0 for col in range(data['height'])] for row in range(data['width'])]
    # fill in food locations
    for food in data['food']['data']:
        map[food['x']][food['y']] = FOOD
    # fill in snake locations
    for snake in data['snakes']['data']:
        for segment in snake['body']['data']:
            # get each segment from data{snakes, data, body, data}
            map[segment['x']][segment['y']] = SNAKE
        # mark snake head locations
        map[snake['body']['data'][0]['x']][snake['body']['data'][0]['y']] = SNAKE_HEAD

    return map



def print_map(map, w, h):
    for row in map:
        print(str(row))
        print('\n')