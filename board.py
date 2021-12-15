import random
import pyxel

from mario import Mario
from blocks import Blocks
from coins import Coin
from bricks import Bricks
from enemies import Enemies
from mushrooms import Mushroom


class Board:
    def __init__(self, x: int, y: int, fps: int, time: int):
        self.enemies_list = []
        self.remaining_time = 0
        self.elapsed_time = 0
        self.fps = fps
        self.time = time
        self.enemy = Enemies(0, 0, 0)
        self.mushroom = Mushroom(0, 0)
        self.aux = 0
        # Debugging bricks
        # self.bricks_list = [Bricks(11*8, 24*8), Bricks(14*8, 25*8)]
        self.cooldown = 0
        # It has to be taken into account that the y coordinate origin, the 0 is at the top of the screen and the 0 of
        # the x axis is also at the left, that is why, when going down, the y value increases
        pyxel.init(x, y, title='EDU New Super Mario Bros', fps=fps)
        pyxel.load("assets/marioassets.pyxres")
        pyxel.image(0).rect(48, 112, 16, 16, 12)
        self.scroll_border = 80
        self.player = Mario(20, 10)
        self.blocks = Blocks()
        self.coins_list = [Coin(11 * 8, 16 * 8), Coin(14 * 8, 15 * 8)]
        for i in range(random.randint(0, 50)):
            self.coins_list.append(Coin(random.randint(10, 2000), random.randint(15, 24) * 8))
        for i in range(random.randint(0, 20)):
            self.enemies_list.append(Enemies(random.randint(10, 2000), 232, random.random()))
        self.enemies_list.append(Enemies(258, 232, 0.5))
        self.enemies_list.append(Enemies(608, 232, 0.5))
        self.enemies_list.append(Enemies(932, 232, 0.5))

        pyxel.run(self.update, self.draw)
        self.x = x
        self.y = y

    # Gets the tile from a specific coordinate from the tile map
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

    def react_with_mushroom_collision(self, x, y, deltax):
        abs_deltax = abs(deltax)
        sign = 1 if deltax > 0 else -1
        for i in range(abs_deltax):
            if self.mushroom_collision(x + sign, y):
                if self.cooldown <= 0:
                    if not self.player.big:
                        self.player.grow_with_mushroom()
                        self.cooldown = 2
                    else:
                        self.player.score += 200

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
            # This is the text that represents the remaining time
            pyxel.text(230, 4, str(self.remaining_time), 0)
            # This prints the number of coins in the game and the next blt draws the logo of a small coin
            pyxel.text(100, 4, str(self.player.coins) + " coins", 0)
            pyxel.blt(95, 4, 0, 11, 232, 4, 6, 12)
            # This prints the score of mario
            pyxel.text(140, 4, 'Score: ' + str(self.player.score), 0)
            # These two print the x and y coordinates of mario, used in debug but ended being usefully
            pyxel.text(1, 1, 'X coordinate: ' + str(self.player.x), 0)
            pyxel.text(1, 11, 'Y coordinate: ' + str(self.player.y), 0)
            # These print the number of lives remaining and the small heart sprite
            pyxel.text(190, 4, 'Lives: ' + str(self.player.lives), 0)
            pyxel.blt(180, 4, 0, 17, 232, 7, 8, 12)
            for i in self.coins_list:
                i.draw(i.x - self.player.scroll_x, i.y)
            self.aux = self.player.score + 50*self.remaining_time
            pyxel.text(100, 15, "Final score: " + str(self.player.score + 75*self.remaining_time), 0)

            # Part of the debug of colision and acting on brick blocks
            """for j in self.bricks_list:
                j.draw(j.x - self.player.scroll_x, j.y)"""

            # Prints the player
            self.player.draw()

            # We have to draw each block, each coin and each mushroom:
            for i in self.player.question_block_list:
                pyxel.blt(i.x - self.player.scroll_x, i.y, *i.sprite)

            # This function print the coins on the screen
            for i in self.player.coins_list:
                pyxel.blt(i.x - self.player.scroll_x, i.y, *i.sprite)

            for k in self.enemies_list:
                pyxel.blt(k.x - self.player.scroll_x, k.y, *k.sprite)

            # This prints all the mushrooms on the screen
            for j in self.player.mushroom_list:
                pyxel.blt(j.x - self.player.scroll_x, j.y, *j.sprite)

            # This calls the function kikblock, that makes the block break, disappear, removing the object from the list
            self.player.kikblock(self.player.x, self.player.y)

            # This function would ake mario collide with the brick blocks, the question blocks and the already
            # hit question blocks
            self.player.collisions_with_blocks()

            # This function checks the position of the mushrooms and if mario is not big, it will increase mario's size
            self.player.grow_with_mushroom()

            # This function checks the position of mario and checks if it is the same as the coins and remove then
            # while adding them up to the counter of coins the player has.
            self.player.pick_coin(self.player.x, self.player.y)

        # If mario is at the end of the map, a congratulations message is shown:    
        elif self.player.x > 2000:
            pyxel.cls(0)
            pyxel.text(255 // 3, 255 // 2, "You win, congratulations <3 \n :D ", 7)
            self.aux = self.player.score + 75 * self.remaining_time
            pyxel.text(255 // 3, 255 // 3, "Your score was: " + str(self.aux), 7)
            self.aux = 0
        # If nothing of the above is satisfied, it means that mario is dead and has no more lives
        else:
            pyxel.cls(0)
            pyxel.text(255 // 2.5, 255 // 2, "Game over :(", 7)

    # When mario hits the flag pole, he grows, acting as a checkpoint
    def mario_grows(self):
        if 380 < self.player.x > 400 and 216 > self.player.y < 150:
            self.player.big = True

    # All of this medthod is executed every time a new frame is going to be displayed
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

        # if pyxel.btn(god mode) ###############################################################################3
        if pyxel.btn(pyxel.KEY_G) and pyxel.btn(pyxel.KEY_M):
            self.player.lives = 99999
            self.player.big = True

        # Gravity, that moves mario down a maximum of 3 and a minimum of 1 pixel
        self.player.deltay = min(self.player.deltay + 1, 3)

        # This is the part that makes mario big if he encounters the flag
        """if self.player.x > 100:
            self.player.big = True"""

        # This function would ake mario collide with the brick blocks, the question blocks and the already
        # hit question blocks
        self.player.collisions_with_blocks()

        # This function checks the position of the mushrooms and if mario is not big, it will increase mario's size
        self.player.grow_with_mushroom()

        # When Mario touches a coin, the score and the coin counter will increase and the coin will be removed:

        # Collision of coins
        for i in self.coins_list:
            if abs(self.player.x - i.x) < 15 and abs(self.player.y - i.y) < 15:
                self.player.coins += 1
                self.coins_list.remove(i)
                self.player.score += 200

                # Collision of bricks and actuating on the different blocks:

                """if abs(self.player.y - k.y) < 3:
                    self.coins_list.append(Coin(k.x, k.y+16))
                    self.player.question_block_list.remove(k)"""

        # This is the update that is inside the player
        self.player.update()

        # Used to debug and be a ble to jump freely on the map to test the different collisions and speeds, because
        # it is always executed, this code will be commented on the final program, as we only want it to jump when in
        # contact with the floor or a block
        if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.KEY_W):
            self.player.deltay = -12

        # This is the correct method that is used for the player to add to the que the jump when the W or the
        # upwards arrow is pressed
        if pyxel.btnp(pyxel.KEY_W) or pyxel.btnp(pyxel.KEY_UP):
            for l in self.blocks.pfp_list:
                if self.player.x + 16 == l.x and self.player.y + 16 == l.x:
                    self.player.deltay = -12
            """for k in self.blocks.floor_list:
                # If mario is on top of a block
                if self.player.y + 16 == k.x:
                    self.player.deltay = -12
            for c in self.blocks.pipes_list:
                # Checking that mario is on top of a pipe so the player can jump
                if self.player.x + 16 == c.x and self.player.y + 16 == c.x:
                    self.player.deltay = -12"""

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

        for i in self.player.coins_list:
            pyxel.blt(i.x - self.player.scroll_x, i.y, *i.sprite)

        for i in self.player.mushroom_list:
            pyxel.blt(i.x, i.y, *i.sprite)

        # We have to check in each frame if Mario is colliding with any block, if he is kicking any block or if he
        # is picking any mushroom or coin:
        self.player.kikblock(self.player.x, self.player.y)
        self.player.grow_with_mushroom()
        self.player.pick_coin(self.player.x, self.player.y)

        # Generating the enemies:
        # if (random.random() * self.elapsed_time % 15) == 1:

        # Update of enemies:
        for k in self.enemies_list:
            if k.x < 50 or k.x > 200:
                self.enemies_list.remove(k)
            k.move_left()

        if len(self.enemies_list) > 4:
            self.aux = 0
            self.aux = self.enemies_list[0]
            self.enemies_list.remove(self.aux)

        for g in self.enemies_list:
            if not self.player.big:
                if g.x == self.player.x and abs(g.y - self.y ) < 3:
                    self.game_ends()
            else:
                if g.x == self.player.x and abs(g.y - self.y +16 ) < 3:
                    self.player.decrease_with_enemy()
            self.enemies_list.remove(g)


