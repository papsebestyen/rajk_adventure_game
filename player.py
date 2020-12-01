import pygame
import config

class Player:
    def __init__(self, x_postition, y_position):
        print("player created")
        self.position = [x_postition, y_position]
        
        image = pygame.image.load(config.PENIS)
        # image = pygame.transform.scale(image, (100, 125))
        # image = pygame.transform.flip(image, False, True)
        self.image = pygame.image.load("imgs/player.png")
        self.image = pygame.transform.scale(self.image, (config.SCALE, config.SCALE))
        self.rect =pygame.Rect(self.position[0] * config.SCALE, self.position[1] * config.SCALE, config.SCALE, config.SCALE)

    def update(self):
        print("player updated")

    def update_position(self, new_position):
        self.position[0] = new_position[0]
        self.position[1] = new_position[1]
        self.rect = pygame.Rect(self.position[0] * config.SCALE, self.position[1] * config.SCALE, config.SCALE, config.SCALE)

    def render(self, screen, camera):
        # pygame.draw.rect(screen, config.WHITE, (self.position[0] * config.SCALE, self.position[1] * config.SCALE, config.SCALE, config.SCALE), 4)
        self.rect = pygame.Rect(self.position[0] * config.SCALE, self.position[1] * config.SCALE - (camera[1] * config.SCALE), config.SCALE, config.SCALE)
        screen.blit(self.image, self.rect)