import bottle
import os
import time

debug = True
# board variables
SPACE = 0
FOOD = 1
MY_HEAD = 2
SNAKE_BODY = 3
ENEMY_HEAD = 4
WALL = 5
directions = ['up', 'left', 'down', 'right']
# general variables
direction = 0
# a* variables



@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


# respond on /start
@bottle.post('/start')
def start():
    data = bottle.request.json
    game_id = data['game_id']
    board_width = data['width']
    board_height = data['height']
    # get head pic url
    head_url = '%s://%s/static/snake_profile.png' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )
    # TODO: Do things with data
    return {
        'color': '#99ccff',
        'secondary_color': '#99ddff',
        'taunt': 'Not cool peep.',
        'head_url': head_url,
        'name': 'zero_cool'
    }


# respond on /move
@bottle.post('/move')
def move():
    global direction
    global directions
    data = bottle.request.json
    # build current map using game data
    start_time = time.time()
    map = build_map(data)
    # run ai to get next direction
    direction = kill_time(direction, data)
    # print data for debugging
    if debug:
        print_map(map)
        print(directions[direction])
        end_time = time.time()
        print('Time for move was ' + str((end_time - start_time) * 1000) + 'ms')
    # return next move
    return {
        'move': directions[direction],
        'taunt': 'Not cool.'
    }


# test ai
def kill_time(direction, data):
    if debug:
        print('Killing time..')
        close_food = closest_food(data)
        print(close_food)

    direction += 1
    if direction == body_direction(data):
        direction += 1
    if direction > 3:
        direction = 0
    return direction


# convert object yx to list yx
def get_coords (o):
    return (o['x'], o['y'])


# return manhattan distance between a and b
def get_distance(a, b):
    return (abs(a[0] - b[0]) + abs(a[1] - b[1]))


# return coords of closest food to head
def closest_food(data):
    current = current_location(data)
    shortest_distance = -1
    closest_food = None
    foods = data['food']['data']
    # iterate over each piece of food
    for food in foods:
        food = get_coords(food)
        distance = get_distance(current, food)
        if shortest_distance < 0:
            shortest_distance = distance
            closest_food = food
        else:
            if distance < shortest_distance:
                shortest_distance = distance
                closest_food = food
    return closest_food


# return x,y coords of current head location
def current_location(data):
    return (data['you']['body']['data'][0]['x'], data['you']['body']['data'][0]['y'])


# return direction of previous body segment from head segment
def body_direction(data):
    coord_head = get_coords(data['you']['body']['data'][0])
    coord_body = get_coords(data['you']['body']['data'][1])
    x = coord_head[0] - coord_body[0]
    y = coord_head[1] - coord_body[1]
    direction = 0
    # directions = ['up', 'left', 'down', 'right']
    if x < 0:
        direction = 3
    elif x > 0:
        direction = 1
    elif y < 0:
        direction = 2
    return direction


# return map array
def build_map(data):
    # create map and fill with zeros
    #print('Height: ' + str(data['height']) + '  Width: ' + str(data['width']))
    map = [ [SPACE for col in range(data['height'])] for row in range(data['width'])]
    # fill in food locations
    for food in data['food']['data']:
        map[food['x']][food['y']] = FOOD
    # fill in snake locations
    for snake in data['snakes']['data']:
        for segment in snake['body']['data']:
            # get each segment from data{snakes, data, body, data}
            map[segment['x']][segment['y']] = SNAKE_BODY
        # mark snake head locations
        map[snake['body']['data'][0]['x']][snake['body']['data'][0]['y']] = ENEMY_HEAD
    # mark my head location
    map[data['you']['body']['data'][0]['x']][data['you']['body']['data'][0]['y']] = MY_HEAD
    return map


# print whole map
def print_map(map):
    for row in map:
        print(str(row))


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))