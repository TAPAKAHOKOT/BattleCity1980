import pygame as pg

class Water:
    def __init__(self, surf, size, cell_size, pos):
        self.surf = surf

        self.x, self.y = pos

        self.draw_rect = pg.Rect(50 + self.x * cell_size, 50 + self.y * cell_size, cell_size, cell_size)

        self.x, self.y = 50 + self.x * cell_size, 50 + self.y * cell_size

        self.main_img = pg.transform.scale(pg.image.load("images/water.jpg"), (cell_size, cell_size))

    def draw(self):
        # self.rect = pg.draw.rect(self.surf, self.color, self.draw_rect)

        self.img = self.surf.blit(self.main_img, (self.x, self.y))