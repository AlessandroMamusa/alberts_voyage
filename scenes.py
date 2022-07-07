# !/usr/bin/env python
# -*- coding: utf-8 -*-
import pyxel

from characters import Monkey, Player

S_T_M = 8


class Scene:
    def __init__(self, x, y, tm, u, v, w, h):
        self.x = x
        self.y = y
        self.tm = tm
        # TODO: this are info relative to the tilemap, define them inside
        self.u = u
        self.v = v
        self.w = w
        self.h = h

    def update(self):
        pass

    def draw(self):
        pyxel.bltm(self.x, self.y, self.tm, self.u, self.v, self.w, self.h)


class CityScene(Scene):
    def __init__(self, x, y, tm, u, v, w, h):
        super().__init__(x, y, tm, u, v, w, h)
        self.characters = []
        self.enemies = []
        player = Player(x + 1 * S_T_M, y + 6 * S_T_M, tm)
        enemy = Monkey(x + 13 * S_T_M, y + 8 * S_T_M, tm)
        self.characters.append(player)
        self.enemies.append(enemy)

    def update(self):
        for c in self.characters:
            c.update()
            if not c.p._is_shoot:
                continue
            for enemy in self.enemies:
                if (
                    enemy.x + enemy.w > c.p.x
                    and c.p.x > enemy.x
                    and enemy.y + enemy.h > c.p.y
                    and c.p.y > enemy.y
                ):
                    c.p._has_hit = True
                    c.p._is_shoot = False

        for e in self.enemies:
            e.update()

    def draw(self):
        super().draw()
        for c in self.characters:
            c.draw()
        for e in self.enemies:
            e.draw()
