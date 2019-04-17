import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep
import json


# 最高分文件名
file_name = "highest_score.json"


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """检测按键按下事件"""
    if event.key == pygame.K_RIGHT:   # 向右移动飞船
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullets(ai_settings, screen, ship, bullets)


def fire_bullets(ai_settings, screen, ship, bullets):
    """如果子弹还没有达到限额，就发射一颗子弹"""
    # 创建一颗子弹，并将其加入到编组bullets
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)  # 代表着加入精灵bullets组的bullet是属于Bullet类


def check_keyup_events(event, ship):
    """检测按键抬起事件"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    """响应鼠标、键盘事件"""
    for event in pygame.event.get():  # 每个鼠标/键盘事件都会激活for循环
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                sys.exit()
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)


def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    """在玩家单击Play按钮开始游戏"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:  # 仅当玩家单击按钮且游戏当前处于非活跃状态时才运行以下代码
        # 重置游戏设置
        ai_settings.initialize_dynamic_settings()

        # 读取最高分
        try:
            with open(file_name, "r") as obj_load:
                stats.high_score = json.load(obj_load)
                print(stats.high_score)
        except FileNotFoundError:
            stats.high_score = 0
            print("Didn't found the stored highest score!")

        # 隐藏光标
        pygame.mouse.set_visible(False)
        # 重置游戏信息
        stats.reset_stats()
        stats.game_active = True

        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        # 重置记分板
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # 创建一群新的外星人，并让飞船居中
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


"""
def check_events(ship):

    for event in pygame.event.get():  # 键盘/鼠标事件都会激活for循环
        if event.type == pygame.QUIT:  # 如果用户点击了X关闭窗口按钮
            sys.exit()  # 调用sys来退出游戏
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                # 向右移动飞船
                ship.moving_right = True
            elif event.key == pygame.K_LEFT:
                ship.moving_left = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                ship.moving_right = False
            elif event.key == pygame.K_LEFT:
                ship.moving_left = False

"""


def update_screen(ai_settings, screen, ship, aliens, bullets, play_button, stats, sb):
    """更新屏幕上的图像 并且换到新屏幕"""
    screen.fill(ai_settings.bg_color)  # 调用settings类中的颜色属性作为填充背景色

    # 在飞船和外星人后面重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()  # 填充背景后，调用blitme来将飞船绘制在屏幕上 确保飞船在背景前

    aliens.draw(screen)  # 绘制外星人

    # 显示得分
    sb.show_score()

    # 如果游戏处于非活动状态，就绘制按钮
    if not stats.game_active:
        play_button.draw_button()

    pygame.display.flip()  # 命令pygame让最近绘制的屏幕可见 擦出旧屏幕


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """更新子弹的位置、并删除已消失的子弹"""
    # 更新子弹位置
    bullets.update()
    # 这里没有创建实例的原因是在fire_bullets里面把属于Bullet类的bullet加入到了bullets精灵组里

    # 删除已消失子弹
    for bullet in bullets.copy():  # bullets的工作很繁杂 用copy减轻一下负担
        if bullet.rect.bottom <= 0:
            bullet.remove(bullets)

    check_bullet_alien_collision(ai_settings, screen, stats, sb, ship, aliens, bullets)


