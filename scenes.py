# !/usr/bin/env python
# -*- coding: utf-8 -*-
import pyxel

from characters import Monkey, Player

S_T_M = 8


class Scene:
    def __init__(self, x, y, tm, u, v, w, h, game):
        self.x = x
        self.y = y
        self.tm = tm
        # TODO: this are info relative to the tilemap, define them inside
        self.u = u
        self.v = v
        self.w = w
        self.h = h
        self.game = game

    def update(self):
        pass

    def draw(self):
        pyxel.bltm(self.x, self.y, self.tm, self.u, self.v, self.w, self.h)


class CityScene(Scene):
    def __init__(self, x, y, tm, u, v, w, h, game):
        super().__init__(x, y, tm, u, v, w, h, game)
        self.characters = []
        self.enemies = []
        player = Player(x + 1 * S_T_M, y + 6 * S_T_M, tm)
        enemy = Monkey(x + 13 * S_T_M, y + 8 * S_T_M, tm)
        self.characters.append(player)
        self.enemies.append(enemy)

        self.turn = 0

    def update(self):
        for character in self.characters:
            character.update()
            # if not character.projectile._is_shoot:
            #     continue
            for enemy in self.enemies:
                if (
                    # check for enemies hitten
                    enemy.x + enemy.w > character.projectile.x
                    and character.projectile.x > enemy.x
                    and enemy.y + enemy.h > character.projectile.y
                    and character.projectile.y > enemy.y
                ):
                    # play enemy death animation
                    character.projectile._has_hit = True
                    self.enemies.pop()
                    if len(self.enemies) == 0:
                        self.game.victory()
            if (character.projectile._has_hit):  # projectile hit something else
                character.projectile._has_hit = True
                character.projectile._is_shoot = False
                character.endTurn()
                self.turn += 1

        for e in self.enemies:
            e.update()

    def draw(self):
        super().draw()
        for c in self.characters:
            c.draw()
        for e in self.enemies:
            e.draw()


SCENES = [CityScene]
VICTORY_SCENE = Scene
GAME_OVER_SCENE = Scene
