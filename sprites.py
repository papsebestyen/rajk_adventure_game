import pygame as pg
from settings import *
from person import *
from os import path
import datetime

def convert_image(file_path, img_size):
    image = pg.image.load(file_path).convert_alpha()
    return pg.transform.scale(image, img_size)

vec = pg.math.Vector2
def round_vec(vec):
    vec.x = round(vec.x)
    vec.y = round(vec.y)
    return vec

class Player(pg.sprite.Sprite, Person):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        Person.__init__(self, game, x, y, game.characters[PLAYER_IMG])

    def get_keys(self):
        self.speed = vec(0, 0)
        pressed = pg.key.get_pressed()
        if pressed[pg.K_RIGHT]:
            self.speed = vec(1, 0)
        elif pressed[pg.K_LEFT]:
            self.speed = vec(-1, 0)
        elif pressed[pg.K_DOWN]:
            self.speed = vec(0, 1)
        elif pressed[pg.K_UP]:
            self.speed = vec(0, -1)

    def update(self):
        if not self.step_speed:
            self.check_step()
        if self.step_speed:
            self.do_step()

    def collide_check(self):
        if pg.sprite.spritecollide(self, self.game.walls, False):
            return True
        if pg.sprite.spritecollide(self, self.game.shifters, False):
            pg.sprite.spritecollide(self, self.game.shifters, False)[0].shift_map()
        if pg.sprite.spritecollide(self, self.game.mobs, False):
            self.game.question.get_text(pg.sprite.spritecollide(self, self.game.mobs, False)[0])
            self.speed = vec(0, 0)
            return True
         

class Mob(pg.sprite.Sprite, Person):
    def __init__(self, game, x, y, properties):
        self.name = properties['mob_id']
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        Person.__init__(self, game, x, y, game.characters[MOBS[self.name]['character']])
        self.mob_step = 0
        self.mob_move = [vec(int(move.split(',')[0]), int(move.split(',')[1])) for move in properties['move'].split(';')] if properties['move'] else []

    def update(self):
        if not self.step_speed:
            
            if len(self.mob_move) != 0:
                if self.mob_step > len(self.mob_move) - 1:
                    self.mob_step = 0

                self.target = self.mob_move[self.mob_step]
                self.step_speed = pg.math.Vector2.normalize(self.target - self.float_rect)
                self.speed = self.step_speed
            else:
                self.step_speed = vec(0, 0)
            self.start = self.float_rect
            self.mob_step += 1

        if self.step_speed:
            self.do_step()

    def collide_check(self):
        if pg.sprite.spritecollide(self, [self.game.player], False):
            self.mob_step -= 1
            return True

class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, width, height):
        self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, width, height)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

def text_to_surf(font, text):
    return font.render(text, False, BLACK)

def vec_to_ans(vector):
    if vector.x == 1:
        if vector.y == 1:
            return 'd'
        else:
            return 'b'
    else:
        if vector.y == 1:
            return 'c'
        else:
            return 'a'

class QuestionBox():
    def __init__(self, game):
        self.game = game
        self.font = game.font
        self.font_bold = game.font_bold
        self.font_bold.set_bold(True)
        self.choose = vec(0, 0)

    def wrap_text(self):
        pass
    
    def get_text(self, mob):
        if MOBS[mob.name]['correct'] == None:
            self.title = f'{mob.name}: {MOBS[mob.name]["question"]}'
            self.question = {q: f'{q.upper()}: {MOBS[mob.name][q]}' for q in 'abcd'}
        else:
            self.title = f'{mob.name}: Már találkoztunk, húzzá má el innét!'
        self.mob = mob
        self.game.stop = True

    def render(self):
        self.surface = pg.Surface((WIDTH, HEIGHT / 10))
        self.surface.fill(TEXTBOX_COLOR)
        self.surface.blit(text_to_surf(self.font, self.title), (3, 0))
        if MOBS[self.mob.name]['correct'] == None:
            self.surface.blit(text_to_surf(self.font if 'a' != vec_to_ans(self.choose) else self.font_bold, self.question['a']), (3, 23 * 1))
            self.surface.blit(text_to_surf(self.font if 'b' != vec_to_ans(self.choose) else self.font_bold, self.question['b']), (WIDTH / 2 + 3, 23 * 1))
            self.surface.blit(text_to_surf(self.font if 'c' != vec_to_ans(self.choose) else self.font_bold, self.question['c']), (3, 23 * 2))
            self.surface.blit(text_to_surf(self.font if 'd' != vec_to_ans(self.choose) else self.font_bold, self.question['d']), (WIDTH / 2 + 3, 23 * 2))

    def apply(self):
        self.render()
        self.game.screen.blit(self.surface, (0, HEIGHT / 10 * 9))

    def get_keys(self):
        pressed = pg.key.get_pressed()
        if MOBS[self.mob.name]['correct'] == None:
            if pressed[pg.K_RETURN]:
                self.game.stop = False
                MOBS[self.mob.name]['correct'] = True if MOBS[self.mob.name]['answer'] == vec_to_ans(self.choose) else False
            elif pressed[pg.K_RIGHT]:
                self.choose.x = 1
            elif pressed[pg.K_LEFT]:
                self.choose.x = 0
            elif pressed[pg.K_DOWN]:
                self.choose.y = 1
            elif pressed[pg.K_UP]:
                self.choose.y = 0
        else:
            if pressed[pg.K_RETURN]:
                self.game.stop = False

