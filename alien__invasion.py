import pygame
from settings import Seetings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


def run_game():

    pygame.init()  # 初始化pygame

    # 定义窗口等有关设置
    ai_settings = Seetings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))  # 创建一个surface 用来绘制游戏图像 注意传入的是一个元组
    pygame.display.set_caption("Alien Invasion")  # 设置窗口标题

    # 创建Play按钮
    play_button = Button(ai_settings, screen, "Play")

    # 创建一个用于储存游戏统计信息的实例
    stats = GameStats(ai_settings)

    # 创建一个储存游戏统计信息的积分板实例， 并创建记分板
    sb = Scoreboard(ai_settings, screen, stats)

    # 创建一个飞船的实例
    ship = Ship(ai_settings, screen)  # 必须在主while之前创建实例，以免每次循环都创建一艘飞船

    # 创建一个外星人的实例
    alien = Alien(ai_settings, screen)  # 感觉这一行没有任何作用啊汪

    # 创建一个用于储存子弹的编组
    bullets = Group()
    # 创建一个用于储存外星人的编组
    aliens = Group()

    # 创建外星人群
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # 开始游戏主循环 每次循环都会重绘屏幕
    while True:  # 处理响应事件

        gf.check_events(ai_settings, screen, stats, play_button, ship, aliens, bullets)

        if stats.game_active:  # 如果游戏状态是活动的 处理游戏中心代码
            ship.update()  # 用检测完毕的鼠标代码事件控制飞船的移动
            gf.update_bullets(ai_settings, screen, ship, aliens, bullets)
            gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets)

        gf.update_screen(ai_settings, screen, ship, aliens, bullets, play_button, stats, sb)


"""
        for event in pygame.event.get():  # 键盘/鼠标事件都会激活for循环
            if event.type == pygame.QUIT:  # 如果用户点击了X关闭窗口按钮
                sys.exit()  # 调用sys来退出游戏
                
        screen.fill(ai_settings.bg_color)  # 调用settings类中的颜色属性作为填充背景色
            ship.blitme()  # 填充背景后，调用blitme来将飞船绘制在屏幕上 确保飞船在背景前
            pygame.display.flip()  # 命令pygame让最近绘制的屏幕可见 擦出旧屏幕

"""
run_game()
