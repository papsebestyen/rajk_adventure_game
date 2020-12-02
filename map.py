import pygame
import config
import game
import math
from tile import Tile

class Map():

    def __init__(self, floor):
        self.floor = floor
        self.load_map()
        self.camera = [0, 0]

    def load_map(self):
        with open(f"maps/{self.floor}.txt") as map_file:
            with open(f"maps/{self.floor}_objects.txt") as map_objects_file:
                self.map = [[Tile(map_tile, object_tile) for map_tile, object_tile in zip(map_line.split(), object_line.split())] for map_line, object_line in zip(map_file, map_objects_file)]
        
        for line in self.map:
            print([(tile.background_type, tile.object_type) for tile in line])

    def render_map(self, screen, player):
        self.determine_camera(player)

        calc_rect = lambda x_pos, y_pos: pygame.Rect(x_pos * config.SCALE, y_pos * config.SCALE - (self.camera[1] * config.SCALE), config.SCALE, config.SCALE)

        [[tile.render(screen, calc_rect(x_pos, y_pos)) for x_pos, tile in enumerate(line)] for y_pos, line in enumerate(self.map)]

    def determine_camera(self, player):
        max_y_position = len(self.map) - config.SCREEN_HEIGHT / config.SCALE
        # y_position = self.player.position[1] - math.ceil(round(config.SCREEN_HEIGHT / config.SCALE / 2))
        y_position = player.position[1] - math.ceil(round(config.SCREEN_HEIGHT / config.SCALE / 2))

        if y_position <= max_y_position and y_position >= 0:
            self.camera[1] = y_position
        elif y_position < 0:
            self.camera[1] = 0
        else:
            self.camera[1] = max_y_position
    