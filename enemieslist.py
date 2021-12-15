import random
from enemies import Enemies
import pyxel


class EnemiesList:
    def __init__(self):
        self.enemies_list = []
        self.enemies_list.append()
        if (random.random() * self.elapsed_time % 15) == 1:
            self.enemies_list.append(Enemies(200, 232, random.random()))

    def update(self):
        for k in self.enemies_list:
            if k.x < 50 or k.x > 200:
                self.enemies_list.remove(k)
