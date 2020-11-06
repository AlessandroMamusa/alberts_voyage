# !/usr/bin/env python
# -*- coding: utf-8 -*-

import pyxel


class Character:
    def __init__(self, x, y, img, u, v, w, h):
        self.x = x
        self.y = y
        self.img = img
        self.u = u
        self.v = v
        self.w = w
        self.h = h

    def update(self):
        pass

    def draw(self):
        pyxel.blt(self.x, self.y, self.img, self.u, self.v, self.w, self.h, 0)


class Monkey(Character):
    def __init__(self, x, y):
        super().__init__(x, y, 0, 0, 0, 16, 16)

class Player(Monkey):
    def update(self):
        # add player input
        pass


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
        self.player = Player(x+1, y+6)
        self.enemy = Monkey(x+13, y+8)

    def update(self):
        self.x = self.x

    def draw(self):
        super().draw()
        self.player.draw()
        self.enemy.draw()


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
