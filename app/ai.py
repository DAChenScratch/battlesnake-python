def test_ai(direction, data):
    direction += 1
    if direction == body_direction(data):
        direction += 1
    if direction > 3:
        direction = 0
    return direction

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