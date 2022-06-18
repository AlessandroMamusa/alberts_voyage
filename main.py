# !/usr/bin/env python
# -*- coding: utf-8 -*-

import math

import pyxel

# SPRITE_TO_TILE_MODIFIER
S_T_M = 8

# costant velocity (to be replaced in future)
VO = 3


class Projectile:
    def __init__(self, x, y, tm, type=None):
        self.x = self.ix = x + 3
        self.y = self.iy = y + 4
        self.vx = self.vy = self.angle = 0
        self._is_shoot = self._has_hit = False
        self.g = 0.08
        self.tm = pyxel.tilemap(0)

    def reload(self):
        self.x = self.ix
        self.y = self.iy
        self.t = self.vx = self.vy = 0
        self._is_shoot = self._has_hit = False

    def _check_collision(self):
        if self.y >= 120:
            self._has_hit = True
            self._is_shoot = False

    def draw(self):
        # _drawPreview(angle)
        if self._is_shoot:
            # add animation
            pyxel.blt(self.x, self.y, 0, 17, 9, 4, 7, 0)
        elif self._has_hit:
            pyxel.blt(self.x, self.y, 0, 24, 10, 7, 5, 0)
        else:
            pyxel.blt(self.x, self.y, 0, 17, 9, 4, 7, 0)

    def update(self):
        if self._is_shoot and not self._has_hit:
            self.vy += self.g  # += because in pyxel the y axis goes down
            self.x = min(self.x + self.vx, 126)
            self.y = max(self.y + self.vy, 0)
            self._check_collision()

    def shoot(self, angle, velocity, trajectory=None):
        self.vx = VO * math.cos(angle)
        self.vy = VO * math.sin(angle)
        self._is_shoot = True

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
    def __init__(self, x, y, img, u, v, w, h, tm, *args, **kwargs):
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
        self.p = Projectile(self.x, self.y, tm)

    def update(self):
        pass

    def draw(self):
        # character sprite
        pyxel.blt(self.x, self.y, self.img, self.u, self.v, self.w, self.h, 0)
        if self._myTurn():
            # sight sprite
            pyxel.blt(self.sight_x, self.sight_y, self.img, 32, 0, 8, 8, 0)
            self.p.draw()

    def _myTurn(self):
        return self.active


class Monkey(Character):
    def __init__(self, x, y, *args, **kwargs):
        super().__init__(x, y, 0, 0, 0, 16, 16, *args, **kwargs)


class Player(Monkey):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.active = True

    def update(self):
        if not self.active:
            return

        if pyxel.btn(pyxel.KEY_LEFT):
            self.sight_angle -= 0.05
            self.sight_x = self.x + 8 + math.cos(self.sight_angle) * 16
            self.sight_y = self.y + 8 + math.sin(self.sight_angle) * 16

        if pyxel.btn(pyxel.KEY_RIGHT):
            self.sight_angle += 0.05
            self.sight_x = self.x + 8 + math.cos(self.sight_angle) * 16
            self.sight_y = self.y + 8 + math.sin(self.sight_angle) * 16

        if pyxel.btn(pyxel.KEY_UP):
            self.sight_angle -= 0.05
            self.sight_x = self.x + 8 + math.cos(self.sight_angle) * 16
            self.sight_y = self.y + 8 + math.sin(self.sight_angle) * 16

        if pyxel.btn(pyxel.KEY_DOWN):
            self.sight_angle += 0.05
            self.sight_x = self.x + 8 + math.cos(self.sight_angle) * 16
            self.sight_y = self.y + 8 + math.sin(self.sight_angle) * 16

        self.p.update()
        if pyxel.btn(pyxel.KEY_SPACE):
            self.p.shoot(self.sight_angle, velocity=VO)
        if pyxel.btn(pyxel.KEY_R):
            self.p.reload()


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
        player = Player(x + 1 * S_T_M, y + 6 * S_T_M, tm)
        enemy = Monkey(x + 13 * S_T_M, y + 8 * S_T_M, tm)
        self.characters.append(player)
        self.characters.append(enemy)

    def update(self):
        for c in self.characters:
            c.update()

    def draw(self):
        super().draw()
        for c in self.characters:
            c.draw()


class App:
    def __init__(self):
        pyxel.init(
            width=128, height=128, title="Albert's voyage", fps=60, quit_key=pyxel.KEY_Q
        )
        pyxel.load("assets/albert.pyxres", image=True, tilemap=True)
        self.city = CityScene(0, 0, 0, 0, 0, 128, 128)

        pyxel.run(self.update, self.draw)

    def update(self):
        self.city.update()

    def draw(self):
        self.city.draw()


App()
