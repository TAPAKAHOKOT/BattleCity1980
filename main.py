import winsound

import pygame as pg
import os
from copy import deepcopy
from settings import Settings
from tanks import Tank
from grass import Grass
from armor import Armor
from bricks import Brick
from fin import  Fin
from water import Water
from bot import Bot
from random import randint as rnd

pg.init()

settings = Settings()
settings.staying_sound.play(loops=-1)

os.environ['SDL_VIDEO_WINDOW_POS'] = '%i,%i' % (-1500, 0)

screen = pg.display.set_mode(settings.win_size, flags=pg.DOUBLEBUF)
surf = pg.Surface(settings.win_size)

settings.screen = screen
settings.main_surf = surf

clock = pg.time.Clock()

file = open("cards", "r")

fd = {}
arr = file.read().split("|")[1:]
glo = []
l = []

for k in range(len(arr)//2):
    fd[arr[k * 2]] = []

    a = []
    for lol in arr[ k * 2 + 1 ].split("\n"):
        bb = []
        for n in lol.split("$"):
            co = []
            if "!" not in n:
                for u in n.split(", "):
                    if u != "":
                        bb.append(int(u))
            else:
                for i in n.split("!"):
                    if i != ", ":
                        r = []
                        for t in i.split(", "):
                            if t != "":
                                r.append(int(t[:1]))
                        if r:
                            co.append(r)
            if co:
                bb.append(co)
        if bb:
            fd[arr[k * 2]].append(bb)
file.close()
settings.levels = deepcopy(fd)

settings.field = deepcopy(settings.levels[str(settings.cur_level)])

def init_game():
    for y, row in enumerate(settings.field):
        for x, column in enumerate(row):
            if column == 1:
                settings.grass.append(Grass(settings.main_surf, settings.field_size, settings.cells_size, (x, y)))
            elif column == 2:
                settings.armor.append(Armor(settings.main_surf, settings.field_size, settings.cells_size, (x, y)))
            elif type(column) is list:

                for add_nums in column:
                    if add_nums[0] == 0:
                        if add_nums[1] % 2 == 0:
                            ind = 0
                        else:
                            ind = 3
                    else:
                        if add_nums[1] % 2 == 0:
                            ind = 2
                        else:
                            ind = 1

                    settings.bricks.append(Brick(settings.main_surf, settings.field_size, settings.cells_size,
                                            (50 + settings.cells_size * x + add_nums[0] * settings.cells_size // 2,
                                            50 + settings.cells_size * y + add_nums[1] * settings.cells_size // 4), ind))
            elif column == 4:
                settings.fin.append(Fin(settings.main_surf, settings.field_size, settings.cells_size, (x, y)))
                settings.fin_pos = (x, y)

            elif column == 5:
                settings.spawns.append([x, y])
            elif column == 6:
                settings.bots_spawn.append([x, y])
            elif column == 7:
                settings.water.append(Water(settings.main_surf, settings.field_size, settings.cells_size, (x, y)))

init_game()

settings.tanks = [Tank(settings, 1), Tank(settings, 2)]


while True:
    settings.main_surf.fill(settings.win_bg)

    clock.tick(settings.win_fps)

    settings.bots_spawn_counter += 1
    settings.main_counter += 1

    if settings.grill:
        for y in range(settings.field_size + 1):
            line = pg.draw.aaline(settings.main_surf, (255, 255, 255), (50, 50 + y * settings.cells_size),
                                      (50 + settings.field_size * settings.cells_size, 50 + y * settings.cells_size))
        for x in range(settings.field_size + 1):
            line = pg.draw.aaline(settings.main_surf, (255, 255, 255), (50 + x * settings.cells_size, 50),
                                      (50 + x * settings.cells_size, 50 + settings.field_size * settings.cells_size))

    ln = pg.draw.rect(settings.main_surf, settings.frame_color, pg.Rect((0, 0, settings.win_width, 50)))
    ln = pg.draw.rect(settings.main_surf, settings.frame_color, pg.Rect((0, settings.win_height - 50, settings.win_width, 50)))

    ln = pg.draw.rect(settings.main_surf, settings.frame_color, pg.Rect((0, 0, 50, settings.win_height)))
    ln = pg.draw.rect(settings.main_surf, settings.frame_color, pg.Rect((settings.win_width - 50, 0, 50, settings.win_height)))

    enemies_counter = 0
    for k in range(settings.enemies_at_level // 2):
        for i in range(2):
            enemies_counter += 1
            if enemies_counter <= settings.enemies_left:
                img = settings.main_surf.blit(settings.mini_tank, (settings.win_width - 45 + i * 20, settings.win_height // 2 - 320 + k * 30))

    if settings.enemies_left == 0:
        settings.enemies_left = settings.enemies_at_level
        settings.cur_level += 1
        settings.field = deepcopy(settings.levels[str(settings.cur_level)])

        settings.bots_spawn_counter = 0
        settings.bots_spawner_speed = 150
        settings.bots_spawned = 0

        settings.spawns = []
        settings.bots_spawn = []

        settings.grass = []
        settings.armor = []
        settings.bricks = []
        settings.fin = []
        settings.bullets = []
        settings.water = []
        settings.bots = []
        settings.bonuses = []
        init_game()

        [tank.respawn() for tank in settings.tanks]


    for block in settings.water:
        block.draw()

    for bullet in settings.bullets:
        if bullet.update():
            settings.bullets.pop(settings.bullets.index(bullet))
        bullet.draw()

        if not 50 < bullet.x < settings.win_width - 50:
            bullet.settings.bangs.append([bullet.x - bullet.x_v, bullet.y - bullet.y_v, 1, 0, 1])
            settings.bullets.pop(settings.bullets.index(bullet))
            if bullet.team == 1:
                winsound.PlaySound("music/past_shoot.wav", winsound.SND_ASYNC)
        if not 50 < bullet.y < settings.win_height - 50:
            settings.bullets.pop(settings.bullets.index(bullet))
            bullet.settings.bangs.append([bullet.x - bullet.x_v, bullet.y - bullet.y_v, 1, 0, 1])
            if bullet.team == 1:
                winsound.PlaySound("music/past_shoot.wav", winsound.SND_ASYNC)

    for tank in settings.tanks:
        tank.update()
        tank.draw()

        for bonus in settings.bonuses:
            if tank.rect.clip(bonus.rect):
                bonus.badums(tank.ind)
                settings.bonuses.pop(settings.bonuses.index(bonus))
            if bonus.blink_speed == 1:
                settings.bonuses.pop(settings.bonuses.index(bonus))

    for bot_el in settings.bots:
        if bot_el.start_counter >= settings.spawn_time and settings.stop_interval < settings.main_counter:
            bot_el.update()
        if settings.stop_interval > settings.main_counter:
            if settings.main_counter % 4 // 2 == 1:
                bot_el.draw()
        else:
            bot_el.draw()

    for bonus in settings.bonuses:
        bonus.draw()

    if (settings.bots_spawn_counter % settings.bots_spawner_speed == 0
            and settings.bots_spawned < settings.enemies_at_level) or settings.bots_spawn_counter == 5:
        settings.bots.append(Bot(settings))
        settings.bots_spawner_speed -= 5
        settings.bots_spawned += 1

    for block in settings.armor:
        block.draw()



    anim_speed = 3

    for bang in settings.bangs:

        settings.main_surf.blit(settings.booms[bang[2] - 1], (bang[0] - settings.cells_size, bang[1] - settings.cells_size))

        bang[3] += 1
        if bang[3] % anim_speed == 0:
            bang[2] += 1

        if bang[3] == anim_speed * 6 + 3:
            settings.bangs.pop(settings.bangs.index(bang))

    for bang in settings.tanks_bangs:
        settings.main_surf.blit(settings.big_booms[bang[2] - 1],
                                (bang[0] - settings.cells_size * 2, bang[1] - settings.cells_size * 2))

        bang[3] += 1
        if bang[3] % anim_speed == 0:
            bang[2] += 1

        if bang[3] == anim_speed * 6 + 3:
            settings.tanks_bangs.pop(settings.tanks_bangs.index(bang))

    for block in settings.grass:
        block.draw()

    for block in settings.bricks:
        block.draw()

    for block in settings.fin:
        block.draw()

    text = settings.hpfont.render(f"I P", True, (0, 0, 0))
    settings.main_surf.blit(text, text.get_rect(center=(settings.win_width - 25, settings.win_height // 2 - 70)))
    text = settings.hpfont.render(f"{settings.tanks[0].health}", True, (0, 0, 0))
    settings.main_surf.blit(text, text.get_rect(center=(settings.win_width - 25, settings.win_height // 2 -30)))


    text = settings.hpfont.render(f"II P", True, (0, 0, 0))
    settings.main_surf.blit(text, text.get_rect(center=(settings.win_width - 25, settings.win_height // 2 + 30)))
    text = settings.hpfont.render(f"{settings.tanks[1].health}", True, (0, 0, 0))
    settings.main_surf.blit(text, text.get_rect(center=(settings.win_width - 25, settings.win_height // 2 + 70)))

    settings.screen.blit(settings.main_surf, (0, 0))

    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if event.key == 27:
                print("<<< EXIT >>>")
                exit()

            if event.key in [97, 100, 115, 119]:
                settings.moving_sound.play(loops=-1)
                settings.staying_sound.stop()

            if event.key == 119:
                settings.tanks[0].move = [0, 0, 0, 1]
                # print("Up")
            if event.key == 115:
                settings.tanks[0].move = [0, 0, 1, 0]
                # print("Down")
            if event.key == 97:
                settings.tanks[0].move = [0, 1, 0, 0]
                # print("Left")
            if event.key == 100:
                settings.tanks[0].move = [1, 0, 0, 0]
                # print("Right")
            if event.key == 101:
                settings.tanks[0].fire()

            if event.key == 116:
                settings.tanks[1].move = [0, 0, 0, 1]
                # print("Up")
            if event.key == 103:
                settings.tanks[1].move = [0, 0, 1, 0]
                # print("Down")
            if event.key == 102:
               settings.tanks[1].move = [0, 1, 0, 0]
                # print("Left")
            if event.key == 104:
                settings.tanks[1].move = [1, 0, 0, 0]
                # print("Right")
            if event.key == 121:
                settings.tanks[1].fire()

        elif event.type == pg.KEYUP:
            if event.key in [97, 100, 115, 119]:
                settings.tanks[0].move = [0, 0, 0, 0]

                settings.staying_sound.play(loops=-1)
                settings.moving_sound.stop()

            if event.key in [102, 103, 104, 116]:
                settings.tanks[1].move = [0, 0, 0, 0]

    pg.display.update()




