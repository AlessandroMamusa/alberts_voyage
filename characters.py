# !/usr/bin/env python
# -*- coding: utf-8 -*-

import math

import pyxel

from constants import SPRITE_DIM, VO
from projectiles import Projectile


class Character:
    def __init__(self, x, y, img, u, v, w, h, tm, game, targets, *args, **kwargs):
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
        self.is_active = False
        self.projectile = None
        self.tm = tm
        self.game = game
        self.targets = targets

    def update(self):
        if self.is_active:
            self.projectile = self._get_projectile()
            self.projectile.update()
        else:
            # destroy the projectile?
            self.projectile = None

    def draw(self):
        # character sprite
        pyxel.blt(self.x, self.y, self.img, self.u, self.v, self.w, self.h, 0)
        if self.is_active:
            # sight sprite
            pyxel.blt(
                self.sight_x, self.sight_y, self.img, 32, 0, SPRITE_DIM, SPRITE_DIM, 0
            )
            if self.projectile:
                self.projectile.draw()

    def _get_projectile(self):
        if not self.projectile:
            self.projectile = Projectile(
                self.x, self.y, self.tm, self.targets, self.game
            )
        return self.projectile


class Monkey(Character):
    def __init__(self, x, y, *args, **kwargs):
        super().__init__(x, y, 0, 0, 0, SPRITE_DIM * 2, SPRITE_DIM * 2, *args, **kwargs)


class Player(Monkey):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def update(self):
        super().update()
        if not self.is_active:
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
