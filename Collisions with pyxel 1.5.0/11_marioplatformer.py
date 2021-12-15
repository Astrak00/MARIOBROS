
import pyxel
import random

player_width = 13  # en mario
player_height = 16  # en mario
scroll_border = 80  # en board

# They have to be multiplied by 16 to get the correct coordinates on the editor
tile_space = (0, 0)  # en board
# The tile has to be divided into 4 different 8x8 tiles, with s-> superior, i -> inferior, l -> left and r -> right
tile_cobble_sl = (4, 14)
tile_cobble_sr = (5, 14)
tile_cobble_il = (4, 15)
tile_cobble_ir = (5, 15)
tile_cobble_list = ((4, 14), (5, 14), (4, 15), (5, 15))  # en unbreakable_blocks

tile_jukebox_sl = (2, 2)
tile_jukebox_sr = (3, 2)
tile_jukebox_il = (2, 3)
tile_jukebox_ir = (3, 3)
tile_jukebox_list = ((2, 2), (3, 2), (2, 3), (3, 3))  # en unbreakable_blocks

tile_question_sl = (2, 0)
tile_question_sr = (3, 0)
tile_question_il = (2, 1)
tile_question_ir = (3, 1)
tile_question_list = ((2, 0), (3, 0), (2, 1), (3, 1))

tile_lists_of_lists = [(4, 14), (5, 14), (4, 15), (5, 15), (2, 2), (3, 2), (2, 3), (3, 3), (2, 0), (3, 0), (2, 1),
                       (3, 1), (0, 2), (1, 2), (0, 3), (1, 3), (4, 0), (5, 0), (6, 0), (7, 0), (4, 1), (9, 1), (4, 2),
                       (7, 2)]

# Head -> upper part of pipe, s -> superior, l-> left, i -> inferior, r -> right,
# c -> center in x axis, m-> center in y axis
tile_pipe_head_sl = (4, 0)
tile_pipe_head_scl = (5, 0)
tile_pipe_head_scr = (6, 0)
tile_pipe_head_sr = (7, 0)
tile_pipe_head_il = (4, 1)
tile_pipe_head_ir = (9, 1)
tile_pipe_body_left = (4, 2)
tile_pipe_body_right = (7, 2)
tile_pipe_list = ((4, 0), (5, 0), (6, 0), (7, 0), (4, 1), (9, 1), (4, 2), (7, 2))

tile_bricks_sl = (0, 2)
tile_bricks_sr = (1, 2)
tile_bricks_il = (0, 3)
tile_bricks_ir = (1, 3)
tile_bricks_list = [(0, 2), (1, 2), (0, 3), (1, 3)]

tile_goomba = (2, 3)
tile_goomba_generate = (6, 14)

# This is the list of the floor of each block, we use it so mario does not fall off the screen, this allows mario to
# jump when only on this blocks.py,
floor_list_of_isa = []
for i in range(143 + 1):
    floor_list_of_isa.append((i * 8, 31 * 8))
    # We have to multiply everything by 8 because the data provided by Isa is from the tile map, which is made up of
    # 8x8 squares
for i in range(148, 225 + 1):
    floor_list_of_isa.append(((i + 148) * 8, 31 * 8))

platform_list_of_isa = [(29 * 8, 23 * 8), (30 * 8, 23 * 8), (44 * 8, 15 * 8), (45 * 8, 15 * 8), (202 * 8, 23 * 8),
                        (202 * 8, 23 * 8), (221 * 8, 15 * 8),
                        (222 * 8, 15 * 8), (221 * 8, 23 * 8), (222 * 8, 23 * 8), (227 * 8, 23 * 8), (228 * 8, 23 * 8),
                        (236 * 8, 29 * 8), (237 * 8, 29 * 8),
                        (238 * 8, 27 * 8), (239 * 8, 27 * 8), (240 * 8, 25 * 8), (241 * 8, 25 * 8), (90 * 8, 23 * 8),
                        (91 * 8, 23 * 8), (114*8, 23*8), (115*8, 23*8)]
