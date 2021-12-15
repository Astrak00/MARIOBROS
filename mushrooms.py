class Mushroom:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        # The sprite on the image bank 0, position x on 0, y position of 32, and the x and y dimension
        # (width and height) and the colour you want to remove from the image, in this case, it is 12, which is the same
        # colour as the background
        self.sprite = (0, 0, 32, 16, 16, 12)
        self.tiles = [(0, 4), (1, 4), (0, 5), (1, 5)]

