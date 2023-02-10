# !/usr/bin/env python
# -*- coding: utf-8 -*-
import math
import random

import pyxel

from characters import Character, Monkey, Player
from constants import HEIGHT, SPRITE_DIM, WIDTH


def height_to_y(h: int, delta=0) -> int:
    return HEIGHT - 8 - delta - h


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
        super().__init__(x, y, tm, u, v, w, h, game)
        self.skyline = []
        self._regenerate_skyline()
        player = Player(0 + SPRITE_DIM, 16, tm, game.enemies)
        enemy = Monkey(16 + SPRITE_DIM, 16, tm, game.players)
        self._place_characters([player, enemy])
        game.players.append(player)
        game.enemies.append(enemy)

    def draw(self):
        pyxel.cls(1)
        for x, building_height in enumerate(self.skyline):
            pyxel.blt(x * SPRITE_DIM * 2, HEIGHT - 8, 0, 0, 24, 16, 8)  # draw ground
            for height in range(0, building_height, 8):  # build palace
                y = height_to_y(height, SPRITE_DIM)
                pyxel.blt(x * SPRITE_DIM * 2, y, 0, 0, 16, 16, 8)

    def update(self):
        super().update()
        if pyxel.btn(pyxel.KEY_0):
            self._regenerate_skyline()
            self._place_characters(self.game.players + self.game.enemies)

    def _place_characters(self, characters: list[Character]):
        """
        Place characters from the borders inward on the highest of three buildings
        """
        sk, reverse_sk = self.skyline[:], self.skyline[::-1]
        for i, c in enumerate(characters):
            if i % 2:  # from the right
                tris = reverse_sk[(i - 1) * 3 : i * 3]
                max_height = max(tris)
                c.y = height_to_y(max_height, SPRITE_DIM * 2)
                c.x = (len(self.skyline) - tris.index(max_height) - 1) * 16
            else:  # from the left
                tris = sk[i * 3 : (i + 1) * 3]
                max_height = max(tris)
                c.y = height_to_y(max_height, SPRITE_DIM * 2)
                c.x = tris.index(max_height) * 16

    def _regenerate_skyline(self) -> list[int]:
        # pyxel.nseed(SEED)
        buildings_counter = int(WIDTH / (SPRITE_DIM * 2))
        self.skyline.clear()

        for _ in range(buildings_counter):
            h = int(
                (HEIGHT - SPRITE_DIM * 2)
                * pyxel.noise(random.random(), random.random())
            )
            self.skyline.append(math.ceil(h / 8) * 8)


class CityScene(Scene):
    def __init__(self, x, y, tm, u, v, w, h, game):
        super().__init__(x, y, tm, u, v, w, h, game)
        player = Player(x + 1 * SPRITE_DIM, y + 6 * SPRITE_DIM, tm, game.enemies)
        enemy = Monkey(x + 13 * SPRITE_DIM, y + 8 * SPRITE_DIM, tm, game.players)
        game.players.append(player)
        game.enemies.append(enemy)

    def update(self):
        super().update()

    def draw(self):
        super().draw()


SCENES = [CityScene, GeneratedLevel]
VICTORY_SCENE = Scene
GAME_OVER_SCENE = Scene
