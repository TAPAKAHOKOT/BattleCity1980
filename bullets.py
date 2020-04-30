import pygame as pg
from bonuses import Bonus
import winsound

class Bullet:
    def __init__(self, settings, pos, move, team, speed):
        self.surf = settings.main_surf
        self.settings = settings

        self.team = team

        self.speed = speed


        self.move = move

        self.x, self.y = pos[0] + self.settings.cells_size // 2 + 5, pos[1] + self.settings.cells_size // 2 + 5
        self.x_v, self.y_v = move[0] * self.speed, move[1] * self.speed

        self.draw_rect = (self.x - 2 - 2 * abs(self.move[0]), self.y - 2 - 2 * abs(self.move[1]),
                          (1 + abs(self.move[0])) * 2, (1 + abs(self.move[1])) * 2)

        self.color = (255, 255, 255)

        self.rect = pg.draw.rect(self.surf, self.color, self.draw_rect)
        self.check_rect = pg.Rect((self.x - 10, self.y - 10, 20, 20))

    def draw(self):
        self.rect = pg.draw.rect(self.surf, self.color, self.draw_rect)

    def check_coll(self):
        self.check_rect = pg.Rect((self.x - 10, self.y - 10, 20, 20))
        # g = pg.draw.rect(self.surf, (255, 0, 0), self.check_rect, 1)

        res = False

        for k in range(2):
            for block in self.settings.bricks:
                if self.check_rect.clip(block.draw_rect):
                    self.settings.bricks.pop(self.settings.bricks.index(block))
                    self.settings.bangs.append([self.x, self.y, 1, 0, 1])
                    res = True

        for bullet in self.settings.bullets:
            if self.check_rect.clip(bullet.check_rect) and self.team != bullet.team:
                self.settings.bullets.pop(self.settings.bullets.index(bullet))
                return True
        if res: return res

        for block in self.settings.armor:
            if self.rect.clip(block.draw_rect):
                winsound.PlaySound("music/past_shoot.wav", winsound.SND_ASYNC)
                self.settings.bangs.append([self.x - self.x_v, self.y - self.y_v, 1, 0, 1])
                return True

        if self.team == 1:
            for bot_el in self.settings.bots:
                if self.check_rect.clip(bot_el.rect):
                    self.settings.bots.pop(self.settings.bots.index(bot_el))
                    self.settings.enemies_left -= 1
                    winsound.PlaySound("music/bot_boom.wav", winsound.SND_ASYNC)
                    if not bot_el.blink:
                        self.settings.bonuses.append(Bonus(self.settings))
                        winsound.PlaySound("music/bonus_created.wav", winsound.SND_ASYNC)
                    self.settings.tanks_bangs.append([bot_el.x + bot_el.size // 2, bot_el.y + bot_el.size // 2, 1, 0, 1])
                    return True
        if self.team == 2:
            for tank in self.settings.tanks:
                if self.check_rect.clip(tank.rect):
                    if tank.start_counter > self.settings.spawn_time:
                        tank.death()
        return False

    def update(self):
        self.x += self.x_v
        self.y += self.y_v

        self.draw_rect = (self.x - 2 - 2 * abs(self.move[0]), self.y - 2 - 2 * abs(self.move[1]),
                          (2 + abs(self.move[0])) * 2, (2 + abs(self.move[1])) * 2)

        return self.check_coll()
