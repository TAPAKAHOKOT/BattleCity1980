import pygame as pg

class Grass:
    def __init__(self, surf, size, cell_size, pos):
        self.surf = surf

        # self.x, self.y = rnd(0, size), rnd(0, size)
        self.x, self.y = pos

        # self.draw_rect = (50 + self.x * cell_size, 50 + self.y * cell_size, cell_size, cell_size)
        self.x, self.y = 50 + self.x * cell_size, 50 + self.y * cell_size

        self.color = (0, 100, 0)

        self.main_img = pg.transform.scale(pg.image.load("images/grass2.png"), (cell_size, cell_size))

    def draw(self):
        # self.rect = pg.draw.rect(self.surf, self.color, self.draw_rect)

        self.img = self.surf.blit(self.main_img, (self.x, self.y) )