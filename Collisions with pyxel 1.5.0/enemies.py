class Enemies:
    def __init__(self, x: int, y: int, type: float):
        self.x = x
        self.y = y
        self.type = type
        self.sprite = (0, 32, 48, 16, 16, 12)

        if self.type > 0.75:
            self.sprite = (0, 64, 16, 16, 24, 12)

        self.enemy_tiles = [(4, 6), (5, 6), (4, 7), (5, 7)]
        self.all_enemy_tiles = [(4, 6), (5, 6), (4, 7), (5, 7), (9, 2), (8, 3), (9, 3), (9, 4),
                                (9, 5), (8, 6), (9, 6), (8, 7), (9, 7), (8, 8), (9, 8), (8, 9), (9, 9)]

    def move_left(self):
        self.x -= 1