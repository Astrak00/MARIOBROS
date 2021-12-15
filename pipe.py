class Pipes:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

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
