import pygame
import config

class Player:
    def __init__(self, x_postition, y_position):
        print("player created")
        self.position = [x_postition, y_position]
        
        image = pygame.image.load(config.PENIS)
        # image = pygame.transform.scale(image, (100, 125))
        image = pygame.transform.flip(image, False, True)
        self.image = image

    def update(self):
        print("player updated")

    def update_position(self, x_change, y_change):
        self.position[0] += x_change
        self.position[1] += y_change

    def render(self, screen):
        # pygame.draw.rect(screen, config.WHITE, (self.position[0] * config.SCALE, self.position[1] * config.SCALE, config.SCALE, config.SCALE), 4)
        screen.blit(self.image, (self.position[0] * config.SCALE, self.position[1] * config.SCALE, config.SCALE, config.SCALE))