import pygame as pg

class Water:
    def __init__(self, surf, size, cell_size, pos):
        self.surf = surf

        self.x, self.y = pos
        self.cell_size = cell_size

        self.draw_rect = pg.Rect(50 + self.x * cell_size, 50 + self.y * cell_size, cell_size, cell_size)

        self.x, self.y = 50 + self.x * cell_size, 50 + self.y * cell_size

        self.main_img = pg.transform.scale(pg.image.load("images/water1.jpg"), (self.cell_size, self.cell_size))

        self.img_num = 1
        self.counter = 0

    def draw(self):
        self.counter += 1
        if self.counter % 20 == 0:
            self.img_num = 3 - self.img_num
            self.main_img = pg.transform.scale(pg.image.load(f"images/water{self.img_num}.jpg"), (self.cell_size, self.cell_size))

        # self.rect = pg.draw.rect(self.surf, self.color, self.draw_rect)

        self.img = self.surf.blit(self.main_img, (self.x, self.y))