def check_bullet_alien_collision(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """响应子弹和外星人碰撞"""
    # 检查是否有子弹击中了外星人
    # 如果击中了，就删除子弹和外星人

    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    # 这个赋值语句是没有任何作用滴 有后半部分的groupcollide存在就行

    if len(aliens) == 0:  # 将屏幕上的所有外星人全部消灭了?
        # 删除现有的子弹，加快游戏速度，并创建新的一群外星人， 提升一个等级
        bullets.empty()
        ai_settings.increase_speed()
        create_fleet(ai_settings, screen, ship, aliens)  # 创建一个新的外星人舰队

        # 提升等级
        stats.level += 1
        sb.prep_level()

    if collisions:
        for aliens in collisions.values():  # collision中与每个子弹键相关的值都是一个列表，包含着被子弹撞到的外星人
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
    check_high_score(stats, sb)  # 每当有外星人被消灭就检测是否有最高分诞生


def get_number_alien_x(ai_settings, alien_width):
    """计算每行可容纳多少外星人"""
    available_space_x = ai_settings.screen_width - 2 * alien_width  # 计算每行的可用空间
    number_alien_x = int(available_space_x / (2 * alien_width))  # 计算可用空间内可以容纳多少外星人并取整
    return number_alien_x


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """创建一个外星人并将其放在当前行"""
    alien = Alien(ai_settings, screen)  # 创建一个外星人实例
    alien_width = alien.rect.width  # 把外星人外接矩形的宽度赋值给变量
    alien.x = alien_width + 2 * alien_width * alien_number  # 计算每一行新的外星人的x所在位置
    alien.rect.x = alien.x  # 将计算出的x赋值给每一行每一个新的外星人外接矩形的x值
    alien.y = alien.rect.height + 2 * alien.rect.height * row_number  # 计算每一行新的外星人的y所在位置
    alien.rect.y = alien.y  # 将计算出的y赋值给每一行每一个新的外星人的外接矩形的y值
    aliens.add(alien)  # 把每一个新的alien添加到aliens编组里


def create_fleet(ai_settings, screen, ship, aliens):
    """创建外星人群"""
    # 创建一个外星人，并计算每行可以容纳多少个外星人
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_alien_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    # 创建多行外星人
    for row_number in range(number_rows):  # 迭代出行号
        for alien_number in range(number_aliens_x):  # 迭代行号对应的X坐标
            create_alien(ai_settings, screen, aliens, alien_number, row_number)  # 在每一行都添加满外星人 再进行下一行的绘制


def get_number_rows(ai_settings, ship_height, alien_height):
    """计算屏幕可容纳多少行外星人"""
    available_space_y = (ai_settings.screen_height -
                         (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """响应被外星人撞到的飞船"""
    if stats.ships_left > 0:  # 还有剩余的飞船
        # 将ships_left -1
        stats.ships_left -= 1

        # 更新记分牌
        sb.prep_ships()

        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        # 创建一群新的外星人，并将飞船放到屏幕底端中央
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # 暂停
        sleep(0.5)
    else:  # 没有剩余的飞船
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """检查是否与外星人到达可屏幕底端"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # 像飞船被撞到一样进行处理
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break  # 代码块结尾一定要有一个break 有一个外星人触碰到了底端就退出for循环


def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """检查是否有外星人位于屏幕边缘，并更新整个外星人群的位置"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # 检测外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
    # 检查是否有外星人到达屏幕底端
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)


def check_fleet_edges(ai_settings, aliens):
    """有外星人到达屏幕边缘时采取相应措施"""
    for alien in aliens.sprites():  # 遍历精灵aliens组里的alien
        if alien.check_edges():  # 判断是否有alien撞到了屏幕啊
            change_fleet_direction(ai_settings, aliens)  # 改变舰队的方向
            break  # 代码块结尾一定要有一个break 有一个外星人触碰到了边缘就退出for循环


def change_fleet_direction(ai_settings, aliens):
    """将整个外星人群下移，并改变他们的方向"""
    for alien in aliens.sprites():  # 遍历精灵aliens组里的alien
        alien.rect.y += ai_settings.fleet_drop_speed  # 下移外星人舰队
    ai_settings.fleet_direction *= -1  # 改变下一次改变舰队的方向


def check_high_score(stats, sb):
    """检查是否诞生了新的最高分"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
        with open(file_name, "w") as obj_write:
            json.dump(stats.high_score, obj_write)

"""
def creat_fleet(ai_settings, screen, aliens):
    创建外星人舰队
    # 创建一个外星人，并计算一行可以容纳多少外星人
    # 外星人间距为外星人的宽度
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    available_space_x = ai_settings.screen_width - 2 * alien_width  # 计算每行的可用空间
    number_aliens_x = int(available_space_x / (2 * alien_width))  # 计算一行可以摆多少个外星人

    # 创建第一行外星人
    for alien_number in range(number_aliens_x):
        # 创建一个外星人并将其加入当前行
        alien = Alien(ai_settings, screen)
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        aliens.add(alien)
"""