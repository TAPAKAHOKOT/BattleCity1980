
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
import keyboard as kb
from threading import Thread
import winsound as ws



pg.init()
pg.display.init()


joystick_num = pg.joystick.get_count()

js_1 = pg.joystick.Joystick(0)
js_1.init()

if joystick_num > 1:
    js_0 = pg.joystick.Joystick(1)
    js_0.init()

settings = Settings()
settings.staying_sound.play(loops=-1)

os.environ['SDL_VIDEO_WINDOW_POS'] = '%i,%i' % (500, -30)

screen = pg.display.set_mode((1920, 1080), flags=pg.DOUBLEBUF | pg.FULLSCREEN)
surf = pg.Surface((1920, 1080))

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
                settings.fin_pos.append([x, y])

            elif column == 5:
                settings.spawns.append([x, y])
            elif column == 6:
                settings.bots_spawn.append([x, y])
            elif column == 7:
                settings.water.append(Water(settings.main_surf, settings.field_size, settings.cells_size, (x, y)))

init_game()


def new_level():
    if settings.cur_level > settings.levels_num:
        settings.field = deepcopy((settings.levels[str( (settings.cur_level - 1) % (settings.levels_num - 1) + 1)]))
    else:
        settings.field = deepcopy((settings.levels[str((settings.cur_level - 1) % settings.levels_num + 1)]))

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


    big_bot = settings.cur_level // 3.5
    small_bot = rnd(0, 20 - big_bot)
    medium_bot = rnd(0, 20 - big_bot - small_bot)
    third_bot = 20 - big_bot - small_bot - medium_bot

    settings.bots_nums = [small_bot, medium_bot, third_bot, big_bot]

    [tank.respawn() for tank in settings.tanks]

