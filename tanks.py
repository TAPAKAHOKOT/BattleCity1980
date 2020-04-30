import pygame as pg
from random import randint as rnd
from bullets import Bullet
import winsound

class Tank:
    def __init__(self, settings, ind):
        self.settings = settings

        self.x, self.y = self.settings.spawns[ind - 1]
        self.ind = ind

        self.tank_level = 1

        self.x, self.y = 50 + self.settings.cells_size * self.x - int(self.settings.cells_size * 1.3) // 2, \
                         50 + self.settings.cells_size * self.y - int(self.settings.cells_size * 1.3) // 2

        self.move = [0, 0, 0, 0]
        self.ind = ind

        self.health = 3

        self.speed = self.settings.tanks_speed[self.tank_level - 1]

        self.color = (rnd(0, 255), rnd(0, 255), rnd(0, 255))

        self.size = int(self.settings.cells_size * 1.3)

        self.main_img = pg.transform.scale(pg.image.load(f"images/tanks/good/tank{self.tank_level}{ind}.png"),
                                           (self.size, self.size))

        self.draw_img = self.main_img
        self.moving = False

        self.bullet_move = [0, -1]
        self.fire_rate = self.settings.tanks_fire_rate[self.tank_level - 1]
        self.counter = 0
        self.start_counter = 0
        self.def_counter = 100
        self.main_counter = 0

        self.def_img = []
        self.defeat_on = True
        for k in range(1, 5):
            self.def_img.append(pg.transform.scale(pg.image.load(f"images/def/def{k}.png"),
                                                   (int(self.size * 1.6), int(self.size * 1.7))))

        self.flicks = []
        for k in range(1, 5):
            self.flicks.append(pg.transform.scale(pg.image.load(f"images/flicks/flick{k}.png"), (self.size, self.size)))
        self.draw_flick = 0
        self.flick_add = 1

        self.rect = pg.Rect( (self.x, self.y,
                             int(self.settings.cells_size * 1.3), int(self.settings.cells_size * 1.3)))

    def draw(self):
        # self.rect = pg.draw.circle(self.settings.main_surf, self.color,
        #                            (self.x, self.y), self.settings.cells_size // 2, 1)
        if self.start_counter > self.settings.spawn_time:
            self.img = self.settings.main_surf.blit(self.draw_img, (self.x, self.y))

        else:
            self.start_counter += 1
            self.draw_flick += self.flick_add
            if self.draw_flick == 3:
                self.flick_add = -1
            if self.draw_flick == 0:
                self.flick_add = 1

            self.img = self.settings.main_surf.blit(self.flicks[self.draw_flick % 4], (self.x, self.y))

    def add_level(self):
        if self.tank_level < 4:
            self.tank_level += 1

            self.main_img = pg.transform.scale(pg.image.load(f"images/tanks/good/tank{self.tank_level}{self.ind}.png"),
                                               (self.size, self.size))
    def add_hp(self):
        if self.health < 3:
            self.health += 1

    def test_to_move(self, step):
        res =  (40 < (self.x + step[0]) < self.settings.win_width - 75) and\
               (40 < (self.y + step[1]) < self.settings.win_height - 75)


        self.test_rect = pg.Rect((self.x + step[0] + 5, self.y + step[1] + 5, self.size - 10, self.size - 10))

        # test = pg.draw.rect(self.settings.main_surf, (255, 0, 0), self.test_rect, 1)


        if res:
            for block in self.settings.armor:
                if self.test_rect.clip(block.draw_rect):
                    res = False
                    break
        if res:
            for block in self.settings.bricks:
                if self.test_rect.clip(block.draw_rect):
                    res = False
                    break
        if res:
            for block in self.settings.water:
                if self.test_rect.clip(block.draw_rect):
                    res = False
                    break
        return res
    def fire(self):

        if self.counter > self.fire_rate and self.start_counter > self.settings.spawn_time:
            winsound.PlaySound("music/fire.wav", winsound.SND_ASYNC)

            self.settings.bullets.append(Bullet(self.settings, (self.x, self.y), self.bullet_move, 1,
                                                self.settings.tanks_bullets_speed[self.tank_level - 1]))
            self.counter = 0

    def death(self):
        if not self.defeat_on:
            winsound.PlaySound("music/death.wav", winsound.SND_ASYNC)

            self.health -= 1

            self.x, self.y = self.settings.spawns[self.ind - 1]

            self.x, self.y = 50 + self.settings.cells_size * self.x - int(self.settings.cells_size * 1.3) // 2, \
                             50 + self.settings.cells_size * self.y - int(self.settings.cells_size * 1.3) // 2
            self.start_counter = 0

            self.def_counter = self.main_counter + 60
            self.defeat_on = True

    def respawn(self):
        self.x, self.y = self.settings.spawns[self.ind - 1]

        self.x, self.y = 50 + self.settings.cells_size * self.x - int(self.settings.cells_size * 1.3) // 2, \
                         50 + self.settings.cells_size * self.y - int(self.settings.cells_size * 1.3) // 2
        self.start_counter = 0

        self.def_counter = self.main_counter + 60
        self.defeat_on = True

    def defeat(self):
        if self.main_counter < self.def_counter:
            self.defeat_on = True

            img = self.settings.main_surf.blit(self.def_img[self.counter % 4], (self.x - self.size // 2 + 2, self.y - self.size // 2 + 5))
        else:
            self.defeat_on = False

    def update(self):
        if self.start_counter > self.settings.spawn_time:

            self.counter += 1
            self.main_counter += 1

            if self.defeat_on:
                self.defeat()

            if self.move[0] == 1:
                self.draw_img = pg.transform.rotate(self.main_img, -90)
                self.bullet_move = [1, 0]
                if self.test_to_move([10, 0]):
                    self.x += self.speed
            if self.move[1] == 1:
                self.draw_img = pg.transform.rotate(self.main_img, 90)
                self.bullet_move = [-1, 0]
                if self.test_to_move([-10, 0]):
                    self.x -= self.speed

            if self.move[2] == 1:
                self.draw_img = pg.transform.rotate(self.main_img, 180)
                self.bullet_move = [0, 1]
                if self.test_to_move([0, 10]):
                    self.y += self.speed
            if self.move[3] == 1:
                self.draw_img = self.main_img
                self.bullet_move = [0, -1]
                if self.test_to_move([0, -10]):
                    self.y -= self.speed

            self.rect = pg.Rect((self.x, self.y, self.size, self.size))
            # t = pg.draw.rect(self.settings.main_surf, (255, 0, 0), self.rect, 1)
