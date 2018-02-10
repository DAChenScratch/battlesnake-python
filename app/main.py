import bottle
import os
import time
from ai import test_ai
from map_builder import build_map
from map_builder import print_map
from map_builder import display_map


test_direction = 0


@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.post('/start')
def start():
    data = bottle.request.json
    game_id = data['game_id']
    board_width = data['width']
    board_height = data['height']

    head_url = '%s://%s/static/head.png' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )

    # TODO: Do things with data

    return {
        'color': '#99ccff',
        'secondary_color': '#99ddff',
        'taunt': 'Im Baffled.',
        'head_url': head_url,
        'name': 'BaffleSnek'
    }


@bottle.post('/move')
def move():
    global test_direction
    data = bottle.request.json
    start_time = time.time()
    # build current map using game data
    map = build_map(data)

    directions = ['up', 'left', 'down', 'right']
    test_direction = test_ai(test_direction, data)

    print(directions[test_direction])
    print_map(map, data['width'], data['height'])
    #display_map(map)
    end_time = time.time()
    print('Time for move was ' + str((end_time - start_time) * 1000) + 'ms')
    return {
        'move': directions[test_direction],
        'taunt': 'battlesnake-python!'
    }


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))