def test_ai(direction):
    direction += 1
    if direction > 3:
        direction = 0
    return direction