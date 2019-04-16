class Seetings():

    def __init__(self):

        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # 飞船设置
        """self.ship_speed_factor = 2"""
        self.ship_limit = 3  # 一共可以玩四条命汪

        # 子弹设置
        """self.bullet_speed_factor = 3"""
        self.bullet_width = 300
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 5

        # 外星人设置
        """self.alien_speed_factor = 1"""
        self.fleet_drop_speed = 100
        # fleet_direction为1表示向右移，-1表示向左移动
        """self.fleet_direction = 1"""

        # 以什么样的速度加快游戏节奏 倍数增长
        self.speedup_scale = 1.1
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """初始化虽游戏的进行而变化的设置"""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1

        # fleet_direction为1表示向右移， -1表示向左移动
        self.fleet_direction = 1
        # 计分
        self.alien_points = 50

    def increase_speed(self):
        """提高游戏速度"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale