import pyxel


class Bricks:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.sprite = (0, 0, 16, 16, 16)

    def draw(self, x: int, y: int):
        pyxel.blt(x, y, *self.sprite)
