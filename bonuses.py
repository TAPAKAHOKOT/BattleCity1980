import winsound

from pygame import transform, image, Rect
from random import randint as rnd


class Bonus:
    def __init__(self, settings):
        self.settings = settings

        self.x, self.y = rnd(100, self.settings.win_width - 100), rnd(100, self.settings.win_width - 100)

        self.rect = Rect((self.x, self.y, self.settings.cells_size * 2, self.settings.cells_size * 2))

        self.bonus_index = rnd(1, 6)

        self.image = transform.scale(image.load(f"images/bonuses/bonus{self.bonus_index}.png"),
                                     (self.settings.cells_size * 2, self.settings.cells_size * 2))

        self.counter = 0
        self.counter_up = -1

        self.blink_speed = 15
        self.blink_counter = 0

    def draw(self):
        self.blink_counter += 1
        self.counter -= self.counter_up

        if self.counter % 5 == 0:
            self.y += self.counter_up
        if self.counter == 30 or self.counter == 0:
            self.counter_up *= -1

        if self.blink_counter >= 60:

            if self.counter % self.blink_speed != 0:
                self.img = self.settings.main_surf.blit(self.image, (int(self.x), int(self.y)))
        else:
            self.img = self.settings.main_surf.blit(self.image, (int(self.x), int(self.y)))

        if self.blink_counter % 30 == 0:
            self.blink_speed -= 1




    def badums(self, tank_ind):

        if self.bonus_index == 1:
            # Get armor
            winsound.PlaySound("music/bomb_bonus.wav", winsound.SND_ASYNC)
            self.settings.tanks[tank_ind - 1].def_counter = self.settings.tanks[tank_ind - 1].counter + 100
            self.settings.tanks[tank_ind - 1].defeat_on = True

        if self.bonus_index == 2:
            # Stop time
            winsound.PlaySound("music/bomb_bonus.wav", winsound.SND_ASYNC)
            self.settings.stop_interval = self.settings.main_counter + 80

        if self.bonus_index == 3:
            # Get armor for spawn
            winsound.PlaySound("music/bomb_bonus.wav", winsound.SND_ASYNC)
            pass

        if self.bonus_index == 4:
            # Get lvl
            winsound.PlaySound("music/bomb_bonus.wav", winsound.SND_ASYNC)
            self.settings.tanks[tank_ind - 1].add_level()

        if self.bonus_index == 5:
            # Bomb all enemies
            winsound.PlaySound("music/bomb_bonus.wav", winsound.SND_ASYNC)

            for bot_el in self.settings.bots:
                winsound.PlaySound("music/bot_boom.wav", winsound.SND_ASYNC)
                self.settings.tanks_bangs.append([bot_el.x + bot_el.size // 2, bot_el.y + bot_el.size // 2, 1, 0, 1])
            self.settings.bots = []

        if self.bonus_index == 6:
            # Get hp
            winsound.PlaySound("music/health_bonus.wav", winsound.SND_ASYNC)
            self.settings.tanks[tank_ind - 1].add_hp()

        if self.bonus_index == 7:
            # Get 3 lvls
            self.settings.tanks[tank_ind - 1].add_level()
            self.settings.tanks[tank_ind - 1].add_level()
            self.settings.tanks[tank_ind - 1].add_level()
