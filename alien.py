import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """表示单个外星人的类"""

    def __init__(self, ai_settings, screen):
        """初始化外星人并设置其起始位置"""
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # 加载外星人图像，并设置其rect属性
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # 每个外星人最初在屏幕左上角附近
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # 存储外星人的准确位置
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def blitme(self):
        """在指定位置绘制外星人"""
        self.screen.blit(self.image, self.rect)

    def draw(self):
        self.blitme()

    def move(self, direction):
        self.x += self.ai_settings.alien_speed_factor * direction
        self.rect.x = int(self.x)


    def drop(self):
        self.y += self.ai_settings.alien_drop_speed
        self.rect.y = int(self.y)

    def check_touch_edge(self):
        """检查外星人是否碰到了屏幕边缘，是就返回True，否则返回False"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
        return False

    def update(self, direction):
        self.move(direction)
