# !/usr/bin/env python
# -*- coding: utf-8 -*-
import random

import pyxel

from characters import Monkey, Player

S_T_M = 8
HEIGHT = 128
WIDTH = 256
SEED = 2340923


class Scene:
    def __init__(self, x, y, tm, u, v, w, h, game):
        self.x = x
        self.y = y
        self.tm = tm
        # TODO: this are info relative to the tilemap, define them inside
        self.u = u
        self.v = v
        self.w = w
        self.h = h
        self.game = game

    def update(self):
        pass

    def draw(self):
        pyxel.bltm(self.x, self.y, self.tm, self.u, self.v, self.w, self.h)


class GeneratedLevel(Scene):
    def __init__(self, x, y, tm, u, v, w, h, game):
        self.generate_skyline()
        super().__init__(x, y, tm, u, v, w, h, game)

    def draw(self):
        for x, building_height in enumerate(self.skyline):
            pyxel.blt(x * 16, HEIGHT - 8, 0, 0, 24, 16, 8)  # draw ground
            for height in range(0, building_height, 8):  # build palace
                y = HEIGHT - 8 - 8 - height
                pyxel.blt(x * 16, y, 0, 0, 16, 16, 8)

    def update(self):
        if pyxel.btn(pyxel.KEY_0):
            pyxel.cls(0)
            self.generate_skyline()
        super().update()

    def generate_skyline(self) -> list[int]:
        # pyxel.nseed(SEED)
        self.skyline = [
            int((HEIGHT - 16) * pyxel.noise(random.random(), random.random()))
            for x in range(16)
        ]


class CityScene(Scene):
    def __init__(self, x, y, tm, u, v, w, h, game):
        super().__init__(x, y, tm, u, v, w, h, game)
        player = Player(x + 1 * S_T_M, y + 6 * S_T_M, tm, game.enemies)
        enemy = Monkey(x + 13 * S_T_M, y + 8 * S_T_M, tm, game.players)
        game.players.append(player)
        game.enemies.append(enemy)

    def update(self):
        super().update()

    def draw(self):
        super().draw()


SCENES = [CityScene, GeneratedLevel]
VICTORY_SCENE = Scene
GAME_OVER_SCENE = Scene
