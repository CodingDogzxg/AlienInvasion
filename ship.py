import pygame
from pygame.sprite import Sprite


class Ship(Sprite):

    def __init__(self, ai_settings, screen):
        super().__init__()
        # 初始化飞船并设置其起始位置
        self.screen = screen
        self.ai_settings = ai_settings

        # 加载飞船图像并且获取其外接矩形
        self.image = pygame.image.load('images\\ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # 将每艘新飞船放在屏幕底部 screen的rect是固定的 将飞船根据screen的rect进行排列
        self.rect.centerx = self.screen_rect.centerx  # 飞船rect中央在窗口rect中央
        self.rect.bottom = self.screen_rect.bottom  # 飞船rect底部在窗口rect底部

        self.center = float(self.rect.centerx)

        self.moving_right = False
        self.moving_left = False

    def update(self):
        """根据移动标志调整飞船的位置"""
        # 更新center值，而不是rect 更新的是self.center变量!
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > self.screen_rect.left:  # self.screen_rect.left也可以换成0
            self.center -= self.ai_settings.ship_speed_factor

        # 根据self.center更新rect对象 将更新完毕的self.center变量赋值给外接矩形centerx
        self.rect.centerx = self.center

    def blitme(self):
        # 在指定位置绘制飞船
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """让飞船在屏幕上居中"""
        self.center = self.screen_rect.centerx