class Stats:
    def __init__(self, game):
        self.game = game
        self.font = game.font
        self.font_bold = game.font_bold
        self.font_bold.set_bold(True)
        self.img_star = convert_image(path.join(game.img_folder, STAR_IMG), (30, 30))
        self.img_star_emp = convert_image(path.join(game.img_folder, STAR_EMPTY_IMG), (30, 30))

    def get_stats(self):
        self.stats = dict()
        for commission in {mob['type'] for mob in MOBS.values()}:
            self.stats.update({commission: sum([mob['correct'] for mob in MOBS.values() if mob['type'] == commission and mob['correct'] != None])})
    
    def render(self):
        self.surface = pg.Surface((WIDTH, 5 + len(self.stats.keys()) * 35 + 5))
        self.surface.fill(TEXTBOX_COLOR)
        for row, commission in enumerate(self.stats.keys()):
            self.surface.blit(text_to_surf(self.font, commission), (WIDTH / 2 - 160, 5 + 7 + row * 35))
            for star in range(5):
                if star < self.stats[commission]:
                    self.surface.blit(self.img_star, (WIDTH / 2 - 160 + 150 + star * 35, 5 + row * 35))
                else:
                    self.surface.blit(self.img_star_emp, (WIDTH / 2 - 160 + 150 + star * 35, 5 + row * 35))

    def apply(self):
        self.get_stats()
        self.render()
        self.game.screen.blit(self.surface, (0, HEIGHT * 0.4))

class GameTime:
    def __init__(self, game):
        self.game = game
        self.font = game.font
        self.time = 0
        self.year_width = self.calc_year_width()
        self.month_width = self.calc_month_width()

    def calc_year_width(self):
        return max([text_to_surf(self.font, f'ÉVFOLYAM: {YEARS[year]}').get_width() for year in range(5)])

    def calc_month_width(self):
        return max([text_to_surf(self.font, f'HÓNAP: {MONTHS[month]}').get_width() for month in range(12)])

    def update(self):
        year = int(self.time // (GAMETIME / 5 * 60))
        month = int(self.time / (GAMETIME / 5 * 60) * 12) - ((self.time // (GAMETIME / 5 * 60)) * 12)
        if year > 4:
            self.game.show_end = True
            year = 4
            month = 11
        self.show_year = f'ÉVFOLYAM: {YEARS[year]}'
        self.show_month = f'HÓNAP: {MONTHS[month]}'

    def render(self):
        self.year_surf = pg.Surface((self.year_width + 2, 23))
        self.month_surf = pg.Surface((self.month_width + 2, 23))
        self.year_surf.fill(TEXTBOX_COLOR)
        self.month_surf.fill(TEXTBOX_COLOR)
        self.year_surf.blit(text_to_surf(self.font, self.show_year), (2, 0))
        self.month_surf.blit(text_to_surf(self.font, self.show_month), (2, 0))

    def apply(self):
        self.render()
        self.game.screen.blit(self.year_surf, (0, 0))
        self.game.screen.blit(self.month_surf, (WIDTH - self.month_width - 2, 0))