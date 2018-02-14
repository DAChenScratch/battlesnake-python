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
mode = ['hungry', 'killing_time']
# general variables
game_id = 0
board_width = 0
board_height = 0

# my snake variables
direction = 0
health = 100
turn = 0
survival_min = 50


@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


# respond on /start
@bottle.post('/start')
def start():
    global game_id, board_width, board_height, survival_min
    data = bottle.request.json
    game_id = data['game_id']
    board_width = data['width']
    board_height = data['height']
    survival_min = max(board_height, board_width) * 2
    if survival_min > 90: survival_min = 90
    # get head pic url
    head_url = '%s://%s/static/snake_profile.png' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )
    return {
        'color': '#3b94e3', # blue
        'secondary_color': '#cc4ff1', # pink
        'taunt': 'So cool fam.',
        'head_url': head_url,
        'name': 'zero_cool'
    }


# respond on /move
@bottle.post('/move')
def move():
    global direction, directions, board_height, board_width, game_id, health, turn
    data = bottle.request.json
    start_time = time.time()
    health = data['you']['health']
    turn = data['turn']
    taunt = 'Super cool.'
    # run ai to get next direction
    if health < survival_min:
        print('HUNGRY! SEEKING FOOD.')
        taunt = 'Not cool.'
        direction = ai(data)
    else:
        print('COOL. KILLING TIME.')
        taunt = 'Super cool.'
        direction = kill_time(data)
    # print data for debugging
    if debug:
        print('REMAINING HEALTH IS ' + str(health) + ' ON TURN ' + str(turn) + '.')
        print('SENDING MOVE: ' + str(directions[direction]))
        end_time = time.time()
        print('Time for move was ' + str((end_time - start_time) * 1000) + 'ms')
    # return next move
    return {
        'move': directions[direction],
        'taunt': 'Not cool.'
    }


# do your thing
def ai(data):
    map = build_map(data)
    close_food = closest_food(data)
    return astar(data, map, close_food)



# follow own tail to kill time
def kill_time(data):
    map = build_map(data)
    tail = get_tail(data)
    return astar(data, map, tail)


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


# return coords to own tail
def get_tail(data):
    body = data['you']['body']['data']
    tail = current_location(data)
    for segment in body:
        tail = get_coords(segment)
    return tail


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

# return direction from a to b
def calculate_direction(a, b, map, data):
    x = a[0] - b[0]
    y = a[1] - b[1]
    direction = 0
    # directions = ['up', 'left', 'down', 'right']
    if x < 0:
        direction = 3
    elif x > 0:
        direction = 1
    elif y < 0:
        direction = 2
    count = 0
    while not valid_move(direction, map, data):
        if count == 3:
            print('DEAD END, NO VALID MOVE REMAINING!')
            print('GAME OVER')
            break
        count += 1
        direction += 1
        if direction == 4:
            direction = 0
    return direction


# check if move in direction will kill you
# return True if valid
# return False if it will kill you
def valid_move(d, map, data):
    global board_height, board_width
    current = current_location(data)
    if debug: print('CHECKING IF MOVE IS VALID!')
    # directions = ['up', 'left', 'down', 'right']
    # check up direction
    if d == 0:
        if current[1] - 1 < 0:
            if debug: print('up move is OFF THE MAP!')
            return False
        if map[current[0]][current[1] - 1] <= 1:
            if debug: print('up move is valid.')
            return True
        else:
            if debug: print('up move is FATAL!')
            return False
    #check left direction
    if d == 1:
        if current[0] - 1 < 0:
            if debug: print('right move is OFF THE MAP!')
            return False
        if map[current[0] - 1][current[1]] <= 1:
            if debug: print('left move is valid.')
            return True
        else:
            if debug: print('left move is FATAL!')
            return False
    # check down direction
    if d == 2:
        if current[1] + 1 > board_height - 1:
            if debug: print('down move is OFF THE MAP!')
            return False
        if map[current[0]][current[1] + 1] <= 1:
            if debug: print('down move is valid.')
            return True
        else:
            if debug: print('down move is FATAL!')
            return False
    # check right direction
    if d == 3:
        if current[0] + 1 > board_width - 1:
            if debug: print('right move is OFF THE MAP!')
            return False
        if map[current[0] + 1][current[1]] <= 1:
            if debug: print('right move is valid.')
            return True
        else:
            if debug: print('right move is FATAL!')
            return False
    # failsafe
    if d > 3: print('valid_move FAILED! direction IS NOT ONE OF FOUR POSSIBLE MOVES!')
    return True


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
def astar(data, map, destination):
    global debug
    #if debug: print('destination for search: ' + str(destination))
    #destination = get_coords(destination)
    search_scores = build_astar_grid(data['width'], data['height'])
    open_set = []
    closed_set = []
    # set start location to current head location
    start = current_location(data)
    #if debug: print('Current location for search: ' + str(start))
    open_set.append(start)
    #if debug: print('Current location for search in open_set: ' + str(open_set))
    # while openset is NOT empty keep searching
    while open_set:
        #if debug: print('Got here!')
        lowest_cell = [9999, 9999] # x, y
        lowest_f = 9999
        # find cell with lowest f score
        for cell in open_set:
            #if debug: print('cell f: ' + str(search_scores[cell[0]][cell[1]].f))
            if search_scores[cell[0]][cell[1]].f < lowest_f:
                lowest_f = search_scores[cell[0]][cell[1]].f
                lowest_cell = cell
        # found path to destination
        if lowest_cell[0] == destination[0] and lowest_cell[1] == destination[1]:
            if debug: print('FOUND A PATH! CALCULATING NEXT MOVE...')
            # retrace path back to origin to find optimal next move
            temp = lowest_cell
            while search_scores[temp[0]][temp[1]].previous[0] != start[0] and search_scores[temp[0]][temp[1]].previous[1] != start[1]:
                #if debug:
                    #print('Step back from ' + str(temp))
                    #print('to ' + str(search_scores[temp[0]][temp[1]].previous))
                    #print('ending at ' + str(start))
                temp = search_scores[temp[0]][temp[1]].previous
            # get direction of next optimal move
            next_move = calculate_direction(start, temp, map, data)
            return next_move
        # else continue searching
        current = lowest_cell
        current_cell = search_scores[current[0]][current[1]]
        # update sets
        open_set.remove(lowest_cell)
        closed_set.append(current)
        # check every viable neighbor to current cell
        for neighbor in search_scores[current[0]][current[1]].neighbors:
            neighbor_cell = search_scores[neighbor[0]][neighbor[1]]
            # check if neighbor has already been evaluated
            if neighbor not in closed_set:
                temp_g = current_cell.g + 1
                shorter = True
                # check if already evaluated with lower g score
                if neighbor in open_set:
                    if temp_g > neighbor_cell.g:
                        shorter = False
                # if not in either set, add to open set
                else:
                    neighbor
                    open_set.append(neighbor)
                # this is the current best path, record it
                if shorter:
                    neighbor_cell.g = temp_g
                    neighbor_cell.h = get_distance(neighbor, destination)
                    neighbor_cell.f = neighbor_cell.g + neighbor_cell.h
                    neighbor_cell.previous = current
                    #if debug: print('added ' + str(current) + ' as previous to ' + str(neighbor))
    # if reach this point and open set is empty, no path
    if not open_set:
        if debug: print('COULD NOT FIND PATH!')
        return 0



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