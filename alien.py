import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """表示单个外星人的类"""

    def __init__(self, ai_settings, screen):
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # 加载外星人图像，并设置其rect属性
        self.image = pygame.image.load('images\\alien.bmp')
        self.rect = self.image.get_rect()

        # 存储外星人最初都在屏幕左上角
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # 存储外星人的准确位置
        self.x = float(self.rect.x)

    def blitme(self):
        """在指定的地方绘制外星人"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """向左或向右移动外星人"""
        self.x += (self.ai_settings.alien_speed_factor *
                   self.ai_settings.fleet_direction)  # 要么向左，要么向右 符号相反 用±1来表示
        self.rect.x = self.x

    def check_edges(self):
        """检测外星人撞到了屏幕边缘就返回True"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= screen_rect.left:  # screen.left 也可以换成0
            return True