def show_score():
    settings.main_surf.fill(settings.win_bg)

    text = settings.score_font.render(f"STAGE {settings.cur_level}", True, (255, 255, 255))
    settings.main_surf.blit(text, text.get_rect(center=(settings.win_width // 2, 100)))

    record_file = open("record", "r")
    score = int(record_file.read())
    record_file.close()

    if settings.score[0] + settings.score[1] > score:
        file = open("record", "w")
        file.write(str(settings.score[0] + settings.score[1]))
        file.close()

    file = open("record", "r")
    score = file.read()
    file.close()

    text = settings.score_font.render(f"BEST SCORE {score}", True, (255, 255, 150))
    settings.main_surf.blit(text, text.get_rect(center=(settings.win_width // 2, 150)))

    text = settings.score_font.render(f"I-PLAYER", True, (220, 60, 0))
    settings.main_surf.blit(text, text.get_rect(topright=(settings.win_width // 2 - 140, 200)))

    if joystick_num > 1:
        text = settings.score_font.render(f"II-PLAYER", True, (220, 60, 0))
        settings.main_surf.blit(text, text.get_rect(topleft=(settings.win_width // 2 + 140, 200)))


    text = settings.score_font.render(f"SCORE", True, (220, 60, 0))
    settings.main_surf.blit(text, text.get_rect(center=(settings.win_width // 2, 320)))

    text = settings.score_font.render(f"{settings.score[0]}", True, (255, 255, 255))
    settings.main_surf.blit(text, text.get_rect(topright=(settings.win_width // 2 - 140, 305)))

    if joystick_num > 1:
        text = settings.score_font.render(f"{settings.score[1]}", True, (255, 255, 255))
        settings.main_surf.blit(text, text.get_rect(topleft=(settings.win_width // 2 + 140, 305)))


    for k in range(4):
        a_img = surf.blit(settings.bots_imgs[k], (settings.win_width // 2 - settings.cells_size * 1.5 // 2, 400 + k * 100))

        text = settings.score_font.render( f"PTS", True, (255, 255, 255))
        settings.main_surf.blit(text, text.get_rect(center=(settings.win_width // 2 - 180, 440 + k * 100)))

        if joystick_num > 1:
            settings.main_surf.blit(text, text.get_rect(center=(settings.win_width // 2 + 180, 440 + k * 100)))

        if settings.killed[0][k] != -1:
            text = settings.score_font.render(f"{settings.killed[0][k]}", True, (255, 255, 255))
            settings.main_surf.blit(text, text.get_rect(center=(settings.win_width // 2 - 80, 440 + k * 100)))

            text = settings.score_font.render(f"{settings.killed[0][k] * settings.bots_costs[k]}", True, (255, 255, 255))
            settings.main_surf.blit(text, text.get_rect(topright=(settings.win_width // 2 - 280, 420 + k * 100)))

        if settings.killed[1][k] != -1 and joystick_num > 1:
            text = settings.score_font.render(f"{settings.killed[1][k]}", True, (255, 255, 255))
            settings.main_surf.blit(text, text.get_rect(center=(settings.win_width // 2 + 80, 440 + k * 100)))

            text = settings.score_font.render(f"{settings.killed[1][k] * settings.bots_costs[k]}", True, (255, 255, 255))
            settings.main_surf.blit(text, text.get_rect(topleft=(settings.win_width // 2 + 280, 420 + k * 100)))

    pg.draw.line(settings.main_surf, (255, 255, 255), (settings.win_width // 2 - 300, 800),
                 (settings.win_width // 2 + 300, 800), 3)

    text = settings.score_font.render(f"Total", True, (255, 255, 255))
    settings.main_surf.blit(text, text.get_rect(topright=(settings.win_width // 2 - 140, 830)))

    if joystick_num > 1:
        settings.main_surf.blit(text, text.get_rect(topleft=(settings.win_width // 2 + 140, 830)))


    if settings.main_counter % 4 == 0 and settings.p < 4:
        # settings.blink_audio.play()
        ws.PlaySound("music/blink.wav", ws.SND_ASYNC)
        # settings.blink_sound.play()

        t = True
        if settings.killed[0][settings.p] < settings.enemies_killed[0][settings.p]:
            settings.killed[0][settings.p] += 1
            t = False

        if settings.killed[1][settings.p] < settings.enemies_killed[1][settings.p]:
            settings.killed[1][settings.p] += 1
            t = False
        if t:
            settings.p += 1

    if settings.p == 4:

        text = settings.score_font.render(f"{sum(settings.enemies_killed[0])}", True, (255, 255, 255))
        settings.main_surf.blit(text, text.get_rect(topright=(settings.win_width // 2 - 80, 830)))

        if joystick_num > 1:
            text = settings.score_font.render(f"{sum(settings.enemies_killed[1])}", True, (255, 255, 255))
            settings.main_surf.blit(text, text.get_rect(topleft=(settings.win_width // 2 + 80, 830)))


def show_stage():
    if settings.stage_up:
        show_score()

    stage_rect = pg.Rect((0, 0, settings.win_width, settings.stage_up_pos))
    pg.draw.rect(settings.main_surf, (55, 55, 55), stage_rect)

    stage_rect = pg.Rect((0, settings.win_height, settings.win_width, -settings.stage_up_pos))
    pg.draw.rect(settings.main_surf, (55, 55, 55), stage_rect)

    if settings.stage_up_pos < settings.win_height // 2:
        settings.stage_up_pos += settings.win_height // 40
    else:
        settings.stage_up_pos = settings.win_height // 2

    if settings.stage_up_pos == settings.win_height // 2:
        text = settings.score_font.render(f"STAGE {settings.cur_level}", True, (255, 255, 255))
        settings.main_surf.blit(text, text.get_rect(center=(settings.win_width // 2, settings.win_height // 2)))

    if -settings.main_counter + settings.start_storage_show == 40:
        new_level()

    if settings.main_counter >= settings.start_storage_show - 20:
        settings.stage_up = False

    if not settings.stage_up:
        settings.stage_up_pos -= settings.win_height // 20

if joystick_num > 1:
    settings.tanks = [Tank(settings, 1), Tank(settings, 2)]
else:
    settings.tanks = [Tank(settings, 1)]

pg.mouse.set_pos(-100, 0)

while settings.run_game:
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
                img = settings.main_surf.blit(settings.mini_tank, (settings.win_width - 46 + i * 20, settings.win_height // 2 - 450 + k * 30))

    for block in settings.water:
        block.draw()

    for bullet in settings.bullets:
        if bullet.update():
            settings.bullets.pop(settings.bullets.index(bullet))
        bullet.draw()

        if not 50 < bullet.x < settings.win_width - 50:
            bullet.settings.bangs.append([bullet.x - bullet.x_v, bullet.y - bullet.y_v, 1, 0, 1])
            try:
                settings.bullets.pop(settings.bullets.index(bullet))
            except: pass
            if bullet.team == 1:
                # settings.past_shoot_audio.play()
                # ws.PlaySound("music/past_shoot.wav", ws.SND_ASYNC)
                settings.past_shoot_sound.play()

        if not 50 < bullet.y < settings.win_height - 50:
            try:
                settings.bullets.pop(settings.bullets.index(bullet))
            except: pass
            bullet.settings.bangs.append([bullet.x - bullet.x_v, bullet.y - bullet.y_v, 1, 0, 1])
            if bullet.team == 1:
                # settings.past_shoot_audio.play()
                #  ws.PlaySound("music/past_shoot.wav", ws.SND_ASYNC)
                settings.past_shoot_sound.play()
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

    if (settings.bots_spawn_counter % settings.bots_spawner_speed == 0
            and settings.bots_spawned < settings.enemies_at_level) or settings.bots_spawn_counter == 5:

        while True:
            bot_index = rnd(0, 3)
            if settings.bots_nums[bot_index] != 0:
                break
        settings.bots_nums[bot_index] -= 1
        settings.bots.append(Bot(settings, bot_index))

        settings.bots_spawner_speed -= 3
        settings.bots_spawned += 1

    for block in settings.armor:
        block.draw()


    hp = 0
    for tank in settings.tanks:
        hp += tank.health
    if (hp) == 0 and settings.enemies_left != 0:
        settings.enemies_left = 0
        settings.cur_level = 0
        settings.stop_game = True

    anim_speed = 3

    for bang in settings.bangs:
        settings.main_surf.blit(settings.booms[bang[2] - 1],
                                (bang[0] - settings.cells_size, bang[1] - settings.cells_size))

        bang[3] += 1
        if bang[3] % anim_speed == 0:
            bang[2] += 1

        if bang[3] == anim_speed * 6 + 3:
            settings.bangs.pop(settings.bangs.index(bang))

    for bang in settings.tanks_bangs:

        settings.main_surf.blit(settings.big_booms[bang[2] - 1],
                                (bang[0] - settings.cells_size * 2, bang[1] - settings.cells_size * 2))

        if bang[4]:
            text = settings.points_font.render(f"{bang[4]}", True, (255, 255, 255))

            test_surf = pg.Surface(text.get_size(), pg.SRCALPHA)
            test_surf.fill((255, 255, 255, int(255 * ((20 - bang[3]) / 20))))

            text.blit(test_surf, (0, 0), special_flags=pg.BLEND_RGBA_MULT)

            settings.main_surf.blit(text, text.get_rect(center=(bang[0], bang[1] - bang[3])))

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

    for bonus in settings.bonuses:
        bonus.draw()

    text = settings.hpfont.render(f"I P", True, (0, 0, 0))
    settings.main_surf.blit(text, text.get_rect(center=(settings.win_width - 25, settings.win_height // 2 - 60)))
    text = settings.hpfont.render(f"{settings.tanks[0].health}", True, (0, 0, 0))
    settings.main_surf.blit(text, text.get_rect(center=(settings.win_width - 25, settings.win_height // 2 -30)))

    if joystick_num > 1:
        text = settings.hpfont.render(f"II P", True, (0, 0, 0))
        settings.main_surf.blit(text, text.get_rect(center=(settings.win_width - 25, settings.win_height // 2 + 30)))
        text = settings.hpfont.render(f"{settings.tanks[1].health}", True, (0, 0, 0))
        settings.main_surf.blit(text, text.get_rect(center=(settings.win_width - 25, settings.win_height // 2 + 60)))


    if settings.enemies_left == 0:
        if settings.end_level_wait == 0:

            settings.start_score_show = settings.main_counter
            settings.end_level_wait = settings.main_counter + 180
        if settings.main_counter > settings.end_level_wait:
            if settings.start_storage_show == 0:
                if settings.stop_game:

                    kb.wait("enter")
                    settings.run_game = False

                else:
                    settings.start_storage_show = settings.main_counter + 80
                    settings.cur_level += 1
                    # settings.spawn_audio.play()   198 168 0 14
                    # ws.PlaySound("music/battle-city-dendi.wav", ws.SND_ASYNC)
                    settings.spawn_sound.play()

            if settings.main_counter <= settings.start_storage_show:
                show_stage()
            else:
                record_file = open("record", "r")
                score = int(record_file.read())
                record_file.close()

                if settings.score[0] + settings.score[1] > score:
                    file = open("record", "w")
                    file.write(str(settings.score[0] + settings.score[1]))
                    file.close()
                settings.enemies_killed = [[0, 0, 0, 0], [0, 0, 0, 0]]
                settings.start_score_show = 0
                settings.start_storage_show = 0
                settings.end_level_wait = 0
                settings.stage_up_pos = 0
                settings.stage_up = True

                settings.killed = [[-1, -1, -1, -1], [-1, -1, -1, -1]]
                settings.p = 0
                settings.wait = False

                settings.enemies_left = settings.enemies_at_level
        else:
            if settings.start_score_show + 60 < settings.main_counter:
                settings.wait = True
                settings.staying_sound.stop()
                show_score()

    text = settings.fps_font.render(f"{round(clock.get_fps())}", True, (255, 255, 255))
    settings.main_surf.blit(text, text.get_rect(topleft=(10, 20)))

    settings.screen.blit(settings.main_surf, (406, -14))

    if not settings.wait:
        if joystick_num > 1:
            j0_left_right = js_0.get_axis(0)
            if round(j0_left_right) == 1:
                settings.tanks[1].move = [1, 0, 0, 0]
                # print("right")

            elif round(j0_left_right) == -1:
                settings.tanks[1].move = [0, 1, 0, 0]
                # print("left")

            elif round(j0_left_right) == 0:
                settings.tanks[1].move[0], settings.tanks[1].move[1] = 0, 0

            j0_up_down = js_0.get_axis(1)
            if round(j0_up_down) == 1:
                settings.tanks[1].move = [0, 0, 1, 0]
                # print("down")

            elif round(j0_up_down) == -1:
                settings.tanks[1].move = [0, 0, 0, 1]
                # print("up")

            elif round(j0_up_down) == 0:
                settings.tanks[1].move[2], settings.tanks[1].move[3] = 0, 0

            fire_button = js_0.get_button(0)
            if fire_button:
                settings.tanks[1].fire()



        j1_left_right = js_1.get_axis(0)
        if round(j1_left_right) == 1:
            settings.tanks[0].move = [1, 0, 0, 0]
            # print("right")

        elif round(j1_left_right) == -1:
            settings.tanks[0].move = [0, 1, 0, 0]
            # print("left")

        elif round(j1_left_right) == 0:
            settings.tanks[0].move[0], settings.tanks[0].move[1] = 0, 0

        j1_up_down = js_1.get_axis(1)
        if round(j1_up_down) == 1:
            settings.tanks[0].move = [0, 0, 1, 0]
            # print("down")

        elif round(j1_up_down) == -1:
            settings.tanks[0].move = [0, 0, 0, 1]
            # print("up")

        elif round(j1_up_down) == 0:
            settings.tanks[0].move[2], settings.tanks[0].move[3] = 0, 0

        fire_button = js_1.get_button(0)
        if fire_button:
            settings.tanks[0].fire()

        if joystick_num > 1:
            if abs(round(j1_up_down)) + abs(round(j1_left_right)) + abs(round(j0_up_down)) + abs(round(j0_left_right)) != 0:
                if settings.stay:
                    settings.moving_sound.play(loops=-1)
                    settings.stay = False
                    settings.staying_sound.stop()
            else:
                if not settings.stay:
                    settings.staying_sound.play(loops=-1)
                    settings.moving_sound.stop()
                    settings.stay = True
        else:
            if abs(round(j1_up_down)) + abs(round(j1_left_right)) != 0:
                if settings.stay:
                    settings.moving_sound.play(loops=-1)
                    settings.stay = False
                    settings.staying_sound.stop()
            else:
                if not settings.stay:
                    settings.staying_sound.play(loops=-1)
                    settings.moving_sound.stop()
                    settings.stay = True

    else:
        settings.staying_sound.stop()
        settings.moving_sound.stop()


    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if event.key == 27:
                print("<<< EXIT >>>")
                exit()

            if not settings.wait:
                if event.key in [97, 100, 115, 119]:
                    # settings.moving_sound.play(loops=-1)
                    # settings.staying_sound.stop()
                    pass

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

                # settings.staying_sound.play(loops=-1)
                # settings.moving_sound.stop()

            if event.key in [102, 103, 104, 116]:
                settings.tanks[1].move = [0, 0, 0, 0]

    pg.display.update()