for i in range(40, 48 + 1):
    platform_list_of_isa.append((i * 8, 23 * 8))
for i in range(160, 165 + 1):
    platform_list_of_isa.append((i * 8, 23 * 8))
for i in range(168, 187 + 1):
    platform_list_of_isa.append((i * 8, 15 * 8))
for i in range(196, 203 + 1):
    platform_list_of_isa.append((i * 8, 15 * 8))
for i in range(210, 213 + 1):
    platform_list_of_isa.append((i * 8, 23 * 8))


pipes_list_of_isa = []
for i in range(56, 59 + 1):
    pipes_list_of_isa.append((i * 8, 27*8))
for i in range(72, 75+1):
    pipes_list_of_isa.append((i*8, 23*8))
for i in range(96, 99+1):
    pipes_list_of_isa.append((i*8, 20*8))
for i in range(120, 123+1):
    pipes_list_of_isa.append((i*8, 20*8))


enemy_list = []
scroll_x = 0
player = None


def get_tilemap(x, y):
    """This function gives us the value of the tile, from the tile map that we drew on the tile editor, to be precise,
    this function allows us to modify the tilemap and with it, modify the collisions, but not the jump, as we
    implemented the jump using list of coordinates, that had to be multiplied by 8, as each tile in the tilemap
    is made up of 8 pixels"""
    return pyxel.tilemap(0).pget(x, y)


def check_tilemap_collision(x, y):
    """This function uses as parameters, the position of mario, x and y. It gets their position and the range
    where the sprite is, for example, as mario is 13 pixels wide, it checks from 0 to 12 and in the j direction, from 0 to 15 for
    any of the blocks.py that have to collide with, but we divide it by 8, to be a ble to handle it with the other elements"""
    x1 = x // 8
    y1 = y // 8

    # Getting where the sprite of mario ends, if, for example, it is between two blocks.py, it will not clip.
    x2 = (x + player_width - 1) // 8
    y2 = (y + player_height - 1) // 8

    # Getting the values between the two possible positions plus 1 to check for the next block and checking if it is
    # equal to any element of the list of collisionable tiles, called tile_lists_of_lists and if it does not, it will
    # return a False
    for i in range(y1, y2 + 1):
        for j in range(x1, x2 + 1):
            for k in range(len(tile_lists_of_lists)):
                if get_tilemap(j, i) == tile_lists_of_lists[k]:
                    return True
    return False


# This function uses the previous function to check if weather if where mario wants to go is free or if it

def react_on_collision(x, y, deltax, deltay):
    abs_deltax = abs(deltax)
    abs_deltay = abs(deltay)

    if abs_deltax > abs_deltay:
        sign = 1 if deltax > 0 else -1
        for i in range(abs_deltax):
            if not check_tilemap_collision(x + sign, y):
                x += sign

        sign = 1 if deltay > 0 else -1
        for i in range(abs_deltay):
            if not check_tilemap_collision(x, y + sign):
                y += sign

    else:
        sign = 1 if deltay > 0 else -1
        for i in range(abs_deltay):
            if not check_tilemap_collision(x, y + sign):
                y += sign

        sign = 1 if deltax > 0 else -1
        for i in range(abs_deltax):
            if not check_tilemap_collision(x + sign, y):
                x += sign

    return x, y, deltax, deltay


