# !/usr/bin/env python
# -*- coding: utf-8 -*-

import pyxel

from scenes import SCENES, VICTORY_SCENE, GAME_OVER_SCENE


class Game:
    def __init__(self):
        self._current_scene = 0
        self.scene = SCENES[self._current_scene]

    def start(self):
        self._scene_instance = self.scene(0, 0, 0, 0, 0, pyxel.width, pyxel.height, self)

    def victory(self):
        self.scene = VICTORY_SCENE

    def game_over(self):
        self.scene = GAME_OVER_SCENE

    def next_scene(self):
        self._current_scene += 1
        self.scene = SCENES[self._current_scene]
        # destroy last scene
        # init new scene

    def update(self):
        self._scene_instance.update()

    def draw(self):
        self._scene_instance.draw()


class App:
    def __init__(self):
        pyxel.init(
            width=128, height=128, title="Albert's voyage", fps=60, quit_key=pyxel.KEY_Q
        )
        pyxel.load("assets/albert.pyxres", image=True, tilemap=True)
        self.game = Game()
        self.game.start()
        pyxel.run(self.update, self.draw)

    def update(self):
        self.game.update()

    def draw(self):
        self.game.draw()


App()
