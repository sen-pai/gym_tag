import pygame as pg

import gym
from gym import spaces, error

import numpy as np
import math
import os
from os import path

from .settings import *
from .sprites import *

"""
Instead of registering multiple environments with different configs,
I pass a dictionary that hass all the tweaks you can do to the environment

Things you can change
"map": Check maps folder, create your own map if you want
"env_type": 3 options ["goal", "empty", "mob"] this influences your reward function
"reward type": 2 options ["survival", "distance"]
"action type": 2 options(for now ) ["type1", "type2"]

"""
base_config = {
    "map": "empty_map.txt",
    "env_type": "empty",
    "reward_type": "survival",
    "action type": "type2",
}


class EmptyEnv(gym.Env):
    def __init__(self, config=base_config):
        os.environ["SDL_VIDEODRIVER"] = "dummy"
        # pg.init()
        # pg.display.init()
        # pg.display.set_mode((1, 1), pg.NOFRAME)
        # self.screen = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA, 32)
        # self.clock = pg.time.Clock()

        self.config = config

        # self.load_data()

        # max timesteps for the mob version
        self.steps = 0
        self.mob_max_steps = 1000
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Box(low=0.0, high=256.0, shape=(384, 384, 3))

        self.reset()

    def set_config(self, new_config):
        """
        if you have a new config call it right after gym.make()
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
        pg.init()
        pg.display.init()
        pg.display.set_mode((1, 1), pg.NOFRAME)
        self.screen = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA, 32)
        self.clock = pg.time.Clock()
        self.load_data()

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
                if tile == "G":
                    self.goal = Goal(self, col, row)

        self.dt = self.clock.tick(FPS) / 1000
        if self.config["action type"] == "type1":
            self.player.get_action_input()
        elif self.config["action type"] == "type2":
            self.player.get_action_input_type_2()

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
        # self.draw_grid()
        self.all_sprites.draw(self.screen)
        pg.display.flip()

    def _get_obs(self):
        return np.array(pg.surfarray.array3d(self.screen).swapaxes(0, 1))

    def _reward_func(self):
        self.goal_reached_reward = 10
        self.mob_hit_punishment = -1

        if self.config["env_type"] == "goal":
            assert self.config["map"].startswith("goal"), "need a goal map, change map or env_type"

            # return distance between player and goal
            # dist = round(
            #     -math.hypot(self.goal.x - self.player.pos.x, self.goal.y - self.player.pos.y)
            #     / TILESIZE,
            #     2,
            # )

            hits = pg.sprite.spritecollide(self.player, self.goals, False)

            if self.config["reward_type"] == "distance":
                # if goal hit return 10
                if hits:
                    return self.goal_reached_reward
                return -0.1
            elif self.config["reward_type"] == "survival":
                if hits:
                    return self.goal_reached_reward
                return -0.1

        if self.config["env_type"] == "mob":
            assert self.config["map"].startswith("mob"), "need a mob map, change map or env_type"

            # fixed reward type for mob
            # +0.1 every timestep
            # -1 if hit by mob
            #
            # hitx = collide_with_walls(self.player, self.mobs, "x")
            # hity = collide_with_walls(self.player, self.mobs, "y")

            hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_with_rects)
            # print(hits)
            if hits:
                return self.mob_hit_punishment
            return 0.1

    def _check_done(self):
        if self.config["env_type"] == "goal":
            if self._reward_func() == self.goal_reached_reward:
                return True
            return False

        if self.config["env_type"] == "mob":
            if self.mob_max_steps == self.steps:
                return True
            return False

        if self.config["env_type"] == "empty":
            return False

    def step(self, action):
        """4 actions
        0 = do nothing
        1 = turn left + forward
        2 = turn right + forward
        3 = forward
        """
        if self.config["action type"] == "type1":
            self.player.get_action_input(action)
        elif self.config["action type"] == "type2":
            self.player.get_action_input_type_2(action)

        self.all_sprites.update()
        self.draw()

        obs = self._get_obs()
        reward = self._reward_func()
        done = self._check_done()
        info = {}

        self.steps += 1
        return obs, reward, done, info

    def render(self, mode="human", close=False):
        pass

    def close(self):
        pg.quit()

    def seed(self, seed):
        # no randomness in the env, but keeping the method to avoid future errors
        pass
