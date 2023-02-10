# !/usr/bin/env python
# -*- coding: utf-8 -*-

import math

import pyxel

# SPRITE_TO_TILE_MODIFIER
SPRITE_DIM = 8

# costant velocity (to be replaced in future)
VO = 3


class Projectile:
    def __init__(self, x, y, tm, targets, type=None):
        self.x = self.ix = x + 3
        self.y = self.iy = y + 4
        self.vx = self.vy = self.angle = 0
        self._is_flying = self._has_hit = False
        self.g = 0.08
        self.tm = pyxel.tilemap(0)
        self.targets = targets

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
                self.targets.pop()
        if self._has_hit:  # projectile hit something else
            self._has_hit = True
            self._is_flying = False

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
