
class QuestionBlocks:
    def __init__(self, x: int, y: int, container="nothing"):
        self.x = x
        self.y = y
        self.container = container
        self.sprite = (0, 0, 16, 16, 16)  # Bricks
        if self.container == "coin" or self.container == "mushroom":
            self.sprite = (0, 16, 0, 16, 16)  # Question Block
        elif self.container == "empty":
            self.sprite = (0, 16, 16, 16, 16)
