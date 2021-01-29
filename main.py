import pygame as pg
import sys
from settings import *
from sprites import *
from os import path
from tilemap import *

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(300, 100)
        self.load_data()
        self.info = []
        self.player = None
        self.stop = False
        self.show_stat = False
        self.show_end = False
    
    def load_data(self):
        game_folder = path.dirname(__file__)
        self.img_folder = path.join(game_folder, 'img')
        self.map_folder = path.join(game_folder, 'maps')
        self.font_folder = path.join(game_folder, 'fonts')
        characters_folder = path.join(game_folder, 'charcaters')

        self.show_debug = False
        self.map_floor = 'udvar'

        self.font = pg.font.Font(path.join(self.font_folder, 'SuperLegendBoy-4w8Y.ttf'), TEXTSIZE)
        self.font_bold = pg.font.Font(path.join(self.font_folder, 'SuperLegendBoy-4w8Y.ttf'), TEXTSIZE)
        self.font_big = pg.font.Font(path.join(self.font_folder, 'SuperLegendBoy-4w8Y.ttf'), TEXTSIZE + 30)

        self.question = QuestionBox(self)
        self.stat = Stats(self)
        self.game_time = GameTime(self)

        self.load_characters(path.join(characters_folder, 'characters.tmx'))

    def load_characters(self, filename):
        self.characters = dict()
        tmx = pytmx.load_pygame(filename, pixelalpha = True)
        tile_img = tmx.get_tile_image_by_gid
        for layer in tmx.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                direction_i = 0
                new = dict()
                for x, y, glob_id in layer:
                    if glob_id != 0:
                        tile = tile_img(glob_id)
                        if tile:
                            tile = pg.transform.scale(tile, (TILESIZE, TILESIZE))
                            new[CHAR_DIRS[direction_i]] = tile
                        direction_i += 1
                self.characters[layer.name] = new

    def load_map(self):
        self.map = TiledMap(path.join(self.map_folder, f'{self.map_floor}.tmx'))
        self.map_img = self.map.make_map()
        self.map_top_img = self.map.make_top_map()
        self.map_rect = self.map_img.get_rect()
    
    def new(self):
        self.load_map()
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.shifters = pg.sprite.Group()

        for tile_object in self.map.tmxdata.objects:
            if tile_object.name == 'player' and not self.player:
                self.player = Player(self, tile_object.x, tile_object.y)
            elif tile_object.name == 'obstacle':
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            elif tile_object.name == 'mob':
                Mob(self, tile_object.x, tile_object.y, tile_object.properties)
            elif tile_object.name == 'shifter':
                MapShifter(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height, tile_object.properties)

        self.camera = Camera(self.map.width, self.map.height)

    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            if not self.show_stat:
                self.game_time.time += self.dt
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def debug_info(self, screen):
        font = pg.font.SysFont('Times New Roman', 20)
        information = [
            f'Player position: {(self.player.rect.x, self.player.rect.y)}, in grid {(self.player.rect.x / TILESIZE, self.player.rect.y / TILESIZE)}',
            f'Player new position: {(self.player.new_rect.x, self.player.new_rect.y)}, in grid {(self.player.new_rect.x / TILESIZE, self.player.new_rect.y / TILESIZE)}',
            '',
            f'Player direction: {self.player.direction}',
            f'Player speed: {self.player.speed}',
            f'Player step speed {self.player.step_speed}'
            f'Moving: {self.player.moving}',
            f'Move time: {int(self.player.move_time)}',
            '',
            f'Camera offset: {list(map(lambda x: int(x / TILESIZE), self.camera.camera.topleft))}',
            f'Camera offset in pixel: {list(self.camera.camera.topleft)}',
            '',
            f'FPS: {self.clock.get_fps():.2f}',
            f'Stop: {self.stop}',
            '',
            f'Map size: {[self.map.tmxdata.width, self.map.tmxdata.height]}',
            f'Map size in pixel: {[self.map.tmxdata.width * TILESIZE, self.map.tmxdata.height * TILESIZE]}',
            f'{self.walls}',
            f'{pg.sprite.spritecollide(self.player, self.walls, False)}',
            f'{self.player.rect}'
        ]
        self.info = [font.render(text, False, YELLOW) for text in information]

    def update(self):
        if not self.stop and not self.show_end and not self.show_stat:
            self.mobs.update()
            self.player.update()
    
        self.camera.update(self.player)

        self.debug_info(self.screen)

        self.game_time.update()

    def draw(self):

        self.screen.fill(BLACK)

        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))

        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))

        self.screen.blit(self.map_top_img, self.camera.apply_rect(self.map_rect))

        self.game_time.apply()

        if self.show_end:
            self.draw_end()

        if self.stop:
            self.question.apply()

        if self.show_stat:
            self.stat.apply()

        if self.show_debug:
            [self.screen.blit(text, (10, text_index * 20)) for text_index, text in enumerate(self.info)]

        pg.display.flip()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_0:
                    self.show_debug = not self.show_debug
                if event.key == pg.K_p:
                    self.show_stat = not self.show_stat
        if not self.stop:
            self.player.get_keys()
        else:
            self.question.get_keys()

    def draw_end(self):
        end_text = text_to_surf(self.font_big, 'RAJKOS DIPLOMÁD')
        end_surf = pg.Surface((WIDTH, HEIGHT * 0.1))
        end_surf.fill(TEXTBOX_COLOR)
        end_surf.blit(end_text, ((end_surf.get_width() - end_text.get_width()) / 2, (end_surf.get_height() - end_text.get_height()) / 2))
        self.screen.blit(end_surf, (0, 0))
        self.show_stat = True


g = Game()
while True:
    g.new()
    g.run()
