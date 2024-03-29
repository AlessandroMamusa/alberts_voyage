# !/usr/bin/env python
# -*- coding: utf-8 -*-

# ####### TODOS ########
# DONE: generate skyline
# DONE: place player and enemie/s
# DONE: turns
# DONE: projectiles that interact with buildings (holes) and player + enemies
# TODO: enemy AI
# TODO: camera that follow projectile
# TODO: schenes (menu, start, win, game over)
# TODO: add HUD
# TODO: core ready?
# TODO: schene start from enemies position and transition to player
# TODO: toggle to move the camera around
# ######################

# ######## BUGS & IMPROVEMENTS ########
# scope starting in wrong position
# banana starting in wrong position
# manage collisions for different shapes
# #####################################

import pyxel

from characters import Character
from scenes import GAME_OVER_SCENE, SCENES, VICTORY_SCENE


class Game:
    def __init__(self):
        self._current_scene = 1
        self.scene_cls = SCENES[self._current_scene]
        self.players = []
        self.enemies = []
        self.turn_manager = TurnManager(self)

    def update(self):
        self.scene.update()
        for p in self.players:
            p.update()
        for e in self.enemies:
            e.update()

    def draw(self):
        self.scene.draw()
        for p in self.players:
            p.draw()
        for e in self.enemies:
            e.draw()

    def start(self):
        self.scene = self.scene_cls(0, 0, 0, 0, 0, pyxel.width, pyxel.height, self)
        self.turn_manager.start()

    def end_turn(self):
        self.turn_manager.pass_turn()

    def victory(self):
        self.scene_cls = VICTORY_SCENE

    def game_over(self):
        self.scene_cls = GAME_OVER_SCENE

    def next_scene(self):
        self._current_scene += 1
        self.scene_cls = SCENES[self._current_scene]
        # destroy last scene
        # init new scene

    def does_hit(self, box):
        characters = {*self.players, *self.enemies} - {self.turn_manager.active_entity}
        for c in characters:
            if c.collide(box):
                c.hit(box)
                return True
        if self.scene.collide(box):
            self.scene.hit(box)
            return True
        return False


class TurnManager:
    def __init__(self, game):
        self.game = game
        self.active_entity = None

    def start(self):
        self.counter = 0
        self.active_entity: Character = [*self.game.players, *self.game.enemies][0]
        self.active_entity.is_active = True

    def pass_turn(self):
        self.active_entity.is_active = False
        self.counter += 1
        entities = self.game.players + self.game.enemies
        self.active_entity = entities[self.counter % len(entities)]
        self.active_entity.is_active = True


class App:
    def __init__(self):
        pyxel.init(
            width=256, height=128, title="Albert's voyage", fps=30, quit_key=pyxel.KEY_Q
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
