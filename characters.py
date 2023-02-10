# !/usr/bin/env python
# -*- coding: utf-8 -*-

import math

import pyxel

from constants import SPRITE_DIM, VO
from projectiles import Projectile


class Character:
    def __init__(self, x, y, img, u, v, w, h, tm, targets, *args, **kwargs):
        self.x = x
        self.y = y
        self.sight_x = x + 23
        self.sight_y = y + 7
        self.sight_angle = 0.0
        self.img = img
        self.u = u
        self.v = v
        self.w = w
        self.h = h
        self.active = False
        self.projectile = Projectile(self.x, self.y, tm, targets)

    def update(self):
        pass

    def draw(self):
        # character sprite
        pyxel.blt(self.x, self.y, self.img, self.u, self.v, self.w, self.h, 0)
        if self._my_turn():
            # sight sprite
            pyxel.blt(
                self.sight_x, self.sight_y, self.img, 32, 0, SPRITE_DIM, SPRITE_DIM, 0
            )
            self.projectile.draw()

    def _my_turn(self):
        return self.active

    def end_turn(self):
        self.active = False


class Monkey(Character):
    def __init__(self, x, y, *args, **kwargs):
        super().__init__(x, y, 0, 0, 0, SPRITE_DIM * 2, SPRITE_DIM * 2, *args, **kwargs)


class Player(Monkey):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.active = True

    def update(self):
        if not self.active:
            return

        if pyxel.btn(pyxel.KEY_LEFT):
            self.sight_angle -= 0.05
            self.sight_x = (
                self.x + SPRITE_DIM + math.cos(self.sight_angle) * SPRITE_DIM * 2
            )
            self.sight_y = (
                self.y + SPRITE_DIM + math.sin(self.sight_angle) * SPRITE_DIM * 2
            )

        if pyxel.btn(pyxel.KEY_RIGHT):
            self.sight_angle += 0.05
            self.sight_x = (
                self.x + SPRITE_DIM + math.cos(self.sight_angle) * SPRITE_DIM * 2
            )
            self.sight_y = (
                self.y + SPRITE_DIM + math.sin(self.sight_angle) * SPRITE_DIM * 2
            )

        if pyxel.btn(pyxel.KEY_UP):
            self.sight_angle -= 0.05
            self.sight_x = (
                self.x + SPRITE_DIM + math.cos(self.sight_angle) * SPRITE_DIM * 2
            )
            self.sight_y = (
                self.y + SPRITE_DIM + math.sin(self.sight_angle) * SPRITE_DIM * 2
            )

        if pyxel.btn(pyxel.KEY_DOWN):
            self.sight_angle += 0.05
            self.sight_x = (
                self.x + SPRITE_DIM + math.cos(self.sight_angle) * SPRITE_DIM * 2
            )
            self.sight_y = (
                self.y + SPRITE_DIM + math.sin(self.sight_angle) * SPRITE_DIM * 2
            )

        if pyxel.btn(pyxel.KEY_SPACE):
            self.projectile.shoot(self.sight_angle, velocity=VO)
        if pyxel.btn(pyxel.KEY_R):
            self.projectile.reload()

        self.projectile.update()
