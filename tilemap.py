from sprites import * 
import pygame as pg
from settings import *
import pytmx

class TiledMap:
    def __init__(self, filename):
        tm = pytmx.load_pygame(filename, pixelalpha = True)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm

    def render(self, surface):
        tile_img = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, glob_id in layer:
                    tile = tile_img(glob_id)
                    if tile:
                        tile = pg.transform.scale(tile, (TILESIZE, TILESIZE))
                        surface.blit(tile, (x * TILESIZE, y * TILESIZE))

    def render_top(self, surface):
        tile_img = self.tmxdata.get_tile_image_by_gid
        for x, y, glob_id in self.tmxdata.get_layer_by_name('top'):
            if glob_id != 0:
                tile = tile_img(glob_id)
                if tile:
                    tile = pg.transform.scale(tile, (TILESIZE, TILESIZE))
                    surface.blit(tile, (x * TILESIZE, y * TILESIZE))
        
    def make_map(self):
        temp_surface = pg.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface

    def make_top_map(self):
        temp_surface = pg.Surface((self.width, self.height)).convert_alpha()
        temp_surface.fill((0, 0, 0, 0))
        self.render_top(temp_surface)
        return temp_surface

class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.x + int(WIDTH / 2)
        y = -target.rect.y + int(HEIGHT / 2)
 
        self.camera = pg.Rect(x, y, self.width, self.height)

class MapShifter(pg.sprite.Sprite):
    def __init__(self, game, x, y, width, height, properties):
        self.groups = game.shifters
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.properties = properties
        self.to_map = properties['to_map']
        self.to_position_x = int(properties['to_position_x'])
        self.to_position_y = int(properties['to_position_y'])
        self.rect = pg.Rect(x, y, width, height)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

    def shift_map(self):
        self.game.map_floor = self.properties['to_map']
        self.game.load_map()
        self.game.new()
        self.game.player = Player(self.game, self.to_position_x, self.to_position_y)
