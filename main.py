# !/usr/bin/env python
# -*- coding: utf-8 -*-

import pyxel

from scenes import CityScene


class App:
    def __init__(self):
        pyxel.init(
            width=128, height=128, title="Albert's voyage", fps=60, quit_key=pyxel.KEY_Q
        )
        pyxel.load("assets/albert.pyxres", image=True, tilemap=True)
        self.city = CityScene(0, 0, 0, 0, 0, pyxel.width, pyxel.height)

        pyxel.run(self.update, self.draw)

    def update(self):
        self.city.update()

    def draw(self):
        self.city.draw()


App()