class Mario:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.deltax = 0
        self.deltay = 0
        self.sprite = (0, 0, 48, 13, 16, 12)
        self.coins = 69
        self.score = 0
        self.lives = 3

    def update(self):
        global scroll_x  # ------------------------------------------------------------------------------------------

        if pyxel.btn(pyxel.KEY_LEFT):
            self.deltax = -2

        if pyxel.btn(pyxel.KEY_RIGHT):
            self.deltax = 2

        self.deltay = min(self.deltay + 1, 3)

        if pyxel.btnp(pyxel.KEY_UP):
            for k in range(len(floor_list_of_isa)):
                if player.y + 16 == floor_list_of_isa[k][1]:
                    self.deltay = -12
            for b in range(len(platform_list_of_isa)):
                if player.y + 16 == platform_list_of_isa[b][1] or player.x + 16 == platform_list_of_isa[b][0]:
                    self.deltay = -12
            for c in pipes_list_of_isa:
                if player.x + 16 == c[0] or player.y + 16 == c[1]:
                    self.deltay = -12




        self.x, self.y, self.deltax, self.deltay = react_on_collision(self.x, self.y, self.deltax, self.deltay)

        if self.x < scroll_x:
            self.x = scroll_x

        if self.y < 0:
            self.y = 0

        self.deltax = int(self.deltax * 0.8)

        if self.x > scroll_x + scroll_border:
            scroll_x = min(self.x - scroll_border, 248 * 8)

        if self.y > 300:
            game_ends()

    def draw(self):
        pyxel.blt(self.x - scroll_x, self.y, *self.sprite)


class Goomba:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.deltax = 0
        self.deltay = 0
        self.direction = 1
        self.alive = True
        self.sprite = (0, 32, 48, 16, 16, 12)
        self.is_falling = True

    def update(self):
        self.deltax = self.direction
        self.deltay = min(self.deltay + 1, 3)

        self.x, self.y, self.deltax, self.deltay = \
            react_on_collision(self.x, self.y, self.deltax, self.deltay)

    def draw(self):
        pyxel.blt(self.x - scroll_x, self.y, *self.sprite)


def enemy_update(x, y, kind, is_alive):
    if is_alive and abs(x - player.x) < 10 and abs(y - player.y) < 12:
        is_alive = False
        player.score += 200
    return x, y, kind, is_alive


class App:
    def __init__(self, x: int, y: int, fps: int):
        pyxel.init(x, y, title='Mario Brosh', fps=fps)
        pyxel.load("assets/marioassets.pyxres")
        pyxel.image(0).rect(48, 112, 16, 16, 12)
        self.enemy = [(random.randint(8, 250), 200, random.randint(0, 2), True)]

        # This will resolve when importing classes
        global player
        player = Mario(20, 10)
        pyxel.run(self.update, self.draw)

    def update_enemy(x, y, kind, is_alive):
        if is_alive and abs(x - player.x) < 12 and abs(y - player.y) < 12:
            is_alive = False

    def update(self):
        player.update()

        if pyxel.btnp(pyxel.KEY_SHIFT):
            pyxel.quit()
        self.remaining_time = 300 - pyxel.frame_count // 60

        #        for i, v in enumerate(self.enemy):
        #            self.enemy[i] = self.update_enemy(*v)

        if self.remaining_time == 0:
            game_ends()

    def draw(self):
        pyxel.cls(0)
        pyxel.bltm(-(scroll_x % 8), 0, 0, scroll_x // 8, 0, 40, 40)
        player.draw()

        for enemy in enemy_list:
            enemy.draw()

        pyxel.text(230, 4, str(self.remaining_time), 0)
        pyxel.text(100, 4, str(player.coins) + " coins", 0)
        pyxel.blt(95, 4, 0, 11, 232, 4, 6, 12)
        pyxel.text(140, 4, 'Score: ' + str(player.score), 0)
        pyxel.text(1, 1, 'X coordinate: ' + str(player.x), 0)
        pyxel.text(1, 11, 'Y coordinate: ' + str(player.y), 0)
        pyxel.text(190, 4, 'Lives: ' + str(player.lives), 0)
        pyxel.blt(180, 4, 0, 17, 232, 7, 8, 12)



        for x, y, kind, is_alive in self.enemy:
            if is_alive:
                pyxel.blt(x, y, 0, 48, 32, 16, 24, 12)


def game_ends():
    global scroll_x

    scroll_x = 0
    player.x = 20
    player.y = 10
    player.deltax = 0
    player.deltay = 0
    player.lives -= 1
    if player.lives == 0:
        pyxel.cls(0)
        pyxel.text(255 // 2, 255 // 2, "Game over :(", 7)



App(255, 255, 60)