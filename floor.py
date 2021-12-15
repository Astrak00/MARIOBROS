class Floor:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        # The sprite on the image bank 0, position x on 32, y position of 112, and the x and y dimension (width and
        # height)
        self.sprite = (0, 32, 112, 16, 16)

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

    @property
    def sprite(self):
        return self.__sprite

    @sprite.setter
    def sprite(self, sprite: tuple):
        if type(sprite) == tuple:
            self.__sprite = sprite
        else:
            raise TypeError("sprite type is not valid, must be a tuple")