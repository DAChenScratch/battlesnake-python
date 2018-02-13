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
game_id = 0
board_width = 0
board_height = 0

# a* variables



@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


# respond on /start
@bottle.post('/start')
def start():
    global game_id, board_width, board_height
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
    global direction, directions, board_height, board_width, game_id
    data = bottle.request.json
    # build current map using game data
    start_time = time.time()
    map = build_map(data)
    # run ai to get next direction
    direction = kill_time(direction, data)
    #astar(data)
    # print data for debugging
    if debug:
        #print_map(map)
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
    global board_height, board_width
    if debug:
        print('Killing time..')
        close_food = closest_food(data)
        grid = build_astar_grid(board_width, board_height)
        print('closest food: ' + str(close_food))
        print('neighbors of food: ')
        for neighbor in grid[close_food[0]][close_food[1]].neighbors:
            print(neighbor)
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


# astar search
# def astar(data, map, destination):
#     #destination = get_coords(destination)
#     search_scores = build_astar_grid(data['width'], data['height'])
#     open_set = set()
#     closed_set = set()
#     # set start location to current head location
#     start = current_location(data)
#     open_set.add(start)
#     # while openset is NOT empty keep searching
#     while open_set:
#         lowest_cell = [9999, 9999] # x, y
#         lowest_f = 9999
#         # find cell with lowest f score
#         for cell in open_set:
#             if search_scores[cell[0]][cell[1]].f < lowest_f:
#                 lowest_f = search_scores[cell[0]][cell[1]].f
#                 lowest_cell = cell
#         # found path to destination
#         if lowest_cell == destination:
#             something = 0
#             # TODO figure out what to return, probably a direction
#             return something
#         # else continue searching
#         current_cell = lowest_cell
#         # update sets
#         open_set.remove(lowest_cell)
#         closed_set.add(current_cell)
#         # check every viable neighbor to current cell
#         assess_neighbors(current_cell)


# return grid of empty Cells for astar search data
def build_astar_grid(w, h):
    grid = [ [Cell(row, col) for col in range(h)] for row in range(w)]
    return grid


# the cell class for storing a* search information
class Cell:
    global board_height, board_width
    def __init__(self, x, y):
        self.f = 0
        self.g = 0
        self.h = 0
        self.x = x
        self.y = y
        self.neighbors = []
        self.previous = None
        if self.x < board_width - 1:
            self.neighbors.append([self.x + 1, self.y])
        if self.x > 0:
            self.neighbors.append([self.x - 1, self.y])
        if self.y < board_height - 1:
            self.neighbors.append([self.x, self.y + 1])
        if self.y > 0:
            self.neighbors.append([self.x, self.y - 1])


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))