# !/usr/bin/env python
# -*- coding: utf-8 -*-

import pyxel
import math

# SPRITE_TO_TILEMAP_MODIFIER
S_T_M = 8


class Character:
    def __init__(self, x, y, img, u, v, w, h, *args, **kwargs):
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
            # X := originX + cos(angle)*radius
            # Y := originY + sin(angle)*radius
            self.sight_angle -= 0.1
            self.sight_x = self.x+8 + math.cos(self.sight_angle)*16
            self.sight_y = self.y+8 + math.sin(self.sight_angle)*16

        if pyxel.btn(pyxel.KEY_RIGHT):
            self.sight_angle += 0.1
            self.sight_x = self.x+8 + math.cos(self.sight_angle)*16
            self.sight_y = self.y+8 + math.sin(self.sight_angle)*16

        if pyxel.btn(pyxel.KEY_UP):
            self.sight_angle -= 0.1
            self.sight_x = self.x+8 + math.cos(self.sight_angle)*16
            self.sight_y = self.y+8 + math.sin(self.sight_angle)*16

        if pyxel.btn(pyxel.KEY_DOWN):
            self.sight_angle += 0.1
            self.sight_x = self.x+8 + math.cos(self.sight_angle)*16
            self.sight_y = self.y+8 + math.sin(self.sight_angle)*16



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
        player = Player(x+1*S_T_M, y+6*S_T_M)
        enemy = Monkey(x+13*S_T_M, y+8*S_T_M)
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
        pyxel.init(width=128, height=128, caption="Albert's journey", fps=60)
        pyxel.load("assets/albert.pyxres")
        self.city = CityScene(0, 0, 0, 0, 0, 16, 16)

        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        self.city.update()

    def draw(self):
        self.city.draw()


App()
