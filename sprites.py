import pygame as pg

from battle import *
from console import *

vec = pg.math.Vector2


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_img
        self.rect = self.image.get_rect()
        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        self.direction = 0
        self.animation_counter = 0
        # initializing animation of player
        self.image_left = ['pokechar_left_1.png', 'pokechar_left_2.png', 'pokechar_left_3.png', 'pokechar_left_4.png']
        self.image_right = ['pokechar_right_1.png', 'pokechar_right_2.png', 'pokechar_right_3.png',
                            'pokechar_right_4.png']
        self.image_up = ['pokechar_up_1.png', 'pokechar_up_2.png', 'pokechar_up_3.png', 'pokechar_up_4.png']
        self.image_down = ['pokechar_down_1.png', 'pokechar_down_2.png', 'pokechar_down_3.png', 'pokechar_down_4.png']
        self.battle = Battle()
        self.encounter_chance = 0

    def get_keys(self):
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vel.x = -PLAYER_SPEED
            self.direction = 1
        elif keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vel.x = PLAYER_SPEED
            self.direction = 2
        elif keys[pg.K_UP] or keys[pg.K_w]:
            self.vel.y = -PLAYER_SPEED
            self.direction = 3
        elif keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel.y = PLAYER_SPEED
            self.direction = 4
        # if self.vel.x != 0 and self.vel.y != 0:
        #   self.vel *= 0.7071
        # print(self.animation_counter)

    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y

    def update(self):
        self.get_keys()
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'Assets')
        # counter used to travel between 4 states of animation png
        self.animation_counter += 1
        if self.animation_counter % 8 == 0:
            self.encounter_chance = random.randint(0, 9)
            # print(self.pos)
        self.animation_counter %= 32
        # Animation update
        # changing player image based on direction and counter
        if self.direction == 1:
            self.image = pg.image.load(path.join(img_folder, self.image_left[int(self.animation_counter / 8)]))
        if self.direction == 2:
            self.image = pg.image.load(path.join(img_folder, self.image_right[int(self.animation_counter / 8)]))
        if self.direction == 3:
            self.image = pg.image.load(path.join(img_folder, self.image_up[int(self.animation_counter / 8)]))
        if self.direction == 4:
            self.image = pg.image.load(path.join(img_folder, self.image_down[int(self.animation_counter / 8)]))

        # check if player is idle
        if self.vel.x == 0 and self.vel.y == 0:
            if self.direction == 1:
                self.image = pg.image.load(path.join(img_folder, 'pokechar_left_1.png')).convert_alpha()
            if self.direction == 2:
                self.image = pg.image.load(path.join(img_folder, 'pokechar_right_1.png')).convert_alpha()
            if self.direction == 3:
                self.image = pg.image.load(path.join(img_folder, 'pokechar_up_1.png')).convert_alpha()
            if self.direction == 4:
                self.image = pg.image.load(path.join(img_folder, 'pokechar_down_1.png')).convert_alpha()
        # print(self.pos)
        self.pos += self.vel * self.game.dt
        self.rect.x = self.pos.x
        self.collide_with_walls('x')
        self.rect.y = self.pos.y
        self.collide_with_walls('y')


# tmx maps obstacle class for collision
class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
