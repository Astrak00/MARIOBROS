class Enemy3:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rest_time = 0
        self.alive = True


class Enemy3Bullet:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.alive = True

