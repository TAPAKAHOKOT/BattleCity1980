import pygame as pg
from random import randint as rnd

class Brick:
    def __init__(self, surf, size, cell_size, pos, count):
        self.surf = surf

        self.x, self.y = pos

        self.draw_rect = (self.x, self.y, cell_size//2, cell_size // 4)

        self.color = (150, 0, 0)

        self.main_img = pg.transform.scale(pg.image.load(f"images/brick{count}.jpg"), (cell_size//2, cell_size // 4))

    def draw(self):
        # self.rect = pg.draw.rect(self.surf, self.color, self.draw_rect)

        self.img = self.surf.blit(self.main_img, (self.x, self.y))