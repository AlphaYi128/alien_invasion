import sys
from time import sleep

import pygame
from pygame import mouse

import game_stats
import ship
from alien import Alien
from ship import Ship
from settings import Settings
from bullet import Bullet

class TheGame:
    def __init__(self, ai_settings, screen, ship, bullets):
        self.screen = screen
        self.ai_settings = ai_settings
        self.ship = ship
        self.bullets = bullets
        self.space_key_down = False
        self.bullet_interval_tick = self.ai_settings.bullet_interval

        self.fleet_direction = 1 # 初始时，向右移动

    def fire_bullet(self, ai_settings, screen, ship, bullets):
        if ai_settings.bullets_allowed == 0 or len(bullets) < ai_settings.bullets_allowed:
            # 创建一颗子弹， 并将其加入到编组bullets中
            new_bullet = Bullet(ai_settings, screen, ship)
            bullets.add(new_bullet)


    def check_keydown_events(self, event, ai_settings, screen, ship, bullets):
        if event.key == pygame.K_LEFT:
            ship.moving_left = True
        elif event.key == pygame.K_RIGHT:
            ship.moving_right = True
        elif event.key == pygame.K_SPACE:
            self.space_key_down = True
        elif event.key == pygame.K_q:
            sys.exit()


    def check_keyup_events(self, event, ship):
        if event.key == pygame.K_LEFT:
            ship.moving_left = False
        elif event.key == pygame.K_RIGHT:
            ship.moving_right = False
        elif event.key == pygame.K_SPACE:
            self.space_key_down = False
            self.bullet_interval_tick = self.ai_settings.bullet_interval


    def check_events(self, ai_settings, screen, game_stats, play_button, bullets):
        """响应键盘和鼠标事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self.check_keydown_events(event, ai_settings, screen, self.ship, bullets)
            elif event.type == pygame.KEYUP:
                self.check_keyup_events(event, self.ship)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print("mouse button down")
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self.check_play_button(game_stats, play_button, mouse_x, mouse_y)

    def check_play_button(self, game_stats, play_button, mouse_x, mouse_y):
        if play_button.rect.collidepoint(mouse_x, mouse_y):
            game_stats.game_active = True
            game_stats.reset_stats()

    def check_bullet_alien_collisions(self, aliens, bullets):
        """
        检查是否有子弹击中了外星人
        # 如果击中，就删除相应的子弹和外星人
        """
        collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

        # 如果外星人被全部消灭了，删除屏幕上的所有子弹，并重新创建一组外星人
        if len(aliens) == 0:
            bullets.empty()
            self.creat_fleet(aliens)

    def update_bullets(self, bullets, aliens):
        if self.space_key_down:
            if self.bullet_interval_tick == self.ai_settings.bullet_interval:
                self.fire_bullet(self.ai_settings, self.screen, self.ship, self.bullets)
                self.bullet_interval_tick = 0
            else:
                self.bullet_interval_tick += 1
        """更新子弹的位置，删除已消失的子弹"""
        # 更新每个子弹的位置
        bullets.update() #调用父类Sprite的update方法，遍历每一个成员，并调用其update方法

        # 删除已消失（到屏幕外面）的子弹
        for bullet in bullets.copy():
            if bullet.rect.top < 0:
                bullets.remove(bullet)

        self.check_bullet_alien_collisions(aliens, bullets)

    def get_number_aliens_x(self, ai_settings, alien_width):
        available_space_x = self.screen.get_width() - 2 * alien_width
        number_aliens_x = int(available_space_x / (2 * alien_width))
        return number_aliens_x

    def get_number_aliens_y(self, ai_settings, ship_height, alien_height):
        available_space_y = self.screen.get_height() - 3 * alien_height - ship_height
        number_aliens_y = int(available_space_y / (2 * alien_height))
        return number_aliens_y

    def creat_alien(self, ai_settings, screen, aliens, alien_number_x, alien_number_y):
        """创建一个外星人，并将其放在当前行"""
        alien = Alien(self.ai_settings, self.screen)
        alien_width = alien.rect.width
        alien_height = alien.rect.height
        alien.x = alien_width + 2 * alien_number_x * alien_width
        alien.y = alien_height + 2 * alien_number_y * alien_height
        alien.rect.x = alien.x
        alien.rect.y = alien.y
        aliens.add(alien)

    def creat_fleet(self, aliens):
        """创建外星人群，并存储在aliens Group组中"""
        # 创建一个外星人，并计算一行可以容纳多少个外星人
        alien = Alien(self.ai_settings, self.screen)
        alien_width = alien.rect.width
        alien_height = alien.rect.height
        number_aliens_x = self.get_number_aliens_x(self.ai_settings, alien_width)
        number_aliens_y = self.get_number_aliens_y(self.ai_settings, self.ship.rect.height, alien_height)

        # 创建第一行外星人
        for alien_index_y in range(number_aliens_y):
            for alien_index_x in range(number_aliens_x):
                self.creat_alien(self.ai_settings, self.screen, aliens, alien_index_x, alien_index_y)

        #print(len(aliens))

    def change_fleet_direction(self, aliens):
        for alien in aliens:
            alien.rect.y += self.ai_settings.alien_drop_speed
        self.fleet_direction *= -1

    def check_fleet_touch_edge(self, aliens):
        for alien in aliens:
            if alien.check_touch_edge():
                self.change_fleet_direction(aliens)
                break

    def check_fleet_touch_bottom(self, game_stats, aliens, bullets):
        for alien in aliens:
            if alien.rect.bottom >= self.screen.get_rect().bottom:
                self.ship_hit(game_stats, aliens, bullets)
                break

    def check_alien_ship_collisions(self, game_stats, aliens):
        if pygame.sprite.spritecollideany(self.ship, aliens):
            self.ship_hit(game_stats, aliens, self.bullets)

    def ship_hit(self, game_stats, aliens, bullets):
        """响应飞船被外星人碰撞"""
        if game_stats.ship_left > 1:
            # 将ship_left减1
            game_stats.ship_left -= 1

            # 清空外星人列表和子弹列表
            aliens.empty()
            bullets.empty()

            # 创建一群新的外星人，并将飞船放到屏幕底部中央
            self.creat_fleet(aliens)
            self.ship.move_center()

            # 暂停
            sleep(0.5)
        else:
            game_stats.game_active = False
            #print("Game Over")

    def update_aliens(self, game_stats, aliens):
        """更新外星人群中所有外星人的位置"""
        # 先检查飞船是否与外星人发生碰撞
        self.check_alien_ship_collisions(game_stats, aliens)
        # 再检查外星人是否碰到屏幕边缘，并向下移动
        self.check_fleet_touch_edge(aliens)
        # 接着检查是否有外星人到达屏幕底部
        self.check_fleet_touch_bottom(game_stats, aliens, self.bullets)
        aliens.update(self.fleet_direction)

    def update_screen(self, ai_settings, screen, game_stats, aliens, bullets, play_button):
        """更新屏幕上的图像，并切换到新屏幕"""
        screen.fill(ai_settings.bg_color)

        # 重绘所有子弹
        for bullet in bullets.sprites():
            #print(bullet.rect.center)
            bullet.draw()

        # 绘制飞船
        self.ship.blitme()

        # 绘制外星人
        alien: object
        for alien in aliens.sprites():
            #print(bullet.rect.center)
            alien.draw()

        # 如果游戏处于非活动状态，就绘制Play按钮
        if not game_stats.game_active:
            play_button.draw_button()

        # 让最近绘制的屏幕可见
        # pygame.display.update()
        pygame.display.flip()
