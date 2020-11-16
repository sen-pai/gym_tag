import pygame as pg
import sys
from os import path
import os
from settings import *
from sprites import *


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()

    def load_data(self):
        game_folder = path.dirname(__file__)
        self.image_folder = path.join(os.getcwd(), "assets")

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

        self.map_data = []
        with open(path.join(game_folder, "map.txt"), "rt") as f:
            for line in f:
                self.map_data.append(line)

    def new(self):
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
                    self.mob = Goal(self, col, row)

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()

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

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()


# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
