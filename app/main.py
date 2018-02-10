import bottle
import os
import time
from ai import test_ai
from map_builder import build_map
from map_builder import print_map


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


@bottle.post('/move')
def move():
    global test_direction
    data = bottle.request.json

    # build current map using game data
    start_time = time.time()
    map = build_map(data)

    # run ai to get next direction
    directions = ['up', 'left', 'down', 'right']
    test_direction = test_ai(test_direction, data)

    # print data for debugging
    print_map(map, data['width'], data['height'])
    print(directions[test_direction])
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