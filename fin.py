
import pygame as pg

class Fin:
    def __init__(self, surf, size, cell_size, pos):
        self.surf = surf

        self.x, self.y = pos

        self.draw_rect = (50 + self.x * cell_size, 50 + self.y * cell_size, cell_size, cell_size)

        self.color = (55, 55, 55)

    def draw(self):
        self.rect = pg.draw.rect(self.surf, self.color, self.draw_rect)