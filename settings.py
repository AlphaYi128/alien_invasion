class Settings:
    """存储游戏的所有设置的类"""

    def __init__(self):
        """初始化游戏设置"""
        # 屏幕设置
        self.screen_width = 1200
        self.screen_height = 900
        self.bg_color = (230, 230, 230)

        # 飞船的设置
        self.ship_speed_factor = 0.5
        self.ship_limit = 3

        # 子弹的设置
        self.bullet_speed_factor = 1.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 0
        self.bullet_interval = 50

        # 外星人的设置
        self.alien_speed_factor = 0.1
        self.alien_drop_speed = 100
