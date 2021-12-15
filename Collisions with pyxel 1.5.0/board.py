import pyxel

from mario import Mario
from blocks import Blocks
from mushrooms import Mushroom
from sniper import Enemy3
from sniper import Enemy3Bullet
from enemies import Enemies


class Board:
    def __init__(self, x: int, y: int, fps: int, time: int):
        self.dumb_enemy_list = []
        self.remaining_time = 0
        self.elapsed_time = 0
        self.fps = fps
        self.time = time
        self.enemy = Enemies(0, 0, 0)
        self.mushroom = Mushroom(0, 0)
        self.cooldown = 0
        # It has to be taken into account that the y coordinate origin, the 0 is at the top of the screen and the 0 of
        # the x axis is also at the left, that is why, when going down, the y value increases
        pyxel.init(x, y, title='EDU New Super Mario Bros', fps=fps)
        pyxel.load("assets/marioassets.pyxres")
        self.scroll_border = 80
        self.player = Mario(20, 10)
        self.blocks = Blocks()

        pyxel.run(self.update, self.draw)
        self.x = x
        self.y = y
        self.enemy_list = []
        self.enemy_list.append(Enemies())


        self.enemy_bullet_list = []
        self.dumb_enemy_list = Enemies(200, 232, 0.4)

    def get_tilemap(self, x, y):
        return pyxel.tilemap(0).pget(x, y)

    # This function gets the coordinates of mario, and adds them to the width and height of the player, which then
    # checks, in the range, if mario is between two tile, which he always is, as the tiles are 8 by 8 and mario is
    # 13 pixels wide and 16 pixels tall when they are small and 16 by 32 when they are big and divides them by 8.
    # This then checks the tile where mario wants to go and if it is in the list of tiles mario has to collide with,
    # in this case self.player.col_tiles, (collidable tiles)
    def check_tilemap_collision(self, x, y):
        x1 = x // 8
        y1 = y // 8
        x2 = (x + self.player.width - 1) // 8
        y2 = (y + self.player.height - 1) // 8
        for i in range(y1, y2 + 1):
            for j in range(x1, x2 + 1):
                for k in range(len(self.player.col_tiles)):
                    if self.get_tilemap(j, i) == self.player.col_tiles[k]:
                        return True
        return False

    # This is the method that takes the position if mario and the diration is facing, to tell us if the player can
    # move to tht position. It takes 4 arguments, marios x and y position and the direction where mario wants to move.

    def react_on_collision(self, x, y, deltax, deltay):
        abs_deltax = abs(deltax)
        abs_deltay = abs(deltay)

        if abs_deltax > abs_deltay:
            sign = 1 if deltax > 0 else -1  # This is a normal if, made into a single line to occupy less space
            for i in range(abs_deltax):  # This gets all the numbers from 0 to where mario wants to move in the x-axis
                if not self.check_tilemap_collision(x + sign, y):  # And lastly, it checks that it can move
                    x += sign

        sign = 1 if deltay > 0 else -1
        for i in range(abs_deltay):
            if not self.check_tilemap_collision(x, y + sign):
                y += sign

        else:
            sign = 1 if deltay > 0 else -1
            for i in range(abs_deltay):
                if not self.check_tilemap_collision(x, y + sign):
                    y += sign

            sign = 1 if deltax > 0 else -1
            for i in range(abs_deltax):
                if not self.check_tilemap_collision(x + sign, y):
                    x += sign

        # This function then returns the x and y position mario will be on the next frame
        return x, y, deltax, deltay

    def enemy_collision(self, x, y):
        x1 = x // 8
        y1 = y // 8
        x2 = (x + self.player.width - 1) // 8
        y2 = (y + self.player.height - 1) // 8
        for i in range(y1, y2 + 1):
            for j in range(x1, x2 + 1):
                for k in self.enemy.all_enemy_tiles:
                    if self.get_tilemap(j, i) == k:
                        return True
        return False

    def react_on_collision_except_vertical(self, x, y, deltax):
        abs_deltax = abs(deltax)
        sign = 1 if deltax > 0 else -1
        for i in range(abs_deltax):
            if self.enemy_collision(x + sign, y):
                if self.cooldown <= 0:
                    if self.player.big:
                        self.player.decrease_with_enemy()
                        self.cooldown = 2
                    else:
                        self.game_ends()

    def mushroom_collision(self, x, y):
        x1 = x // 8
        y1 = y // 8
        x2 = (x + self.player.width - 1) // 8
        y2 = (y + self.player.height - 1) // 8
        for i in range(y1, y2 + 1):
            for j in range(x1, x2 + 1):
                for k in self.mushroom.tiles:
                    if self.get_tilemap(j, i) == k:
                        return True
        return False


    """def react_with_mushroom_collision(self, x, y, deltax):
        abs_deltax = abs(deltax)
        sign = 1 if deltax > 0 else -1
        for i in range(abs_deltax):
            if self.mushroom_collision(x + sign, y):
                if self.cooldown <= 0:
                    if not self.player.big:
                        self.player.grow_with_mushroom()
                        self.cooldown = 2
                    else:
                        self.player.score += 200"""

    def game_ends(self):
        self.player.scroll_x = 0
        self.player.x = 20
        self.player.y = 10
        self.player.deltax = 0
        self.player.deltay = 0
        self.player.lives -= 1
        self.player.big = False
        self.elapsed_time = 0

    # This is the method that prints the whole game
    def draw(self):
        # The first if condition makes it so the level is displayed if mario is playing, if he is alive and has
        # remaining lives, and it has not reached the castle
        if self.player.lives > 0 and self.player.x < 2000:
            # Clears the screen to a blue background
            pyxel.cls(12)
            # Print the map
            pyxel.bltm(-(self.player.scroll_x % 8), 0, 0, self.player.scroll_x // 8, 0, 40, 40)
            # Prints the player
            self.player.draw()

            pyxel.text(230, 4, str(self.remaining_time), 0)
            # This prints the number of coins in the game and the next blt draws the logo of a small coin
            pyxel.text(100, 4, str(self.player.coins) + " coins", 0)
            pyxel.blt(95, 4, 0, 11, 232, 4, 6, 12)
            # This prints the score of mario
            pyxel.text(100, 12, 'Score: ' + str(self.player.score), 0)
            # These two print the x and y coordinates of mario, used in debug but ended being usefully
            pyxel.text(1, 1, 'X coordinate: ' + str(self.player.x), 0)
            pyxel.text(1, 11, 'Y coordinate: ' + str(self.player.y), 0)
            # These print the number of lives remaining and the small heart sprite
            pyxel.text(190, 4, 'Lives: ' + str(self.player.lives), 0)
            pyxel.blt(180, 4, 0, 17, 232, 7, 8, 12)

            # Prints all the coins
            for i in self.player.coin_list:
                pyxel.blt(i.x , i.y, 0, 0, 232, 10, 16, 12)
            # Prints all the mushrooms
            for i in self.player.mushroom_list:
                pyxel.blt(i.x, i.y, *i.sprite)

            # Drawing the sniper (static enemy)
            """for i in self.enemy_list:
                pyxel.blt(i.x - self.player.scroll_x, i.y, 0, 3, 29, 8, 8, 12)"""

            # Drawing the enemies bullet:
            """for i in self.enemy_bullet_list:
                pyxel.blt(i.x - self.player.scroll_x, i.y, 0, 3, 30, 8, 8, 12)"""

        elif self.player.x > 2000:
            pyxel.cls(0)
            pyxel.text(255 // 3, 255 // 2, "You win, congratulations <3 \n :D ", 7)
            pyxel.text(255 // 3, 255 // 3, "Your score was: " + str(self.player.score + 75 * self.remaining_time), 7)
        else:
            pyxel.cls(0)
            pyxel.text(100, 255 // 2, "Game over :(", 7)

    def update(self):
        # If the q key or the shift key are pressed, the program will exit
        if pyxel.btn(pyxel.KEY_Q) or pyxel.btn(pyxel.KEY_SHIFT):
            pyxel.quit()

        # Mario's update moving left
        if pyxel.btn(pyxel.KEY_A) or pyxel.btn(pyxel.KEY_LEFT):
            self.player.deltax = -2

        if pyxel.btn(pyxel.KEY_E):
            self.player.y -= 2

        # Mario's update moving right
        if pyxel.btn(pyxel.KEY_D) or pyxel.btn(pyxel.KEY_RIGHT):
            self.player.deltax = 2

        # Activating God mode
        if pyxel.btn(pyxel.KEY_G) and pyxel.btn(pyxel.KEY_M):
            self.player.lives = 99999
            self.player.big = True

        # Gravity, that moves mario down a maximum of 3 and a minimum of 1 pixel
        self.player.deltay = min(self.player.deltay + 1, 3)

        if self.mushroom_collision(self.player.x, self.player.y):
            if self.player.grow_with_mushroom():
                if self.cooldown <= 0:
                    self.player.y -= 16
        # self.mushroom_collision(self.player.x, self.player.x)

        # This is the update that is inside the player
        self.player.update()

        # Used to debug and be a ble to jump freely on the map to test the different collisions and speeds, because
        # it is always executed, this code will be commented on the final program, as we only want it to jump when in
        # contact with the floor or a block
        """if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.KEY_W):
            self.player.deltay = -12"""

        # This is the correct method that is used for the player to add to the que the jump when the W or the
        # upwards arrow is pressed
        if pyxel.btnp(pyxel.KEY_W):
            for k in self.blocks.floor_list:
                if self.player.y + 16 == k.x:
                    self.player.deltay = -12
            for b in self.blocks.platform_list:
                if self.player.x + 16 == b.x and self.player.y + 16 == b.y:
                    self.player.deltay = -12
            for c in self.blocks.pipes_list:
                if self.player.x + 16 == c.x and self.player.y + 16 == c.x:
                    self.player.deltay = -12

        # This is the part that affect marios movement, which checks for the collisions and if the path is free,
        # moves the player
        self.player.x, self.player.y, self.player.deltax, self.player.deltay = \
            self.react_on_collision(self.player.x, self.player.y, self.player.deltax, self.player.deltay)

        if self.player.x < self.player.scroll_x:
            self.player.x = self.player.scroll_x

        # This prevents mario from escaping the screen from the top
        if self.player.y < 0:
            self.player.y = 0

        self.player.deltax = int(self.player.deltax * 0.8)

        if self.player.x > self.player.scroll_x + self.scroll_border:
            self.player.scroll_x = min(self.player.x - self.scroll_border, 248 * 8)

            # Mario's collision with enemies:
            self.react_on_collision_except_vertical(self.player.x, self.player.y, self.player.deltax)

        # Deaths and time:
        # self.remaining_time = 300 - pyxel.frame_count // 60
        self.remaining_time = self.time - self.elapsed_time
        if pyxel.frame_count % self.fps == 0:
            self.elapsed_time += 1

        # Adding a cooldown function
        if pyxel.frame_count % self.fps == 0:
            self.cooldown -= 1

        # If the player falls out of the map, though the floor gap, it will call the end function, that resets the game
        if self.remaining_time == 0 or self.player.y > 300:
            self.game_ends()

        # Sniper
        """for i in self.enemy_list:
            i.update(self.player.x, self.player.y)
            if i.rest_time > 0:
                i.rest_time -= 1

            if i.rest_time == 0:
                dx = self.player.x - i.x
                dy = self.player.y - i.y
                sq_dist = dx * dx + dy * dy

                if 60 * 60 > sq_dist > 0:
                    dist = math.sqrt(sq_dist)
                    self.enemy_bullet_list.append(Enemy3Bullet(self.x, self.y, dx / dist, dy / dist))
                    i.rest_time = 60"""

        # Updating the sniper's bullet:
        """for i in self.enemy_bullet_list:
            i.x += i.dx
            i.y += i.dy"""

        # Deleting snipers:
        """self.cleanup_list(self.enemy_list)
        self.cleanup_list(self.enemy_bullet_list)"""

        # Enemies:
        """for i in self.dumb_enemy_list:
            a = 1"""

        # Deaths and time

        if self.player.y > 300:
            self.game_ends()
