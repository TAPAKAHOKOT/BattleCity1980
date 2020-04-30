import pygame as pg
from random import randint as rnd
from bullets import Bullet
from random import choice
from random import randint as rnd
from random import choice


class Bot:
    def __init__(self, settings):
        self.settings = settings

        self.size = (int(self.settings.cells_size * 1.3))
        self.id = rnd(1000000, 9999999)

        while True:
            self.x, self.y = choice(self.settings.bots_spawn)

            self.x, self.y = 50 + self.x * self.settings.cells_size, 50 + self.y * self.settings.cells_size

            if self.test_to_move([0, 0]):
                break

        self.move = [0, 0, 0, 0]
        self.angle = 0

        self.speed = 5

        self.color = (rnd(0, 255), rnd(0, 255), rnd(0, 255))

        self.flicks = []
        for k in range(1, 5):
            self.flicks.append(pg.transform.scale(pg.image.load(f"images/flicks/flick{k}.png"), (self.size, self.size)))
        self.draw_flick = 0
        self.flick_add = 1

        tank_ind = rnd(1, 5)
        self.main_imgs = [pg.transform.scale(pg.image.load(f"images/tanks/bad/tank{tank_ind}{3}.png"), (self.size, self.size)),
                          pg.transform.scale(pg.image.load(f"images/tanks/bad/tank{tank_ind}{4}.png"), (self.size, self.size)) ]

        self.blink = not rnd(0, 6) == 3
        self.draw_img = self.main_imgs[0]

        self.counter = 0
        self.start_counter = 0

        self.bullet_move = [0, -1]
        self.fire_rate = 20

        self.rect = pg.Rect( (self.x, self.y, self.size, self.size))

        self.fin_pos = 50 + self.settings.fin_pos[0] * self.settings.cells_size, \
                       50 + self.settings.fin_pos[1] * self.settings.cells_size

        if abs(self.fin_pos[0] - self.x) > abs(self.fin_pos[1] - self.y):
            if self.fin_pos[0] > self.x:
                self.move = [1, 0, 0, 0]
            else:
                self.move = [0, 1, 0, 0]
        else:
            if self.fin_pos[1] > self.y:
                self.move = [0, 0, 1, 0]
            else:
                self.move = [0, 0, 0, 1]

    def draw(self):
        if self.start_counter > self.settings.spawn_time:

            if self.blink:
                t = 1
            else:
                t = 0 if self.counter % 8 < 4 else 1

            self.draw_img = pg.transform.rotate(self.main_imgs[t], self.angle)
            self.img = self.settings.main_surf.blit(self.draw_img, (self.x, self.y))
        else:
            self.start_counter += 1
            self.draw_flick += self.flick_add
            if self.draw_flick == 7:
                self.flick_add = -1
            if self.draw_flick == 0:
                self.flick_add = 1

            self.img = self.settings.main_surf.blit(self.flicks[self.draw_flick % 4], (self.x, self.y))

    def test_to_move(self, step):
        res =  (50 < (self.x + step[0]) < self.settings.win_width - 90) and\
               (50 < (self.y + step[1]) < self.settings.win_height - 90)

        self.test_rect = pg.Rect((self.x + step[0] // 2, self.y + step[1] // 2, self.size, self.size))

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
        if res:
            for bot_el in self.settings.bots:
                if self.test_rect.clip(bot_el.rect) and bot_el.id != self.id:
                    res = False
                    break
        return res
    def fire(self):
        if self.counter > self.fire_rate:
            self.settings.bullets.append(Bullet(self.settings, (self.x, self.y), self.bullet_move, 2, 10))
            self.counter = 0

    def chose_side(self):

        if self.move[0] + self.move[1] == 1:
            if abs(self.fin_pos[0] - self.x) < 50:
                if self.fin_pos[1] > self.y:
                    self.move = [0, 0, 1, 0]
                else:
                    self.move = [0, 0, 0, 1]
        else:
            if abs(self.fin_pos[1] - self.y) < 50:
                if self.fin_pos[0] > self.x:
                    self.move = [1, 0, 0, 0]
                else:
                    self.move = [0, 1, 0, 0]

    def change_side(self):
        if self.move[0] + self.move[1] == 1:
            if self.fin_pos[1] > self.y:
                self.move = [0, 0, 1, 0]
                self.angle = 180
                self.bullet_move = [0, 1]
            else:
                self.move = [0, 0, 0, 1]
                self.angle = 0
                self.bullet_move = [0, -1]
        else:
            if self.fin_pos[0] > self.x:
                self.move = [1, 0, 0, 0]
                self.angle = -90
                self.bullet_move = [1, 0]
            else:
                self.move = [0, 1, 0, 0]
                self.angle = 90
                self.bullet_move = [-1, 0]

    def update(self):

        self.counter += 1

        if rnd(2, 8) == 3:
            self.chose_side()

        if self.fin_pos[0] - 50 <= self.x <= self.fin_pos[0] + 50:
            self.fire()

        elif self.fin_pos[1] - 50 <= self.y <= self.fin_pos[1] + 50:
            self.fire()

        for tank in self.settings.tanks:
            if tank.x - 50 <= self.x <= tank.x + 50:
                self.fire()

            elif tank.y - 50 <= self.y <= tank.y + 50:
                self.fire()

        if self.move[0] == 1:
            self.angle = -90
            self.bullet_move = [1, 0]
            if self.test_to_move([10, 0]):
                self.x += self.speed
            else:
                # self.change_side()
                if rnd(0, self.fire_rate) == 3:
                    self.fire()

                self.move = choice([[0, 0, 1, 0], [0, 0, 0, 1]])

        if self.move[1] == 1:
            self.angle = 90
            self.bullet_move = [-1, 0]
            if self.test_to_move([-10, 0]):
                self.x -= self.speed
            else:
                # self.change_side()
                if rnd(0, self.fire_rate) == 3:
                    self.fire()

                self.move = choice([[0, 0, 1, 0], [0, 0, 0, 1]])

        if self.move[2] == 1:
            self.angle = 180
            self.bullet_move = [0, 1]
            if self.test_to_move([0, 10]):
                self.y += self.speed
            else:
                # self.change_side()
                if rnd(0, self.fire_rate) == 3:
                    self.fire()

                self.move = choice([[1, 0, 0, 0], [0, 1, 0, 0]])

        if self.move[3] == 1:
            self.angle = 0
            self.bullet_move = [0, -1]
            if self.test_to_move([0, -10]):
                self.y -= self.speed
            else:
                # self.change_side()
                if rnd(0, self.fire_rate) == 3:
                    self.fire()

                self.move = choice([[1, 0, 0, 0], [0, 1, 0, 0]])

        self.rect = pg.Rect((self.x, self.y, self.size, self.size))
        # g = pg.draw.rect(self.settings.main_surf, (255, 0, 0), self.rect, 1)