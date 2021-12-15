class QuestionBlocks:
    def __init__(self, x: int, y: int, container="nothing", kicked = False):
        self.x = x
        self.y = y
        self.container = container
        self.sprite = (16,0)
        skicked = kicked

        if container == "nothing":
            self.sprite = (0,16)


