import pygame as pg
from pygame import image
from settings import *
from copy import deepcopy

vec = pg.math.Vector2

def round_vec(vec):
    vec.x = round(vec.x / TILESIZE) * TILESIZE
    vec.y = round(vec.y / TILESIZE) * TILESIZE
    return vec

class Person():

    def __init__(self, game, x, y, image_dict):
        self.game = game
        self.move_time = 0
        self.moving = False
        self.direction = 'down'
        self.speed = vec(0, 0)
        self.new_rect = vec(x, y)
        self.float_rect = vec(x, y)
        self.image_dict = image_dict
        self.image = self.image_dict[f'{self.direction}_0']
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.step_speed = vec(0, 0)

    def update_image(self):
        if self.speed.x > 0.5:
            self.direction = 'right'
        if self.speed.x < -0.5:
            self.direction = 'left'
        if self.speed.y > 0.5:
            self.direction = 'down'
        if self.speed.y < -0.5:
            self.direction = 'up'

        if self.move_time != 0:
            self.image = self.image_dict[f'{self.direction}_{self.clock_to_move_state()}']
        else:
            self.image = self.image_dict[f'{self.direction}_0']

    def clock_to_move_state(self):
        state = int(self.move_time * MOVE_FPS) % 4
        return [0, 1, 0, 2][state]

    def round_vec(self):
        if self.step_speed.x != 0:
            self.float_rect.x = (self.float_rect.x // TILESIZE) * TILESIZE if self.step_speed.x > 0 else (self.float_rect.x // TILESIZE + 1) * TILESIZE
        if self.step_speed.y != 0:
            self.float_rect.y = (self.float_rect.y // TILESIZE) * TILESIZE if self.step_speed.y > 0 else (self.float_rect.y // TILESIZE + 1) * TILESIZE

    def check_step(self):
        if self.speed:
            self.target = self.float_rect + self.speed * TILESIZE
            self.step_speed = deepcopy(self.speed)

    def collide(self):
        self.round_vec()
        self.step_speed = vec(0, 0)
        self.rect.x, self.rect.y = self.float_rect.x, self.float_rect.y
        self.move_time = 0

    def do_step(self):
        step = self.float_rect + self.step_speed * SPEED * self.game.dt * TILESIZE
        
        if self.float_rect.distance_to(step) > self.float_rect.distance_to(self.target):
            self.float_rect = self.target
            self.step_speed = vec(0, 0)
            if not self.speed:
                self.move_time = 0
            else:
                self.move_time += self.game.dt
        else:
            self.float_rect = step
            self.move_time += self.game.dt

        self.rect.x, self.rect.y = self.float_rect.x, self.float_rect.y
        
        if self.collide_check():
            self.collide()

        self.update_image()

    