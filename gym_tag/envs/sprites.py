import pygame as pg
from .settings import *

vec = pg.math.Vector2


def collide_with_rects(one, two):
    return one.hit_rect.colliderect(two.rect)


def collide_with_walls(sprite, group, dir):
    if dir == "x":
        hits = pg.sprite.spritecollide(sprite, group, False, collide_with_rects)
        if hits:
            if sprite.vel.x > 0:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if sprite.vel.x < 0:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == "y":
        hits = pg.sprite.spritecollide(sprite, group, False, collide_with_rects)
        if hits:
            if sprite.vel.y > 0:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if sprite.vel.y < 0:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.players
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_image
        self.rect = self.image.get_rect()
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.pos = vec(x, y) * TILESIZE
        self.rot = 0

    def get_action_input(self, action=0):

        if action == 0:
            # do nothing
            # set vx and vy = 0 if no key is pressed
            self.vel = vec(0, 0)
            self.rot_speed = 0
        elif action == 1:
            # forward and turn left
            self.rot_speed = PLAYER_SPEED
            self.vel = vec(PLAYER_SPEED * 0.9, 0).rotate(-self.rot)
        elif action == 2:
            # foward and turn right
            self.rot_speed = -PLAYER_SPEED
            self.vel = vec(PLAYER_SPEED * 0.9, 0).rotate(-self.rot)
        elif action == 3:
            # only forward
            self.vel = vec(PLAYER_SPEED * 0.9, 0).rotate(-self.rot)

    def update(self):
        self.rot = (self.rot + self.rot_speed * self.game.dt) % 360
        self.image = pg.transform.rotate(self.game.player_image, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, "x")
        collide_with_walls(self, self.game.goals, "x")

        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, "y")
        collide_with_walls(self, self.game.goals, "y")
        self.rect.center = self.hit_rect.center


class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.mob_image
        self.rect = self.image.get_rect()
        self.hit_rect = MOB_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y) * TILESIZE
        self.rect.center = self.pos
        self.rot = 0
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def avoid_mobs(self):
        for mob in self.game.mobs:
            if mob != self:
                dist = self.pos - mob.pos
                if 0 < dist.length() < MOB_AVOID_RADIUS:
                    self.acc += dist.normalize()

    def update(self):
        self.rot = (self.game.player.pos - self.pos).angle_to(vec(1, 0))
        self.image = pg.transform.rotate(self.game.mob_image, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.acc = vec(1, 0).rotate(-self.rot)
        self.avoid_mobs()
        self.acc.scale_to_length(MOB_SPEED)
        self.acc += self.vel * -1
        self.vel += self.acc * self.game.dt
        self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, "x")
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, "y")
        self.rect.center = self.hit_rect.center


class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.tile_image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class Goal(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.goals
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.goal_image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
