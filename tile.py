import pygame
import config

class Tile():

    def __init__(self, background_type, object_type):
        self.background_type = background_type
        self.object_type = object_type


    def render(self, screen, rect):
        screen.blit(tile_images[self.background_type], rect)
        if self.object_type != "-":
            screen.blit(tile_images[self.object_type], rect)

tileset = {
    "G": "grass1.png",
    "W": "water.png",
    "S": "garden_stone.png",
    "1": "seat_l.png",
    "2": "seat_m.png",
    "3": "seat_r.png",
    "4": "swimming_pool_c_lt.png",
    "5": "swimming_pool_t.png",
    "6": "swimming_pool_c_lb.png",
    "7": "swimming_pool_b.png",
    "8": "stair_l.png",
    "9": "stair_r.png"
}

load_img = lambda type: pygame.transform.scale(pygame.image.load(f"imgs/{tileset[type]}"), (config.SCALE, config.SCALE))
tile_images = {type: load_img(type) for type in tileset.keys()}