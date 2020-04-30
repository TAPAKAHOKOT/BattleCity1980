from pygame import transform, image, mixer, font
class Settings:
    def __init__(self):
        self.field_size = 28
        self.cells_size = 36

        self.win_width = self.field_size * self.cells_size + 100
        self.win_height = self.field_size * self.cells_size + 100
        self.win_size = (self.win_width, self.win_height)

        self.win_bg = (0, 0, 0)
        self.win_fps = 30

        self.screen = None
        self.main_surf = None

        self.grill = False

        self.levels = None

        self.cur_level = 4

        self.enemies_at_level = 14
        self.bots_spawned = 0
        self.enemies_left = self.enemies_at_level

        self.field =  []

        self.grass = []
        self.armor = []
        self.bricks = []
        self.fin = []
        self.bullets = []
        self.water = []
        self.bots = []
        self.bonuses = []

        self.frame_color = (70, 70, 70)

        self.spawns = []
        self.tanks = []

        self.fin_pos = (0, 0)
        self.bots_spawn = []

        self.bangs = []
        self.tanks_bangs = []

        self.tanks_speed = [6, 5, 4, 4]
        self.tanks_force = [1, 2, 3, 3]
        self.tanks_bullets_speed = [12, 10, 8, 10]
        self.tanks_health = [1, 1, 2, 2]

        self.spawn_time = 40

        self.booms = []

        self.bots_spawn_counter = 0
        self.bots_spawner_speed = 150

        for k in range(1, 8):
            self.booms.append(transform.scale(image.load(f"images/booms/boom{k}.png"), (self.cells_size * 2, self.cells_size * 2)))

        self.big_booms = []
        for k in range(1, 8):
            self.big_booms.append(transform.scale(image.load(f"images/booms/boom{k}.png"), (self.cells_size * 4, self.cells_size * 4)))

        self.moving_sound = mixer.Sound("music/move.wav")
        self.staying_sound = mixer.Sound("music/stay.wav")

        self.main_counter = 0
        self.stop_interval = -1

        self.hpfont = font.SysFont('System', int(45))

        self.mini_tank = transform.scale(image.load("images/mini_tank.png"), (24, 24))

