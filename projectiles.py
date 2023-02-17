# !/usr/bin/env python
# -*- coding: utf-8 -*-

import math

import pyxel

from constants import SPRITE_DIM, VO


class Projectile:
    def __init__(self, x, y, tm, targets, game, type=None):
        self.x = self.ix = x + 3
        self.y = self.iy = y + 4
        self.targets = targets
        self.game = game

        self.vx = self.vy = self.angle = 0
        self._is_flying = self._has_hit = False
        self.g = 0.08
        self.tm = pyxel.tilemap(0)

    def reload(self):
        self.x = self.ix
        self.y = self.iy
        self.t = self.vx = self.vy = 0
        self._is_flying = self._has_hit = False

    def _check_collision(self):
        if self.y >= pyxel.height - SPRITE_DIM:
            self._has_hit = True
            self._is_flying = False

    def draw(self):
        # _drawPreview(angle)
        if self._is_flying:
            # flying animation
            pyxel.blt(
                self.x, self.y, 0, 16, 8, SPRITE_DIM, SPRITE_DIM, 0
            )  # 16,8 banana sprite in spritesheet
        elif self._has_hit:
            # splat sprite
            pyxel.blt(
                self.x, self.y, 0, 24, 8, SPRITE_DIM, SPRITE_DIM, 0
            )  # 24,8 splat banana sprite in spritesheet
        else:
            # in hand
            pyxel.blt(
                self.x, self.y, 0, 16, 8, SPRITE_DIM, SPRITE_DIM, 0
            )  # 16,8 banana sprite in spritesheet

    def update(self):
        if self._is_flying and not self._has_hit:
            self.vy += self.g  # += because in pyxel the y axis goes down
            self.x = max(
                min(self.x + self.vx, pyxel.width - SPRITE_DIM), 0
            )  # lock banana into the screen
            self.y = max(self.y + self.vy, 0)  # lock banana into the screen
            self._check_collision()

        for target in self.targets:
            if (
                # check for targets hitten
                target.x + target.w > self.x
                and self.x > target.x
                and target.y + target.h > self.y
                and self.y > target.y
            ):
                # play enemy death animation
                self._has_hit = True
                self.targets.remove(target)
                self.game.end_turn()

        if self._has_hit:  # projectile hit something else
            self._has_hit = True
            self._is_flying = False
            self.game.end_turn()

    def shoot(self, angle, velocity, trajectory=None):
        self.vx = VO * math.cos(angle)
        self.vy = VO * math.sin(angle)
        self._is_flying = True

    # To add the preview, pass angle to draw() and decomment the code under
    # def _drawPreview(angle)
    #     x_future = self.ix + 4
    #     y_future = self.iy + 4
    #     vx = VO * math.cos(angle)
    #     vy = VO * math.sin(angle)
    #     vx_future = vx
    #     vy_future = vy
    #     for i in range(60):
    #         vy_future_plus1 = vy_future + self.g
    #         x_future_plus1 = x_future + vx_future
    #         y_future_plus1 = y_future + vy_future
    #         pyxel.line(x_future, y_future, x_future_plus1, y_future_plus1, 7)
    #         vy_future = vy_future_plus1
    #         x_future = x_future_plus1
    #         y_future = y_future_plus1
