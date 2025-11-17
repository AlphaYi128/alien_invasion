import sys

import pygame

from button import Button
from game_stats import GameStats
from the_game import TheGame
from settings import Settings
from ship import Ship
from pygame.sprite import Group

def run_game():
    # 初始化游戏并创建一个屏幕对象
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # 创建Play按钮
    play_button = Button(ai_settings, screen, "Play")

    # 设置背景色
    # 移入setting中
    #bg_color = (230, 230, 230)

    # 创建一艘飞船
    ship = Ship(ai_settings, screen)

    # 创建一个用于存储子弹的编组
    bullets = Group()

    aliens = Group()

    the_game = TheGame(ai_settings, screen, ship, aliens, bullets)
    the_game.creat_fleet()

    game_stats = GameStats(ai_settings)

    # 开始游戏的主循环
    while True:

        # 监视键盘和鼠标事件
        the_game.check_events(game_stats, play_button)

        if game_stats.game_active:
            ship.update()

            the_game.update_bullets()
            the_game.update_aliens(game_stats)

        # 每次循环时都重绘屏幕
        the_game.update_screen(game_stats, play_button)

run_game()