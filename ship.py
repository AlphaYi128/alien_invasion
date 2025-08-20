import pygame

class Ship:

    def __init__(self, ai_settings, screen):
        """初始化飞船并设置其初始位置"""
        self.screen = screen
        self.ai_settings = ai_settings

        # 加载飞船图像并获取其外形矩形
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        # 在飞船的属性center中存储小数值，以便可以更加精确地控制飞船
        self.moving_right = False
        self.moving_left = False

        # 获取屏幕窗口尺寸
        self.screen_rect = screen.get_rect()

        # 将飞船放置在屏幕底部中央
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        self.center = float(self.rect.centerx)

    def blitme(self):
        # 在指定位置绘制飞船
        self.screen.blit(self.image, self.rect)

    def move_left(self, width=1):
        self.center -= self.ai_settings.ship_speed_factor

    def move_right(self, width=1):
        self.center += self.ai_settings.ship_speed_factor

    def move_center(self):
        self.center = self.screen_rect.centerx

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.move_right()
        elif self.moving_left and self.rect.left > self.screen_rect.left:
            self.move_left()
        self.rect.centerx = int(self.center)
