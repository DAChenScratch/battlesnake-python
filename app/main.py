import bottle
import os
import time

SPACE = 0
FOOD = 1
MY_HEAD = 2
SNAKE_BODY = 3
ENEMY_HEAD = 4
WALL = 5
debug = True

directions = ['up', 'left', 'down', 'right']
test_direction = 0


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
    global test_direction
    global directions
    data = bottle.request.json

    # build current map using game data
    start_time = time.time()
    map = build_map(data)

    # run ai to get next direction
    test_direction = test_ai(test_direction, data)

    # print data for debugging
    if debug:
        print_map(map, data['width'], data['height'])
        print(directions[test_direction])
        end_time = time.time()
        print('Time for move was ' + str((end_time - start_time) * 1000) + 'ms')
    
    return {
        'move': directions[test_direction],
        'taunt': 'battlesnake-python!'
    }


# test ai
def test_ai(direction, data):
    direction += 1
    if direction == body_direction(data):
        direction += 1
    if direction > 3:
        direction = 0
    return direction


# return direction of previous body segment from head segment
def body_direction(data):
    x1 = data['you']['body']['data'][0]['x']
    y1 = data['you']['body']['data'][0]['y']
    x2 = data['you']['body']['data'][1]['x']
    y2 = data['you']['body']['data'][1]['y']
    x = x1 - x2
    y = y1 - y2
    direction = None
    #directions = ['up', 'left', 'down', 'right']
    if x < 0:
        direction = 3
    elif x > 0:
        direction = 1
    elif y < 0:
        direction = 2
    elif y > 0:
        direction = 0
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
def print_map(map, w, h):
    for row in map:
        print(str(row))
        #print('\n')


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))