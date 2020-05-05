
from pygame import transform, image, Rect
from random import randint as rnd, choice

class Bonus:
    def __init__(self, settings):
        self.settings = settings

        self.x, self.y = rnd(100, self.settings.win_width - 100), rnd(100, self.settings.win_width - 100)

        self.rect = Rect((self.x, self.y, self.settings.cells_size * 2, self.settings.cells_size * 2))

        # self.bonus_index = choice([1, 2, 4, 5, 6])
        if rnd(0, 3) == 3:
            self.bonus_index = choice([4, 5])
        else:
            self.bonus_index = choice([1, 2, 6])

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
            # self.settings.bonus_audio.play()
            # ws.PlaySound("music/bomb_bonus.wav", ws.SND_ASYNC)
            self.settings.bonus_sound.play()
            self.settings.tanks[tank_ind - 1].def_counter = self.settings.tanks[tank_ind - 1].main_counter + 140
            self.settings.tanks[tank_ind - 1].defeat_on = True
            print(1)

        if self.bonus_index == 2:
            # Stop time
            # self.settings.bonus_audio.play()
            # ws.PlaySound("music/bomb_bonus.wav", ws.SND_ASYNC)
            self.settings.bonus_sound.play()
            self.settings.stop_interval = self.settings.main_counter + 140

        if self.bonus_index == 3:
            # Get armor for spawn
            # self.settings.bonus_audio.play()
            # ws.PlaySound("music/bomb_bonus.wav", ws.SND_ASYNC)
            self.settings.bonus_sound.play()

        if self.bonus_index == 4:
            # Get lvl
            # self.settings.bonus_audio.play()
            # ws.PlaySound("music/bomb_bonus.wav", ws.SND_ASYNC)
            self.settings.bonus_sound.play()
            self.settings.tanks[tank_ind - 1].add_level()

        if self.bonus_index == 5:
            # Bomb all enemies
            # self.settings.bonus_audio.play()
            # ws.PlaySound("music/bomb_bonus.wav", ws.SND_ASYNC)
            self.settings.bonus_sound.play()
            self.settings.enemies_left -= len(self.settings.bots)

            score_to_add = 0
            for bot_el in self.settings.bots:
                # self.settings.bot_boom_audio.play()
                # ws.PlaySound("music/bot_boom.wav", ws.SND_ASYNC)
                self.settings.bot_boom_sound.play()
                self.settings.tanks_bangs.append([bot_el.x + bot_el.size // 2, bot_el.y + bot_el.size // 2, 1, 0, bot_el.bot_cost])
                score_to_add += bot_el.bot_cost

                if not bot_el.blink:
                    self.settings.bonuses.append(Bonus(self.settings))

            self.settings.score[0] += score_to_add // 2
            self.settings.score[1] += score_to_add // 2

            self.settings.bots = []

        if self.bonus_index == 6:
            # Get hp
            # self.settings.hp_bonus_audio.play()
            # ws.PlaySound("music/health_bonus.wav", ws.SND_ASYNC)
            self.settings.hp_bonus_sound.play()
            self.settings.tanks[tank_ind - 1].add_hp()

        if self.bonus_index == 7:
            # Get 3 lvls
            self.settings.tanks[tank_ind - 1].add_level()
            self.settings.tanks[tank_ind - 1].add_level()
            self.settings.tanks[tank_ind - 1].add_level()
