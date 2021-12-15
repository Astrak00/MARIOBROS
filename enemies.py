import random


class Enemies:
    def __init__(self, x: int, y: int, family: float):
        self.x = x
        self.y = y
        self.type = family
        if self.type > 0.75:
            # Sprite of the KoopaTroopa
            self.sprite = (0, 64, 16, 16, 24, 12)
        else:
            # Sprite of the goomba
            self.sprite = (0, 32, 48, 16, 16, 12)

        # Goomba tiles
        self.enemy_tiles = [(4, 6), (5, 6), (4, 7), (5, 7)]
        self.all_enemy_tiles = [(4, 6), (5, 6), (4, 7), (5, 7), (9, 2), (8, 3), (9, 3), (9, 4),
                                (9, 5), (8, 6), (9, 6), (8, 7), (9, 7), (8, 8), (9, 8), (8, 9), (9, 9)]

        # List of tiles:
        # (9, 2), (8, 3), (9, 3), (9, 4), (9, 5) --> KoopaTroopa
        # (8, 6), (9, 6), (8, 7), (9, 7) --> beatle enemy facing right
        # (8, 8), (9, 8), (8, 9), (9, 9) --> beatle enemy facing left

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, x: int):
        if type(x) == int:
            self.__x = x
        else:
            raise TypeError("X type is not valid, must be int")

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, y: int):
        if type(y) == int:
            self.__y = y
        else:
            raise TypeError("Y type is not valid, must be int")

    def move_left(self):
        self.x -= 1
