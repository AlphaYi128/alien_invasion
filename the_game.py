import sys
from time import sleep

import pygame
#from pygame import mouse
#from pygame.examples import aliens

#import game_stats
from alien import Alien
#from ship import Ship
#from settings import Settings
from bullet import Bullet
#from game_stats import GameStats

class TheGame:
    def __init__(self, ai_settings, screen, ship, aliens, bullets):
        self.screen = screen
        self.ai_settings = ai_settings
        self.ship = ship
        self.aliens = aliens
        self.bullets = bullets
        self.space_key_down = False
        self.bullet_interval_tick = self.ai_settings.bullet_interval

        self.fleet_direction = 1 # 初始时，向右移动

    def fire_bullet(self):
        if self.ai_settings.bullets_allowed == 0 or len(self.bullets) < self.ai_settings.bullets_allowed:
            # 创建一颗子弹， 并将其加入到编组bullets中
            new_bullet = Bullet(self.ai_settings, self.screen, self.ship)
            self.bullets.add(new_bullet)

    def start_game(self, game_stats):
        if not game_stats.game_active:
            # 隐藏鼠标光标
            pygame.mouse.set_visible(False)
            # 重置游戏统计信息
            game_stats.reset_stats()
            game_stats.game_active = True

            # 清空外星人列表和子弹列表
            self.aliens.empty()
            self.bullets.empty()

            # 创建一群新的外星人，并让飞船居中
            self.creat_fleet()
            self.ship.move_center()

    def check_keydown_events(self, event, game_stats):
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_SPACE:
            self.space_key_down = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_p:
            self.start_game(game_stats)


    def check_keyup_events(self, event):
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_SPACE:
            self.space_key_down = False
            self.bullet_interval_tick = self.ai_settings.bullet_interval


    def check_events(self, game_stats, play_button):
        """响应键盘和鼠标事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self.check_keydown_events(event, game_stats)
            elif event.type == pygame.KEYUP:
                self.check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print("mouse button down")
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self.check_play_button(game_stats, play_button, mouse_x, mouse_y)

    def check_play_button(self, game_stats, play_button, mouse_x, mouse_y):
        """玩家单击Play按钮时开始新游戏"""
        play_button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
        if play_button_clicked:
            self.start_game(game_stats)

    def check_bullet_alien_collisions(self):
        """
        检查是否有子弹击中了外星人
        # 如果击中，就删除相应的子弹和外星人
        """
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        # 如果外星人被全部消灭了，删除屏幕上的所有子弹，并重新创建一组外星人
        if len(self.aliens) == 0:
            self.bullets.empty()
            self.creat_fleet()

    def update_bullets(self):
        if self.space_key_down:
            if self.bullet_interval_tick == self.ai_settings.bullet_interval:
                self.fire_bullet()
                self.bullet_interval_tick = 0
            else:
                self.bullet_interval_tick += 1
        """更新子弹的位置，删除已消失的子弹"""
        # 更新每个子弹的位置
        self.bullets.update() #调用父类Sprite的update方法，遍历每一个成员，并调用其update方法

        # 删除已消失（到屏幕外面）的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.top < 0:
                self.bullets.remove(bullet)

        self.check_bullet_alien_collisions()

    def get_number_aliens_x(self, alien_width):
        available_space_x = self.screen.get_width() - 2 * alien_width
        number_aliens_x = int(available_space_x / (2 * alien_width))
        return number_aliens_x

    def get_number_aliens_y(self, ship_height, alien_height):
        available_space_y = self.screen.get_height() - 3 * alien_height - ship_height
        number_aliens_y = int(available_space_y / (2 * alien_height))
        return number_aliens_y

    def creat_alien(self, alien_number_x, alien_number_y):
        """创建一个外星人，并将其放在当前行"""
        alien = Alien(self.ai_settings, self.screen)
        alien_width = alien.rect.width
        alien_height = alien.rect.height
        alien.x = alien_width + 2 * alien_number_x * alien_width
        alien.y = alien_height + 2 * alien_number_y * alien_height
        alien.rect.x = alien.x
        alien.rect.y = alien.y
        self.aliens.add(alien)

    def creat_fleet(self):
        """创建外星人群，并存储在aliens Group组中"""
        # 创建一个外星人，并计算一行可以容纳多少个外星人
        alien = Alien(self.ai_settings, self.screen)
        alien_width = alien.rect.width
        alien_height = alien.rect.height
        number_aliens_x = self.get_number_aliens_x(alien_width)
        number_aliens_y = self.get_number_aliens_y(self.ship.rect.height, alien_height)

        # 创建第一行外星人
        for alien_index_y in range(number_aliens_y):
            for alien_index_x in range(number_aliens_x):
                self.creat_alien(alien_index_x, alien_index_y)

        #print(len(aliens))

    def change_fleet_direction(self):
        for alien in self.aliens:
            alien.rect.y += self.ai_settings.alien_drop_speed
        self.fleet_direction *= -1

    def check_fleet_touch_edge(self):
        for alien in self.aliens:
            if alien.check_touch_edge():
                self.change_fleet_direction()
                break

    def check_fleet_touch_bottom(self, game_stats):
        for alien in self.aliens:
            if alien.rect.bottom >= self.screen.get_rect().bottom:
                self.ship_hit(game_stats)
                break

    def check_alien_ship_collisions(self, game_stats):
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self.ship_hit(game_stats)

    def ship_hit(self, game_stats):
        """响应飞船被外星人碰撞"""
        if game_stats.ship_left > 1:
            # 将ship_left减1
            game_stats.ship_left -= 1

            # 清空外星人列表和子弹列表
            self.aliens.empty()
            self.bullets.empty()

            # 创建一群新的外星人，并将飞船放到屏幕底部中央
            self.creat_fleet()
            self.ship.move_center()

            # 暂停
            sleep(0.5)
        else:
            game_stats.game_active = False
            # 让鼠标光标可见
            pygame.mouse.set_visible(True)
            #print("Game Over")

    def update_aliens(self, game_stats):
        """更新外星人群中所有外星人的位置"""
        # 先检查飞船是否与外星人发生碰撞
        self.check_alien_ship_collisions(game_stats)
        # 再检查外星人是否碰到屏幕边缘，并向下移动
        self.check_fleet_touch_edge()
        # 接着检查是否有外星人到达屏幕底部
        self.check_fleet_touch_bottom(game_stats)
        self.aliens.update(self.fleet_direction)

    def update_screen(self, game_stats, play_button):
        """更新屏幕上的图像，并切换到新屏幕"""
        self.screen.fill(self.ai_settings.bg_color)

        # 重绘所有子弹
        for bullet in self.bullets.sprites():
            #print(bullet.rect.center)
            bullet.draw()

        # 绘制飞船
        self.ship.blitme()

        # 绘制外星人
        alien: object
        for alien in self.aliens.sprites():
            #print(bullet.rect.center)
            alien.draw()

        # 如果游戏处于非活动状态，就绘制Play按钮
        if not game_stats.game_active:
            play_button.draw_button()

        # 让最近绘制的屏幕可见
        # pygame.display.update()
        pygame.display.flip()
