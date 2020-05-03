import pygame as pg
from bonuses import Bonus
import winsound as ws

class Bullet:
    def __init__(self, settings, pos, move, team, speed, ind = -1):
        self.surf = settings.main_surf
        self.settings = settings

        self.ind = ind

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
        self.break_rect = pg.Rect((self.x - 20, self.y - 20, 40, 40))
        # g = pg.draw.rect(self.surf, (255, 0, 0), self.break_rect, 1)

        res = False

        for k in range(3):
            for block in self.settings.bricks:
                if self.break_rect.clip(block.draw_rect):
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
                # self.settings.past_shoot_audio.play()
                # ws.PlaySound("music/past_shoot.wav", ws.SND_ASYNC)
                self.settings.past_shoot_sound.play()
                self.settings.bangs.append([self.x - self.x_v, self.y - self.y_v, 1, 0, 1])
                return True

        if self.team == 1:
            for bot_el in self.settings.bots:
                if self.check_rect.clip(bot_el.rect) and bot_el.start_counter > bot_el.settings.spawn_time:
                    bot_el.hp -= 1
                    if bot_el.hp == 0:
                        self.settings.bots.pop(self.settings.bots.index(bot_el))
                        self.settings.enemies_left -= 1
                        # self.settings.bot_boom_audio.play()
                        # ws.PlaySound("music/bot_boom.wav", ws.SND_ASYNC)
                        self.settings.bot_boom_sound.play()

                        if not bot_el.blink:
                            self.settings.bonuses.append(Bonus(self.settings))
                            # self.settings.bonus_created_audio.play()
                        self.settings.tanks_bangs.append([bot_el.x + bot_el.size // 2, bot_el.y + bot_el.size // 2, 1, 0, bot_el.bot_cost])
                        self.settings.bangs.append([self.x - self.x_v, self.y - self.y_v, 1, 0, 1])
                        self.settings.enemies_killed[self.ind - 1][bot_el.tank_ind - 2] += 1
                        self.settings.score[self.ind - 1] += bot_el.bot_cost
                    else:
                        # self.settings.bim_audio.play()
                        # ws.PlaySound("music/bim.wav", ws.SND_ASYNC)
                        self.settings.bim_sound.play()
                    return True
        if self.team == 2:
            for tank in self.settings.tanks:
                if self.check_rect.clip(tank.rect):
                    if tank.start_counter > self.settings.spawn_time:
                        tank.death()

            for block in self.settings.fin:
                if self.rect.clip(block.draw_rect):
                    # self.settings.death_audio.play()
                    # ws.PlaySound("music/death.wav", ws.SND_ASYNC)
                    self.settings.death_sound.play()
                    self.settings.enemies_left = 0
                    self.settings.fin.pop(self.settings.fin.index(block))
                    for tank in self.settings.tanks:
                        tank.health = 0
                        
                    self.settings.stop_game = True
                    return True
        return False

    def update(self):
        self.x += self.x_v
        self.y += self.y_v

        self.draw_rect = (self.x - 2 - 2 * abs(self.move[0]), self.y - 2 - 2 * abs(self.move[1]),
                          (2 + abs(self.move[0])) * 2, (2 + abs(self.move[1])) * 2)

        return self.check_coll()
