import pygame as pg
import os
from time import sleep
from copy import deepcopy

load = input("Load card? ").lower()

pg.init()

field_size = 28
cells_size = 36

os.environ['SDL_VIDEO_WINDOW_POS'] = '%i,%i' % (300, 30)

screen = pg.display.set_mode(((field_size + 2) * cells_size, field_size * cells_size + 1), flags=pg.DOUBLEBUF | pg.NOFRAME)
surf = pg.Surface(( (field_size + 2) * cells_size, field_size * cells_size + 1))

clock = pg.time.Clock()

field = []
for k in range(field_size):
    field.append([])
    for i in range(field_size):
        field[-1].append(0)

draw = False
wash = False

colors = {"grass": (0, 200, 0), "armor": (200, 200, 200), "brick": (150, 0, 0), "fin": (55, 55, 55)}

pos_d = (0, 0)

chosen_color = (0, 0, 0)
chosen_num = 0
chosen_img = None

old_size = cells_size

def get_imgs():
    grass_img = pg.transform.scale(pg.image.load("images/grass2.png"), (cells_size, cells_size))
    full_grass_img = pg.transform.scale(pg.image.load("images/grass2.png"), (cells_size, cells_size))

    armor_img = pg.transform.scale(pg.image.load("images/armor.jpg"), (cells_size, cells_size))
    full_armor_img = pg.transform.scale(pg.image.load("images/armor.png"), (old_size * 2, old_size * 2))

    full_brick_img = pg.transform.scale(pg.image.load("images/brick.png"), (old_size * 2, old_size * 2))
    full_water_img = pg.transform.scale(pg.image.load("images/water.png"), (old_size * 2, old_size * 2))
    full_grass_img = pg.transform.scale(pg.image.load("images/grass.png"), (old_size * 2, old_size * 2))
    water_img = pg.transform.scale(pg.image.load("images/water.jpg"), (cells_size, cells_size))

    enemies_spawn_img = pg.transform.scale(pg.image.load("images/flicks/flick3.png"), (cells_size * 2, cells_size * 2))
    enemies_little_spawn_img = pg.transform.scale(pg.image.load("images/flicks/flick1.png"), (cells_size * 2, cells_size * 2))

    spawn_img = pg.transform.scale(pg.image.load("images/flicks/flick22.png"), (cells_size * 2, cells_size * 2))
    little_spawn_img = pg.transform.scale(pg.image.load("images/flicks/flick21.png"), (cells_size * 2, cells_size * 2))


    brick_imgs = []
    brick_imgs.append(
        pg.transform.scale(pg.image.load("images/brick0.jpg"), (cells_size // 2, cells_size // 4)))
    brick_imgs.append(
        pg.transform.scale(pg.image.load("images/brick1.jpg"), (cells_size // 2, cells_size // 4)))
    brick_imgs.append(
        pg.transform.scale(pg.image.load("images/brick2.jpg"), (cells_size // 2, cells_size // 4)))
    brick_imgs.append(
        pg.transform.scale(pg.image.load("images/brick3.jpg"), (cells_size // 2, cells_size // 4)))

    return (grass_img, full_grass_img, armor_img, full_armor_img, full_brick_img, full_water_img,
            water_img, spawn_img, little_spawn_img, brick_imgs, enemies_spawn_img, enemies_little_spawn_img)

grass_img, full_grass_img, armor_img, full_armor_img, full_brick_img, full_water_img, water_img, \
                    spawn_img, little_spawn_img, brick_imgs, enemies_spawn_img, enemies_little_spawn_img= get_imgs()
move_x, move_y = 0, 0

if load == "y":
    lvl = input("What lvl? ")
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

    while True:
        try:
            field = deepcopy(fd[lvl])
            break
        except:
            lvl = input("No such lvl, enter enother: ")


draw_full_bricks = False

while True:
    surf.fill((0, 0, 0))

    clock.tick(60)

    if draw:
        pos = pg.mouse.get_pos()
        pos = (pos[0] - move_x, pos[1] - move_y)

        x = int(pos[0] // cells_size)
        y = int(pos[1] // cells_size)

        x_d, y_d = pos[0] - x * cells_size, pos[1] - y * cells_size

        if chosen_num == 3 and draw_full_bricks:
            if chosen_num == 3 and draw_full_bricks:
                field[y][x] = []

                for k in range(2):
                    for i in range(4):
                        field[y][x].append([k, i])

        elif chosen_num == 3:
            if field[y][x] == 0:
                field[y][x] = [[x_d // (cells_size // 2), y_d // (cells_size // 4)]]
            elif type(field[y][x]) is list:
                if [x_d // (cells_size // 2), y_d // (cells_size // 4)] not in field[y][x]:
                    field[y][x].append([x_d // (cells_size // 2), y_d // (cells_size // 4)])
        else:
            field[y][x] = chosen_num

    if wash:
        pos = pg.mouse.get_pos()
        pos = (pos[0] - move_x, pos[1] - move_y)

        x = int(pos[0] // cells_size)
        y = int(pos[1] // cells_size)

        try:
            if type(field[y][x]) is list and not draw_full_bricks:
                x_d, y_d = pos[0] - x * cells_size, pos[1] - y * cells_size
                if [x_d // (cells_size // 2), y_d // (cells_size // 4)] in field[y][x]:
                    field[y][x].remove([x_d // (cells_size // 2), y_d // (cells_size // 4)])
            else:
                field[y][x] = 0
        except:
            pass



    for y in range(field_size + 1):
        line = pg.draw.aaline(surf, (255, 255, 255), (0 + move_x, y * cells_size + move_y),
                              (field_size * cells_size + move_x, y * cells_size + move_y))
    for x in range(field_size + 1):
        line = pg.draw.aaline(surf, (255, 255, 255), (x * cells_size + move_x, 0 + move_y),
                              (x * cells_size + move_x, field_size * cells_size + move_y))

    for y, row in enumerate(field):
        for x, column in enumerate(row):
            if column == 1:
                img = surf.blit(grass_img, (cells_size * x + move_x, cells_size * y + move_y))
            elif column == 2:
                img = surf.blit(armor_img, (cells_size * x + move_x, cells_size * y + move_y))
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

                    img = surf.blit(brick_imgs[ind], (cells_size * x + add_nums[0] * cells_size // 2 + move_x,
                                      cells_size * y + add_nums[1] * cells_size // 4 + move_y))
            elif column == 4:
                fin = pg.draw.rect(surf, (55, 55, 55),
                                   (cells_size * x + move_x, cells_size * y + move_y, cells_size, cells_size))
            elif column == 5:
                a_img = surf.blit(enemies_little_spawn_img, (cells_size * x - cells_size // 2 + move_x, cells_size * y - cells_size // 2 + move_y))
            elif column == 6:
                a_img = surf.blit(little_spawn_img, (cells_size * x - cells_size // 2 + move_x, cells_size * y - cells_size // 2 + move_y))
                # sp_2 = pg.draw.rect(surf, (255, 255, 0),
                #                    (cells_size * x + move_x, cells_size * y + move_y, cells_size, cells_size))
            elif column == 7:
                img = surf.blit(water_img, (cells_size * x + move_x, cells_size * y + move_y))

    a_img = surf.blit(enemies_spawn_img, (old_size * field_size + 1, old_size * 4))
    a_img = surf.blit(spawn_img, (old_size * field_size + 1, old_size * 6))

    a_img = surf.blit(full_grass_img, (old_size * field_size + 1, old_size * 10))
    a_img = surf.blit(full_armor_img, (old_size * field_size + 1, old_size * 12))
    a_img = surf.blit(full_brick_img, (old_size * field_size + 1, old_size * 14))
    a_img = surf.blit(full_water_img, (old_size * field_size + 1, old_size * 16))
    fin = pg.draw.rect(surf, (55, 55, 55), (old_size * field_size + 1, old_size * 18, old_size * 2, old_size * 2))


    try:
        a_img = surf.blit(chosen_img, (old_size * field_size + 1, old_size * 22))
    except:
        pass

    x, y = pos_d
    if x // cells_size <= 27 and chosen_num == 3:
        ln = pg.draw.aaline(surf, (255, 255, 255), (x + move_x, y + move_y), (x + move_x, y + move_y + cells_size))
        ln = pg.draw.aaline(surf, (255, 255, 255), (x + move_x + cells_size // 2, y + move_y), (x + move_x + cells_size // 2, y + move_y + cells_size))
        ln = pg.draw.aaline(surf, (255, 255, 255), (x + move_x + cells_size, y + move_y), (x + move_x + cells_size, y + move_y + cells_size))

        ln = pg.draw.aaline(surf, (255, 255, 255), (x + move_x, y + move_y), (x + move_x + cells_size, y + move_y))
        ln = pg.draw.aaline(surf, (255, 255, 255), (x + move_x, y + move_y + cells_size // 4), (x + move_x + cells_size, y + move_y + cells_size // 4))
        ln = pg.draw.aaline(surf, (255, 255, 255), (x + move_x, y + move_y + cells_size // 4 * 2), (x + move_x + cells_size, y + move_y + cells_size // 4 * 2))
        ln = pg.draw.aaline(surf, (255, 255, 255), (x + move_x, y + move_y + cells_size // 4 * 3), (x + move_x + cells_size, y + move_y + cells_size // 4 * 3))
        ln = pg.draw.aaline(surf, (255, 255, 255), (x + move_x, y + move_y + cells_size // 4 * 4), (x + move_x + cells_size, y + move_y + cells_size // 4 * 4))

    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if event.key == 27:
                print("<<< EXIT >>>")
                exit()
            elif event.key == 13:
                if load == "y":
                    text = []

                    for row in field:
                        row = str(row)[1:-1].replace("[[", "$!").replace("]]", "!$").replace("[", "!").replace("]", "!")
                        text.append(row + "\n")

                    file = open("cards", "r")
                    file_2 = open("promej", "w")

                    change = False
                    counter = 0
                    while True:
                        line = file.readline()
                        if not line:
                            break
                        if f"|{lvl}|" in line:
                            change = True
                            file_2.write(line)
                        elif change and line != "\n":
                            file_2.write(text[counter])
                            counter += change
                        else:
                            file_2.write(line)
                        if counter == 28:
                            change = False

                    file.close()
                    file_2.close()

                    file = open("cards", "w")
                    file_2 = open("promej", "r")

                    while True:
                        line = file_2.readline()
                        if line:
                            file.write(line)
                        else:
                            break
                    exit()
                else:
                    name = input("Enter card index: ")
                    file = open("cards", "a")
                    file.write(f"\n|{name}|\n")

                    for row in field:
                        row = str(row)[1:-1].replace("[[", "$!").replace("]]", "!$").replace("[", "!").replace("]", "!")
                        file.write(row)
                        file.write("\n")

                    file.close()

                    print("\n<<< Saving successful >>>\n")

                    exit()

            elif event.key == 8:
                field = []
                for k in range(field_size):
                    field.append([])
                    for i in range(field_size):
                        field[-1].append(0)
            elif event.key == 304:
                draw_full_bricks = True
        elif event.type == pg.KEYUP:
            if event.key == 304:
                draw_full_bricks = False



        elif  event.type == pg.MOUSEMOTION:
            pos = pg.mouse.get_pos()
            pos = (pos[0] - move_x, pos[1] - move_y)

            x = pos[0] // cells_size
            y = pos[1] // cells_size

            pos_d = (x * cells_size, y * cells_size)

        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:

                pos_o = pg.mouse.get_pos()
                pos = (pos_o[0] - move_x, pos_o[1] - move_y)

                x = pos[0] // cells_size
                y = pos[1] // cells_size

                if pos_o[0] > old_size * field_size:
                    if old_size * 4 <= pos_o[1] < old_size * 6:
                        chosen_img = enemies_spawn_img
                        chosen_num = 5
                    if old_size * 6 <= pos_o[1] < old_size * 8:
                        chosen_color = (255, 255, 0)
                        chosen_img = spawn_img
                        chosen_num = 6

                    if old_size * 10 <= pos_o[1] < old_size * 12:
                        chosen_color = colors["grass"]
                        chosen_img = full_grass_img
                        chosen_num = 1
                    elif old_size * 12 <= pos_o[1] < old_size * 14:
                        chosen_color = colors["armor"]
                        chosen_img = full_armor_img
                        chosen_num = 2
                    elif old_size * 14 <= pos_o[1] < old_size * 16:
                        chosen_color = colors["brick"]
                        chosen_img = full_brick_img
                        chosen_num = 3
                    elif old_size * 16 <= pos_o[1] < old_size * 18:
                        chosen_img = full_water_img
                        chosen_num = 7
                    elif old_size * 18 <= pos_o[1] < old_size * 20:
                        chosen_color = colors["fin"]

                        chosen_num = 4
                else:
                    draw = True

            elif event.button == 3:
                wash = True

        elif event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                draw = False
            elif event.button == 3:
                wash = False

            elif event.button == 4:
                if cells_size < 100:
                    cells_size += 2
                    grass_img, full_grass_img, armor_img, full_armor_img, full_brick_img, full_water_img, water_img, \
                    spawn_img, little_spawn_img, brick_imgs, enemies_spawn_img, enemies_little_spawn_img = get_imgs()

                    m_x, m_y = pg.mouse.get_pos()

                    koef_x = m_x - (cells_size / 36) * m_x
                    koef_y = m_y - (cells_size / 36) * m_y

                    move_x = koef_x
                    move_y = koef_y

                    pos = pg.mouse.get_pos()
                    pos = (pos[0] - move_x, pos[1] - move_y)

                    x = pos[0] // cells_size
                    y = pos[1] // cells_size

                    pos_d = (x * cells_size, y * cells_size)

            elif event.button == 5:
                if cells_size > 36:
                    cells_size -= 2
                    grass_img, full_grass_img, armor_img, full_armor_img, full_brick_img, full_water_img, water_img, \
                    spawn_img, little_spawn_img, brick_imgs, enemies_spawn_img, enemies_little_spawn_img = get_imgs()

                    m_x, m_y = pg.mouse.get_pos()

                    koef_x = m_x - (cells_size / 36) * m_x
                    koef_y = m_y - (cells_size / 36) * m_y

                    move_x = koef_x
                    move_y = koef_y

                    pos = pg.mouse.get_pos()
                    pos = (pos[0] - move_x, pos[1] - move_y)

                    x = pos[0] // cells_size
                    y = pos[1] // cells_size

                    pos_d = (x * cells_size, y * cells_size)


    screen.blit(surf, (0, 0))

    pg.display.update()