import pygame
from pygame import image
import config
from player import Player
from game_state import GameState


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.objects = []
        self.game_state = GameState.NONE
        self.map = []

    def set_up(self):
        player = Player(1, 1)
        self.player = player
        self.objects.append(player)
        print("do set up")
        self.game_state = GameState.RUNNING

        self.load_map("01")

    def update(self):
        self.screen.fill(config.WHITE)
        print("update")
        self.handle_events()

        self.render_map(self.screen)

        for object in self.objects:
            object.render(self.screen)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # escape-el bezár
                self.game_state = GameState.ENDED
            #     handle key events
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game_state = GameState.ENDED
                elif event.key == pygame.K_w or event.key == pygame.K_UP:  # up
                    self.player.update_position(0, -1)
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN:  # down
                    self.player.update_position(0, 1)
                elif event.key == pygame.K_a or event.key == pygame.K_LEFT:  # up
                    self.player.update_position(-1, 0)
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:  # up
                    self.player.update_position(1, 0)

    def load_map(self, file_name):
        with open(f"maps/{file_name}.txt") as map_file:
            
            for line in map_file:
                tiles = []

                for i in range(0, len(line), 2):
                    tiles.append(line[i])

                self.map.append(tiles)

            print(self.map)

    def render_map(self, screen):
        y_pos = 0
        for line in self.map:
            x_pos = 0
            for tile in line:
                image = map_tile_image[tile]
                rect = pygame.Rect(x_pos * config.SCALE, y_pos * config.SCALE, config.SCALE, config.SCALE)
                screen.blit(image, rect)
                x_pos += 1
            y_pos += 1

map_tile_image = {
    "G": pygame.transform.scale(pygame.image.load("imgs/grass1.png"), (config.SCALE, config.SCALE)),
    "W": pygame.transform.scale(pygame.image.load("imgs/water.png"), (config.SCALE, config.SCALE))
}