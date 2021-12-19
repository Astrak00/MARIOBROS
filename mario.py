import pyxel
from blocks import Blocks
from coins import Coin
from mushrooms import Mushroom


class Mario:
    def __init__(self, x, y):
        blocks = Blocks()
        self.pfp_list = blocks.pfp_list
        self.col_tiles = blocks.col_tiles
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
        self.coins_list = []
        self.mushroom_list = []
        self.question_block_list = blocks.question_block_list
        self.character = 'mario'

    # We have to update the size of Mario, the presence of mushrooms and coins and check if Mario is colliding
    # with blocks:
    # Creatred by Eduardo Alarcón 100472175@alumnos.uc3m.es
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

        self.grow_with_mushroom()

        # self.pick_coin(self.x, self.y)
        self.kikblock(self.x, self.y)

        if self.x > 400:
            self.big = True

    # We have to draw Mario with its different directions and sizes:
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

    # With this function we check Mario is colliding with any block and what item that block contains so that
    # the program knows what to do depending on the type of the block:
    # Creatred by Eduardo Alarcón 100472175@alumnos.uc3m.es
    def kikblock(self, x: int, y: int):
        for i in self.question_block_list:
            # If Mario is big the breakable blocks are removed from the block list when kicked:
            if self.big:
                if abs(x - i.x) < 16 and abs(y - i.y) < 10 and i.container == "nothing":
                    self.question_block_list.remove(i)
                    self.coins_list.append(Coin(i.x, i.y + 16))
                    self.y += 8

            # When Mario kicks a question block a new object (coin or mushroom) is created and the sprite of the block
            # changes as well as its content:
            if abs(self.x - i.x) < 10 and abs(self.y - 16 - i.y) < 10:
                if i.container == "coin":
                    i.container = "empty"
                    coin1 = Coin(i.x, i.y - 16)
                    self.coins_list.append(Coin(x, y + 16))
                elif i.container == "mushroom":
                    i.container = 'empty'
                    i.sprite = (0, 16, 16, 16, 16)
                    mushroom1 = Mushroom(i.x, i.y - 16)
                    self.mushroom_list.append(mushroom1)



    # Mario will grow when touching a mushroom, the score will increase and the mushroom will be removed:
    def grow_with_mushroom(self):
        for i in self.mushroom_list:
            if (self.x - i.x) < 10 and (self.y - i.y) < 10:
                self.big = True
                self.sprite = (0, 72, 48, 13, 16, 12)
                self.y -= 16
                self.score += 200
                self.mushroom_list.remove(i)

    def decrease_with_enemy(self):
        if self.big == True:
            self.big = False
            self.sprite = (0, 0, 48, 13, 16, 12)
        else:
            return False

    # When Mario touches a coin, the score and the coin counter will increase and the coin will be removed:
    def pick_coin(self, x: int, y: int):
        for i in self.coins_list:
            if abs(x - i.x) < 10 and abs(y-i.y) < 10:
                self.coins += 1
                self.coins_list.remove(i)
                self.score += 200

    # If Mario is touching a block from bellow he will collides with it:
    def collisions_with_blocks(self):
        for i in self.question_block_list:
            if abs(self.x - i.x) < 8 and (i.y - self.y) < 6 and self.big:
                self.deltay = 0
            elif abs(self.x - i.x) < 8 and (i.y - self.y) < 24:
                self.deltay = 0


    """def collisions_with_blocks(self):
        for i in self.question_block_list:
            if abs(self.x - i.x) < 10 and (self.y - i.y) == 16 and self.deltay <= 0:  # para arriba
                self.deltay = 0
            elif abs(self.x - i.x) < 10 and (i.y - self.y) == 16 and self.deltay >= 0:  # para abajo
                self.deltay = 0
            elif (i.x - self.x - 16) < 1 and abs(self.y - i.y) < 10 and self.deltax >= 0:
                self.deltax = 0
            elif (self.x - i.x - 16) < 1 and abs(self.y - i.y) < 10 and self.deltax <= 0:
                self.deltax = 0"""
    # Creatred by Eduardo Alarcón 100472175@alumnos.uc3m.es

