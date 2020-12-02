import pygame
from pygame import image
import config
from player import Player
from game_state import GameState
import math
from map import Map
from tile import Tile
from tilemap import TiledMap


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.objects = []
        self.game_state = GameState.NONE
        self.map = []
        self.camera = [0, 0]

    def set_up(self):
        player = Player(1, 1)
        self.player = player
        self.objects.append(player)
        print("do set up")
        self.game_state = GameState.RUNNING

        self.map = Map("garden")

    def update(self):
        self.screen.fill(config.WHITE)
        # print("update")
        self.handle_events()
        # self.map.determine_camera(self.player)
        self.map.render_map(self.screen, self.player)

        for object in self.objects:
            object.render(self.screen, self.map.camera)

        # map = TiledMap("map_planning/roguelike-pack/Map/sample_indoor.tmx")
        # map.make_map()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # escape-el bezár
                self.game_state = GameState.ENDED
            #     handle key events
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game_state = GameState.ENDED
                elif event.key == pygame.K_w or event.key == pygame.K_UP:  # up
                    self.move_unit(self.player, [0, -1])
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN:  # down
                    self.move_unit(self.player, [0, 1])
                elif event.key == pygame.K_a or event.key == pygame.K_LEFT:  # up
                    self.move_unit(self.player, [-1, 0])
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:  # up
                    self.move_unit(self.player, [1, 0])

    def move_unit(self, unit, position_change):
        new_position = [unit.position[0] + position_change[0], unit.position[1] + position_change[1]]

        if new_position[0] < 0 or new_position[0] > (len(self.map.map[0]) -1):
            return
        
        if new_position[1] < 0 or new_position[1] > (len(self.map.map) -1):
            return
    
        if self.map.map[new_position[1]][new_position[0]] == "W":
            return

        unit.update_position(new_position)