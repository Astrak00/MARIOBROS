import pyxel
from blocks import Blocks
from coins import Coin
from mushrooms import Mushroom


class Mario:
    def __init__(self, x, y):
        blocks = Blocks()
        self.pfp_list = blocks.pfp_list
        self.col_tiles = blocks.col_tiles
        self.underworld_col_tiles = blocks.underworld_col_tiles
        self.x = x
        self.y = y
        # direction of mario in the x-axis and how much pyxels the player wants to move in that direction
        self.deltax = 0
        # direction of mario in the y-axis and how much pyxels the player wants to move in that direction
        self.deltay = 0
        # image bank, position x in image bank, position y in image bank, width, height, color of the background
        self.sprite = (0, 0, 48, 13, 16, 12)
        self.coins = 0
        self.score = 0
        self.lives = 3
        self.scroll_x = 0
        self.width = 13
        self.height = 16
        self.big = False
        self.blocks = Blocks
        self.coin_list = []
        self.mushroom_list = []
        self.cooldown = 0
        self.available = True
        self.character = 'mario'

    # We have to update the size of Mario, the presence of mushrooms and coins and check if Mario is colliding
    # with blocks:
    def update(self):
        if pyxel.btn(pyxel.KEY_M):
            self.character = 'mario'
        elif pyxel.btn(pyxel.KEY_L):
            self.character = 'luigi'
        elif pyxel.btn(pyxel.KEY_O):
            self.character = 'wario'

        if self.big:
            self.width = 16
            self.height = 32
        if not self.big:
            self.width = 13
            self.height = 16


    def draw(self):
        if self.character == 'mario':
            if not self.big:
                if self.deltax < 0:
                    # Small mario facing left
                    pyxel.blt(self.x - self.scroll_x, self.y, 0, 0, 48, -13, 16, 12)
                else:
                    # Small mario facing right
                    pyxel.blt(self.x - self.scroll_x, self.y, 0, 0, 48, 13, 16, 12)
            else:
                if self.deltax < 0:
                    # Big mario facing left
                    pyxel.blt(self.x - self.scroll_x, self.y, 0, 0, 72, -16, 32, 12)
                else:
                    # Big mario facing right
                    pyxel.blt(self.x - self.scroll_x, self.y, 0, 0, 72, 16, 32, 12)
        elif self.character == 'luigi':
            if not self.big:
                if self.deltax < 0:
                    # Small luigi facing left
                    pyxel.blt(self.x - self.scroll_x, self.y, 0, 64, 80, -16, 16, 12)
                else:
                    # Small luigi facing right
                    pyxel.blt(self.x - self.scroll_x, self.y, 0, 64, 80, 16, 16, 12)
            else:
                if self.deltax < 0:
                    # Big luigi facing left
                    pyxel.blt(self.x - self.scroll_x, self.y, 0, 80, 80, -16, 32, 12)
                else:
                    # Big luigi facing right
                    pyxel.blt(self.x - self.scroll_x, self.y, 0, 80, 80, 16, 32, 12)
        elif self.character == 'wario':
            if not self.big:
                if self.deltax < 0:
                    # Small wario facing left
                    pyxel.blt(self.x - self.scroll_x, self.y, 0, 64, 96, -16, 16, 12)
                else:
                    # Small wario facing right
                    pyxel.blt(self.x - self.scroll_x, self.y, 0, 64, 96, 16, 16, 12)
            else:
                if self.deltax < 0:
                    # Big wario facing left
                    pyxel.blt(self.x - self.scroll_x, self.y, 0, 96, 80, -16, 32, 12)
                else:
                    # Big wario facing right
                    pyxel.blt(self.x - self.scroll_x, self.y, 0, 96, 80, 16, 32, 12)


    def draw_mushroom(self):
        self.drawmushroom = True
        return self.drawmushroom

    def draw_coin(self):
        self.drawcoin = True
        return self.drawcoin

    def kikblock(self):
        for i in self.question_block_list:
            if self.big:
                if (self.x - i.x) < 10 and self.y - 16 == \
                        i.x and i.container == "nothing":
                    self.question_block_list.remove(i)

            if (self.x - i.x) < 10 and self.y - 16 == i.x:
                if i.container == "coin":
                    i.sprite = (16, 16)
                    coin1 = Coin(i.x, i.y - 16)
                    self.coin_list.append(coin1)

            if (self.x - i.x) < 10 and self.y - 16 == i.x:
                if i.container == "mushroom":
                    i = (16, 16)
                    mushroom1 = Mushroom(i.x, i.y - 16)
                    self.mushroom_list.append(mushroom1)

    """def grow_with_mushroom(self):
        for i in self.mushroom_list:
            if (self.x - i.x) < 10 and self.y == i.y:
                self.y -= 16
                self.big = True
                self.sprite = (0, 72, 48, 13, 16, 12)
                self.y -= 16
                self.score += 200
                return True"""
    # Mario will grow when touching a mushroom, the score will increase and the mushroom will be removed:
    def grow_with_mushroom(self):
        self.big = True
        self.sprite = (0, 72, 48, 13, 16, 12)
        self.score += 200
        self.cooldown = 2
        return True

    def decrease_with_enemy(self):
        if self.big == True:
            self.big = False
            self.sprite = (0, 0, 48, 13, 16, 12)
        else:
            return False

    # When Mario touches a coin, the score and the coin counter will increase and the coin will be removed:
    def pick_coin(self):
        for i in self.coin_list:
            if (self.x - i.x) < 10 and self.y == i.y:
                self.coins += 1
                self.coin_list.remove(i)
                self.score += 200