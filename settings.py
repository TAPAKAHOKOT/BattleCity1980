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

        self.cur_level = 1
        self.levels_num = 14

        self.enemies_at_level = 20
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

        self.tanks_speed = [8, 7, 6, 7]
        self.tanks_force = [1, 2, 3, 3]
        self.tanks_fire_rate = [6, 10, 3, 5]
        self.tanks_bullets_speed = [12, 24, 20, 25]
        self.tanks_health = [1, 1, 2, 2]

        self.bots_speed = [5, 7, 6, 4]
        self.bots_fire_rate = [10, 12, 10, 14]
        self.bots_bullets_speed = [12, 16, 12, 10]

        self.spawn_time = 40

        self.booms = []

        self.bots_spawn_counter = 0
        self.bots_spawner_speed = 150
        self.bots_costs = [100, 200, 300, 500]

        for k in range(1, 8):
            self.booms.append(transform.scale(image.load(f"images/booms/boom{k}.png"), (self.cells_size * 2, self.cells_size * 2)))

        self.big_booms = []
        for k in range(1, 8):
            self.big_booms.append(transform.scale(image.load(f"images/booms/boom{k}.png"), (self.cells_size * 4, self.cells_size * 4)))

        self.moving_sound = mixer.Sound("music/move.wav")
        self.staying_sound = mixer.Sound("music/stay.wav")

        self.main_counter = 0
        self.stop_interval = -1

        self.hpfont = font.Font("D:/pycharm_progects/bold_pixel_font.ttf", int(22))
        self.points_font = font.Font("D:/pycharm_progects/pixel_font.ttf", int(24))
        self.score_font = font.Font("D:/pycharm_progects/bold_pixel_font.ttf", int(34))

        self.mini_tank = transform.scale(image.load("images/mini_tank.png"), (24, 24))

        self.score = [0, 0]
        self.end_level_wait = 0

        self.bots_imgs = []
        for k in range(4):
            self.bots_imgs.append(transform.scale(image.load(f"images/tanks/bad/tank{k + 2}{4}.png"),
                                                  (int(self.cells_size * 1.5), int(self.cells_size * 1.5))))

        self.enemies_killed = [[0, 0, 0, 0], [0, 0, 0, 0]]
        self.start_score_show = 0
        self.start_storage_show = 0


        self.killed = [[-1, -1, -1, -1], [-1, -1, -1, -1]]
        self.p = 0

        self.wait = False
        self.stage_up_pos = 0
        self.stage_up = True

        self.bots_nums = [18, 2, 0, 0]

        self.run_game = True
        self.stop_game = False


        # self.fire_audio = sa.WaveObject.from_wave_file("music/fire.wav")
        # self.spawn_audio = sa.WaveObject.from_wave_file("music/battle-city-dendi.wav")
        # self.blink_audio = sa.WaveObject.from_wave_file("music/blink.wav")
        # self.past_shoot_audio = sa.WaveObject.from_wave_file("music/past_shoot.wav")
        # self.death_audio = sa.WaveObject.from_wave_file("music/death.wav")
        # self.bot_boom_audio = sa.WaveObject.from_wave_file("music/bot_boom.wav")
        # self.bonus_created_audio = sa.WaveObject.from_wave_file("music/bonus_created.wav")
        # self.bim_audio = sa.WaveObject.from_wave_file("music/bim.wav")
        # self.bonus_audio = sa.WaveObject.from_wave_file("music/bomb_bonus.wav")
        # self.hp_bonus_audio = sa.WaveObject.from_wave_file("music/health_bonus.wav")

        self.fire_sound = mixer.Sound("music/fire.wav")
        self.spawn_sound = mixer.Sound("music/battle-city-dendi.wav")
        self.blink_sound = mixer.Sound("music/blink.wav")
        self.past_shoot_sound = mixer.Sound("music/past_shoot.wav")
        self.death_sound = mixer.Sound("music/death.wav")
        self.bot_boom_sound = mixer.Sound("music/bot_boom.wav")
        self.bonus_created_sound = mixer.Sound("music/bonus_created.wav")
        self.bim_sound = mixer.Sound("music/bim.wav")
        self.bonus_sound = mixer.Sound("music/bomb_bonus.wav")
        self.hp_bonus_sound = mixer.Sound("music/health_bonus.wav")


        self.stay = True
