import pygame as pg

import gym
from gym import spaces, error

import numpy as np
import matplotlib.pyplot as plt
import math, random
import os
from os import path
import sys
from .settings import *
from .sprites import *

"""
Instead of registering multiple environments with different configs,
I pass a dictionary that hass all the tweaks you can do to the environment

Things you can change
"map": Check maps folder, create your own map if you want
"env_type": 3 options ["goal", "empty", "mob"] this influences your reward function
"reward type": 2 options ["dense", "sparce"]
"""
base_config = {"map": "empty_map.txt",
"env_type": "empty",
"reward_type": "dense",
}

class EmptyEnv(gym.Env):

    def __init__(self, config = base_config):
        os.environ["SDL_VIDEODRIVER"] = "dummy"
        pg.init()
        pg.display.init()
        pg.display.set_mode((1, 1), pg.NOFRAME)
        self.screen = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA, 32)
        self.clock = pg.time.Clock()

        self.config = config
        print(self.config["map"])
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Box(low=0.0, high=256.0, shape=(384, 384, 3))
        self.load_data()
        self.reset()

    def set_config(self, new_config):
        """
        if you have a new config call it right after gym.make
        """
        self.config = new_config
        self.load_data()
        self.reset()

    def load_data(self):

        self.map_data = []

        game_folder = path.dirname(__file__)
        self.maps_folder = path.join(game_folder, "maps")
        self.image_folder = path.join(game_folder, "assets")

        with open(path.join(self.maps_folder, self.config["map"]), "rt") as f:
            for line in f:
                self.map_data.append(line)


        # load player image
        self.player_image = pg.image.load(
            path.join(self.image_folder, "manBlue_gun.png")
        ).convert_alpha()
        # rescale image to fit tilesize
        self.player_image = pg.transform.scale(self.player_image, (TILESIZE, TILESIZE))

        # load tile image
        self.tile_image = pg.image.load(path.join(self.image_folder, "tile.png"))
        # rescale image to fit tilesize
        self.tile_image = pg.transform.scale(self.tile_image, (TILESIZE, TILESIZE))

        # load goal image
        self.goal_image = pg.image.load(path.join(self.image_folder, "crate_45.png"))
        # rescale image to fit tilesize
        self.goal_image = pg.transform.scale(self.goal_image, (TILESIZE, TILESIZE))

        # load mob image
        self.mob_image = pg.image.load(
            path.join(self.image_folder, "zombie1_hold.png")
        ).convert_alpha()
        # rescale image to fit tilesize
        self.mob_image = pg.transform.scale(self.mob_image, (TILESIZE, TILESIZE))

    def reset(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.players = pg.sprite.Group()
        self.goals = pg.sprite.Group()
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile == "1":
                    Wall(self, col, row)
                if tile == "P":
                    self.player = Player(self, col, row)
                if tile == "M":
                    self.mob = Mob(self, col, row)
                # if tile == "G":
                #     self.mob = Goal(self, col, row)

        self.dt = self.clock.tick(FPS) / 1000
        self.player.get_action_input()
        self.all_sprites.update()
        self.draw()

        return self._get_obs()

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        pg.display.flip()

    def _get_obs(self):
        return pg.surfarray.array3d(self.screen).swapaxes(0, 1)

    def _reward_func(self):
        pass

    def _check_done(self):
        pass

    def step(self, action):
        """4 actions
        0 = do nothing
        1 = turn left + forward
        2 = turn right + forward
        3 = forward
        """
        self.player.get_action_input(action)
        self.all_sprites.update()
        self.draw()

        obs = self._get_obs()
        reward = -1
        done = False
        info = {}

        return obs, reward, done, info

    def render(self, mode="human", close=False):
        pass

    def save_obs(self, save_name):
        obs = self._get_obs()
        plt.imsave(save_name, obs)

    def close(self):
        pg.quit()
        sys.exit()
