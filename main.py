import pygame
import sys
import random
import math
import os
from pygame import Color
from texiao import Firework, FlowerEffect  # 添加 FlowerEffect 的导入

# 全局定义
SCREEN_X = 1000
SCREEN_Y = 800
# 世界大小（比屏幕大10倍）
WORLD_X = SCREEN_X * 10
WORLD_Y = SCREEN_Y * 10
AI2_COLOR = (255, 165, 0)  # 第三条AI蛇颜色（橙色）

# 方向常量
DIRECTIONS = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]

# Button class for UI elements
class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        
    def draw(self, screen):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect, 0)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)
        
        # 使用兼容性更好的字体
        try:
            font = pygame.font.Font(None, 32)
        except:
            font = pygame.font.Font(None, 32)
            
        text_surface = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered:
                return True
        return False

# 滑块控件类
class Slider:
    def __init__(self, x, y, width, height, min_val, max_val, initial_val, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.handle_rect = pygame.Rect(x, y, 20, height)
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.color = color
        self.handle_color = (220, 220, 220)
        self.is_dragging = False
        self._update_handle_position()
        
    def _update_handle_position(self):
        value_range = self.max_val - self.min_val
        position_range = self.rect.width - self.handle_rect.width
        position = ((self.value - self.min_val) / value_range) * position_range
        self.handle_rect.x = self.rect.x + position
        
    def draw(self, screen):
        # 绘制滑槽
        pygame.draw.rect(screen, self.color, self.rect, 0)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 1)
        
        # 绘制滑块
        pygame.draw.rect(screen, self.handle_color, self.handle_rect, 0)
        pygame.draw.rect(screen, (100, 100, 100), self.handle_rect, 1)
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.handle_rect.collidepoint(event.pos):
                self.is_dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.is_dragging = False
        elif event.type == pygame.MOUSEMOTION and self.is_dragging:
            # 更新滑块位置
            new_x = event.pos[0]
            if new_x < self.rect.x:
                new_x = self.rect.x
            elif new_x > self.rect.x + self.rect.width - self.handle_rect.width:
                new_x = self.rect.x + self.rect.width - self.handle_rect.width
                
            self.handle_rect.x = new_x
            
            # 更新值
            position_range = self.rect.width - self.handle_rect.width
            value_range = self.max_val - self.min_val
            relative_pos = self.handle_rect.x - self.rect.x
            self.value = self.min_val + (relative_pos / position_range) * value_range
            
            return True
        return False

# 设置面板类
class SettingsPanel:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.active = False
        self.background_color = (50, 50, 50, 200)
        
        # 创建关闭按钮
        close_btn_size = 30
        self.close_button = Button(
            x + width - close_btn_size - 10, 
            y + 10, 
            close_btn_size, 
            close_btn_size, 
            "X", 
            (180, 30, 30), 
            (220, 50, 50)
        )
        
        # 创建音量滑块
        slider_width = width - 100
        self.volume_slider = Slider(
            x + 50, 
            y + 100, 
            slider_width, 
            20, 
            0.0, 
            1.0, 
            pygame.mixer.music.get_volume(), 
            (100, 100, 100)
        )
        
    def draw(self, screen):
        if not self.active:
            return
            
        # 创建半透明表面
        s = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        s.fill((50, 50, 50, 230))  # 半透明灰色
        screen.blit(s, (self.rect.x, self.rect.y))
        
        # 绘制边框
        pygame.draw.rect(screen, (200, 200, 200), self.rect, 2)
        
        # 绘制标题 - 使用兼容性更好的字体
        try:
            # 尝试加载中文字体
            font = pygame.font.Font(None, 36)  # 使用默认字体
            # 如果有中文字体文件，可以尝试加载
            # font = pygame.font.Font("simhei.ttf", 36)  # 黑体
        except:
            font = pygame.font.Font(None, 36)
            
        title = font.render("Game Settings", True, (255, 255, 255))
        title_rect = title.get_rect(center=(self.rect.centerx, self.rect.y + 40))
        screen.blit(title, title_rect)
        
        # 绘制音量标签
        try:
            font = pygame.font.Font(None, 24)
        except:
            font = pygame.font.Font(None, 24)
            
        volume_text = font.render(f"Volume: {int(self.volume_slider.value * 100)}%", True, (255, 255, 255))
        screen.blit(volume_text, (self.rect.x + 50, self.rect.y + 70))
        
        # 绘制滑块
        self.volume_slider.draw(screen)
        
        # 绘制关闭按钮
        self.close_button.draw(screen)
        
    def handle_event(self, event):
        if not self.active:
            return False
            
        # 处理关闭按钮事件
        if self.close_button.handle_event(event):
            self.active = False
            return True
            
        # 处理滑块事件
        if self.volume_slider.handle_event(event):
            pygame.mixer.music.set_volume(self.volume_slider.value)
            return True
            
        return self.rect.collidepoint(event.pos) if event.type == pygame.MOUSEBUTTONDOWN else False

# 蛇类
# 点以25为单位
class Bullet:
    def __init__(self, x, y, direction):
        self.rect = pygame.Rect(x-5, y-5, 10, 10)
        self.direction = direction
        self.speed = 20
        self.lifetime = 150  # 存活时间5秒（150帧）

    def update(self):
        if self.direction == pygame.K_LEFT:
            self.rect.x -= self.speed
        elif self.direction == pygame.K_RIGHT:
            self.rect.x += self.speed
        elif self.direction == pygame.K_UP:
            self.rect.y -= self.speed
        elif self.direction == pygame.K_DOWN:
            self.rect.y += self.speed
        self.lifetime -= 1
        # 检查是否在世界边界内和存活时间
        return (self.lifetime > 0 and 
                self.rect.colliderect(pygame.Rect(0, 0, WORLD_X, WORLD_Y)))

    def draw(self, screen, camera):
        # 将世界坐标转换为屏幕坐标
        screen_x, screen_y = camera.world_to_screen(self.rect.centerx, self.rect.centery)
        # 只在屏幕范围内绘制
        if 0 <= screen_x <= SCREEN_X and 0 <= screen_y <= SCREEN_Y:
            pygame.draw.circle(screen, (0, 0, 0), (int(screen_x), int(screen_y)), 5)

class Snake(object):
    # 初始化各种需要的属性 [开始时默认向右/身体块x5]
    def __init__(self, is_ai=False, start_pos=(0,0), color=(20,220,39)):
        self.bullets = []
        self.dirction = pygame.K_RIGHT
        self.body = []
        self.is_ai = is_ai
        self.color = color
        self.score = 0
        self.cooldown = 0  # 子弹冷却时间
        
        # 设置起始位置
        self.start_x, self.start_y = start_pos
        for x in range(5):
            self.addnode()
    
    # 发射子弹
    def shoot_bullet(self):
        if self.cooldown <= 0 and len(self.body) > 1:  # 确保蛇至少有两节才能发射子弹
            head = self.body[0]
            bullet_x = head.x + head.width // 2
            bullet_y = head.y + head.height // 2
            self.bullets.append(Bullet(bullet_x, bullet_y, self.dirction))
            self.cooldown = 15  # 设置冷却时间为1.5秒（15帧）
            
    # 更新子弹
    def update_bullets(self):
        if self.cooldown > 0:
            self.cooldown -= 1
            
        # 更新所有子弹
        self.bullets = [bullet for bullet in self.bullets if bullet.update()]
        
    # 无论何时 都在前端增加蛇块
    def addnode(self):
        left,top = (self.start_x, self.start_y)
        if self.body:
            left,top = (self.body[0].left,self.body[0].top)
        node = pygame.Rect(left,top,25,25)
        if self.dirction == pygame.K_LEFT:
            node.left -= 25
        elif self.dirction == pygame.K_RIGHT:
            node.left += 25
        elif self.dirction == pygame.K_UP:
            node.top -= 25
        elif self.dirction == pygame.K_DOWN:
            node.top += 25
        self.body.insert(0,node)
        
    # 删除最后一个块
    def delnode(self):
        if len(self.body) > 1:  # 确保蛇至少有一节
            self.body.pop()
    
    # 删除指定位置的块
    def remove_node_at(self, index):
        if 0 < index < len(self.body):  # 不能删除头部
            self.body.pop(index)
            return True
        return False
        
    # 死亡判断
    def isdead(self, other_snake=None):
        # 撞墙 - 现在检查世界边界而不是屏幕边界
        if self.body[0].x not in range(WORLD_X):
            return True
        if self.body[0].y not in range(WORLD_Y):
            return True
        # 撞自己
        if self.body[0] in self.body[1:]:
            return True
        # 撞另一条蛇
        if other_snake:
            if self.body[0] in other_snake.body:
                return True
        return False
        
    # 移动！
    def move(self):
        self.addnode()
        self.delnode()
        
    # 改变方向 但是左右、上下不能被逆向改变
    def changedirection(self,curkey):
        LR = [pygame.K_LEFT,pygame.K_RIGHT]
        UD = [pygame.K_UP,pygame.K_DOWN]
        if curkey in LR+UD:
            if (curkey in LR) and (self.dirction in LR):
                return
            if (curkey in UD) and (self.dirction in UD):
                return
            self.dirction = curkey
            
    # AI决策
    def ai_move(self, food):
        if not self.is_ai:
            return
            
        head = self.body[0]
        food_x = food.rect.x
        food_y = food.rect.y
        
        # 计算到食物的距离
        dx = food_x - head.x
        dy = food_y - head.y
        
        # 创建可能的移动选项
        possible_moves = []
        
        # 水平移动
        if dx > 0 and self.dirction != pygame.K_LEFT:
            possible_moves.append(pygame.K_RIGHT)
        elif dx < 0 and self.dirction != pygame.K_RIGHT:
            possible_moves.append(pygame.K_LEFT)
            
        # 垂直移动
        if dy > 0 and self.dirction != pygame.K_UP:
            possible_moves.append(pygame.K_DOWN)
        elif dy < 0 and self.dirction != pygame.K_DOWN:
            possible_moves.append(pygame.K_UP)
            
        # 如果没有直接移动选项，选择不会导致立即死亡的移动
        if not possible_moves:
            for direction in DIRECTIONS:
                if direction not in [pygame.K_LEFT, pygame.K_RIGHT] and self.dirction in [pygame.K_LEFT, pygame.K_RIGHT]:
                    possible_moves.append(direction)
                elif direction not in [pygame.K_UP, pygame.K_DOWN] and self.dirction in [pygame.K_UP, pygame.K_DOWN]:
                    possible_moves.append(direction)
        
        # 如果有可能的移动，随机选择一个
        if possible_moves:
            self.changedirection(random.choice(possible_moves))
        
        # AI随机发射子弹
        if random.random() < 0.1:  # 10%概率发射子弹
            self.shoot_bullet()

# 食物类
# 方法： 放置/移除
# 点以25为单位
class Food:
    def __init__(self):
        self.rect = pygame.Rect(-25,0,25,25)
        
    def remove(self):
        self.rect.x=-25
    
    def set(self):
        if self.rect.x == -25:
            allpos = []
            # 在整个世界范围内生成食物，不靠墙太近 25 ~ WORLD_X-25 之间
            for pos in range(25, WORLD_X-25, 25):
                allpos.append(pos)
            self.rect.left = random.choice(allpos)
            
            allpos_y = []
            for pos in range(25, WORLD_Y-25, 25):
                allpos_y.append(pos)
            self.rect.top = random.choice(allpos_y)
            print(self.rect)
            

def draw_snake_number(screen, rect, number):
    try:
        font = pygame.font.Font(None, 18)
    except:
        font = pygame.font.Font(None, 18)
    text = font.render(str(number), True, (255,255,255))
    text_rect = text.get_rect(center=rect.center)
    screen.blit(text, text_rect)

def show_text(screen, pos, text, color, font_bold = False, font_size = 60, font_italic = False):   
    #获取系统字体，并设置文字大小  
    try:
        cur_font = pygame.font.Font(None, font_size)
    except:
        cur_font = pygame.font.Font(None, font_size)
    #设置是否加粗属性  
    cur_font.set_bold(font_bold)  
    #设置是否斜体属性  
    cur_font.set_italic(font_italic)  
    #设置文字内容  
    text_fmt = cur_font.render(text, 1, color)  
    #绘制文字  
    screen.blit(text_fmt, pos)

# 摄像机类
class Camera:
    def __init__(self, screen_width, screen_height, world_width, world_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.world_width = world_width
        self.world_height = world_height
        self.x = 0
        self.y = 0
        self.border_threshold = 150  # 当玩家距离边缘多少像素时开始移动摄像机
        
    def update(self, target_x, target_y):
        """根据目标位置更新摄像机位置"""
        # 计算摄像机应该移动到的位置
        desired_x = target_x - self.screen_width // 2
        desired_y = target_y - self.screen_height // 2
        
        # 限制摄像机不超出世界边界
        self.x = max(0, min(desired_x, self.world_width - self.screen_width))
        self.y = max(0, min(desired_y, self.world_height - self.screen_height))
        
        # 平滑移动摄像机（避免跳跃）
        smooth_factor = 0.1
        current_center_x = self.x + self.screen_width // 2
        current_center_y = self.y + self.screen_height // 2
        
        # 只有当玩家接近边缘时才移动摄像机
        screen_target_x = target_x - self.x
        screen_target_y = target_y - self.y
        
        if (screen_target_x < self.border_threshold or 
            screen_target_x > self.screen_width - self.border_threshold or
            screen_target_y < self.border_threshold or 
            screen_target_y > self.screen_height - self.border_threshold):
            
            self.x += (desired_x - self.x) * smooth_factor
            self.y += (desired_y - self.y) * smooth_factor
            
            # 确保摄像机不超出边界
            self.x = max(0, min(self.x, self.world_width - self.screen_width))
            self.y = max(0, min(self.y, self.world_height - self.screen_height))
    
    def world_to_screen(self, world_x, world_y):
        """将世界坐标转换为屏幕坐标"""
        return world_x - self.x, world_y - self.y
    
    def screen_to_world(self, screen_x, screen_y):
        """将屏幕坐标转换为世界坐标"""
        return screen_x + self.x, screen_y + self.y

def main():
    pygame.init()
    # 加载并播放背景音乐
    pygame.mixer.init()
    pygame.mixer.music.load('music.mp3')
    pygame.mixer.music.set_volume(0.2)  # 设置音量为20%
    pygame.mixer.music.play(-1)  # -1 表示循环播放
    screen_size = (SCREEN_X, SCREEN_Y)
    screen = pygame.display.set_mode(screen_size)

    pygame.display.set_caption('贪吃蛇：起源')
    clock = pygame.time.Clock()
    isdead = False

    # 加载火星背景图片
    bg_img = pygame.image.load('mars_bg2.bmp')
    bg_img = pygame.transform.scale(bg_img, (SCREEN_X, SCREEN_Y))

    # 蛇/食物/特效
    player_snake = Snake(is_ai=False, start_pos=(WORLD_X // 6, WORLD_Y // 6), color=(20, 220, 39))
    ai_snake = Snake(is_ai=True, start_pos=(WORLD_X - 500, WORLD_Y - 500), color=(60, 255, 60))
    ai_snake2 = Snake(is_ai=True, start_pos=(WORLD_X // 2, WORLD_Y // 2), color=AI2_COLOR)
    food = Food()
    firework = Firework()
    flower_effect = FlowerEffect()  # 创建花朵特效实例

    # Create restart button (initially hidden)
    restart_button = Button(SCREEN_X // 2 - 100, 320, 200, 50, "Restart Game", (34, 139, 34), (50, 205, 50))
    
    # 创建设置按钮
    settings_button = Button(SCREEN_X - 120, 20, 100, 40, "Settings", (50, 50, 150), (70, 70, 180))
    
    # 创建设置面板
    settings_panel = SettingsPanel(SCREEN_X // 2 - 200, SCREEN_Y // 2 - 150, 400, 300)

    # 创建摄像机实例
    camera = Camera(SCREEN_X, SCREEN_Y, WORLD_X, WORLD_Y)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                player_snake.changedirection(event.key)
                # 玩家按空格发射子弹
                if event.key == pygame.K_SPACE and not isdead and not settings_panel.active:
                    player_snake.shoot_bullet()
                # 重新开始游戏
                if (event.key == pygame.K_SPACE or event.key == pygame.K_RETURN) and isdead:
                    return main()
                # 按ESC关闭设置面板
                if event.key == pygame.K_ESCAPE and settings_panel.active:
                    settings_panel.active = False
            
            # 处理设置按钮事件
            if settings_button.handle_event(event):
                settings_panel.active = True
                
            # 处理设置面板事件
            if settings_panel.handle_event(event):
                continue
                
            # Handle button events when dead
            if isdead:
                if restart_button.handle_event(event):
                    return main()
                
        # 绘制火星背景
        screen.blit(bg_img, (0, 0))

        # 移动蛇
        if not isdead and not settings_panel.active:
            player_snake.move()
            ai_snake.move()
            ai_snake2.move()
            ai_snake.ai_move(food)
            ai_snake2.ai_move(food)
            
            # 更新摄像机位置跟随玩家蛇
            if player_snake.body:
                player_head = player_snake.body[0]
                camera.update(player_head.x + player_head.width // 2, 
                            player_head.y + player_head.height // 2)
            
            # 更新所有蛇的子弹
            player_snake.update_bullets()
            ai_snake.update_bullets()
            ai_snake2.update_bullets()
            
            # 检测子弹碰撞
            # 检查玩家子弹与AI蛇的碰撞
            for bullet in player_snake.bullets[:]:
                for i, body_part in enumerate(ai_snake.body[1:], 1):  # 跳过头部
                    if bullet.rect.colliderect(body_part):
                        player_snake.bullets.remove(bullet)
                        ai_snake.remove_node_at(i)
                        break
                        
                for i, body_part in enumerate(ai_snake2.body[1:], 1):  # 跳过头部
                    if bullet in player_snake.bullets and bullet.rect.colliderect(body_part):
                        player_snake.bullets.remove(bullet)
                        ai_snake2.remove_node_at(i)
                        break
            
            # 检查AI蛇子弹与玩家的碰撞
            for bullet in ai_snake.bullets[:]:
                for i, body_part in enumerate(player_snake.body[1:], 1):  # 跳过头部
                    if bullet.rect.colliderect(body_part):
                        ai_snake.bullets.remove(bullet)
                        player_snake.remove_node_at(i)
                        break
                        
                for i, body_part in enumerate(ai_snake2.body[1:], 1):  # 跳过头部
                    if bullet in ai_snake.bullets and bullet.rect.colliderect(body_part):
                        ai_snake.bullets.remove(bullet)
                        ai_snake2.remove_node_at(i)
                        break
            
            # 检查AI蛇2子弹与其他蛇的碰撞
            for bullet in ai_snake2.bullets[:]:
                for i, body_part in enumerate(player_snake.body[1:], 1):  # 跳过头部
                    if bullet.rect.colliderect(body_part):
                        ai_snake2.bullets.remove(bullet)
                        player_snake.remove_node_at(i)
                        break
                        
                for i, body_part in enumerate(ai_snake.body[1:], 1):  # 跳过头部
                    if bullet in ai_snake2.bullets and bullet.rect.colliderect(body_part):
                        ai_snake2.bullets.remove(bullet)
                        ai_snake.remove_node_at(i)
                        break

        # 绘制平铺背景
        # 简单方法：绘制足够覆盖屏幕的背景瓦片
        tiles_x = (SCREEN_X // SCREEN_X) + 2  # 需要的水平瓦片数
        tiles_y = (SCREEN_Y // SCREEN_Y) + 2  # 需要的垂直瓦片数
        
        start_tile_x = int(camera.x // SCREEN_X)
        start_tile_y = int(camera.y // SCREEN_Y)
        
        for tile_x in range(start_tile_x, start_tile_x + tiles_x):
            for tile_y in range(start_tile_y, start_tile_y + tiles_y):
                world_x = tile_x * SCREEN_X
                world_y = tile_y * SCREEN_Y
                screen_x, screen_y = camera.world_to_screen(world_x, world_y)
                screen.blit(bg_img, (screen_x, screen_y))
            
        # 画玩家蛇（使用摄像机坐标）
        for rect in player_snake.body:
            screen_x, screen_y = camera.world_to_screen(rect.x, rect.y)
            # 只绘制在屏幕范围内的蛇身
            if (-25 <= screen_x <= SCREEN_X and -25 <= screen_y <= SCREEN_Y):
                screen_rect = pygame.Rect(screen_x, screen_y, rect.width, rect.height)
                pygame.draw.rect(screen, player_snake.color, screen_rect, 0)
            
        # 画AI蛇（使用摄像机坐标）
        for rect in ai_snake.body:
            screen_x, screen_y = camera.world_to_screen(rect.x, rect.y)
            if (-25 <= screen_x <= SCREEN_X and -25 <= screen_y <= SCREEN_Y):
                screen_rect = pygame.Rect(screen_x, screen_y, rect.width, rect.height)
                pygame.draw.rect(screen, ai_snake.color, screen_rect, 0)
                draw_snake_number(screen, screen_rect, 2)
            
        # 画第三条AI蛇（使用摄像机坐标）
        for rect in ai_snake2.body:
            screen_x, screen_y = camera.world_to_screen(rect.x, rect.y)
            if (-25 <= screen_x <= SCREEN_X and -25 <= screen_y <= SCREEN_Y):
                screen_rect = pygame.Rect(screen_x, screen_y, rect.width, rect.height)
                pygame.draw.rect(screen, ai_snake2.color, screen_rect, 0)
                draw_snake_number(screen, screen_rect, 10)
            
        # 绘制所有子弹
        for bullet in player_snake.bullets:
            bullet.draw(screen, camera)
        for bullet in ai_snake.bullets:
            bullet.draw(screen, camera)
        for bullet in ai_snake2.bullets:
            bullet.draw(screen, camera)
            
        # 检查死亡状态
        player_dead = player_snake.isdead(ai_snake) or player_snake.isdead(ai_snake2)
        ai_dead = ai_snake.isdead(player_snake) or ai_snake.isdead(ai_snake2)
        ai2_dead = ai_snake2.isdead(player_snake) or ai_snake2.isdead(ai_snake)
        isdead = player_dead or ai_dead or ai2_dead
        
        if isdead:
            if player_dead and ai_dead:
                show_text(screen,(SCREEN_X//2-200,200),'DRAW!',(227,29,18),False,100)
            elif player_dead:
                show_text(screen,(SCREEN_X//2-200,200),'AI WINS!',(227,29,18),False,100)
            else:
                show_text(screen,(SCREEN_X//2-200,200),'YOU WIN!',(227,29,18),False,100)
            restart_button.draw(screen)
            
        # 食物处理
        if food.rect == player_snake.body[0]:
            effect_x = food.rect.x + food.rect.width // 2
            effect_y = food.rect.y + food.rect.height // 2
            player_snake.score += 50
            food.remove()
            player_snake.addnode()
            firework.create_explosion(effect_x, effect_y)
        elif food.rect == ai_snake.body[0]:
            effect_x = food.rect.x + food.rect.width // 2
            effect_y = food.rect.y + food.rect.height // 2
            ai_snake.score += 50
            food.remove()
            ai_snake.addnode()
            firework.create_explosion(effect_x, effect_y)
        elif food.rect == ai_snake2.body[0]:
            effect_x = food.rect.x + food.rect.width // 2
            effect_y = food.rect.y + food.rect.height // 2
            ai_snake2.score += 50
            food.remove()
            ai_snake2.addnode()
            firework.create_explosion(effect_x, effect_y)
        
        # 食物投递
        food.set()
        # 绘制食物（使用摄像机坐标）
        food_screen_x, food_screen_y = camera.world_to_screen(food.rect.x, food.rect.y)
        if (0 <= food_screen_x <= SCREEN_X and 0 <= food_screen_y <= SCREEN_Y):
            food_screen_rect = pygame.Rect(food_screen_x, food_screen_y, food.rect.width, food.rect.height)
            pygame.draw.rect(screen, (136, 0, 21), food_screen_rect, 0)
        
        # 更新和绘制烟花特效
        firework.update()
        firework.draw(screen)
        
        # 显示分数文字
        show_text(screen,(50,500),'Player: '+str(player_snake.score),(223,223,223))
        show_text(screen,(50,550),'AI 1: '+str(ai_snake.score),(223,223,223))
        show_text(screen,(SCREEN_X-200,550),'AI 10: '+str(ai_snake2.score),(223,223,223))
        
        # 显示子弹使用提示
        if not isdead and not settings_panel.active:
            show_text(screen, (SCREEN_X // 2 - 180, 20), "Press SPACE to shoot", (255, 255, 255), False, 24)
        
        # 显示摄像机信息（调试用）
        show_text(screen, (10, 10), f"Camera: ({int(camera.x)}, {int(camera.y)})", (255, 255, 255), False, 16)
        
        # 显示世界位置信息
        if player_snake.body:
            player_world_x = player_snake.body[0].x
            player_world_y = player_snake.body[0].y
            world_progress_x = (player_world_x / WORLD_X) * 100
            world_progress_y = (player_world_y / WORLD_Y) * 100
            show_text(screen, (10, 30), f"World Position: {int(world_progress_x)}%, {int(world_progress_y)}%", 
                     (255, 255, 0), False, 16)
        
        # 绘制小地图
        minimap_size = 150
        minimap_x = SCREEN_X - minimap_size - 20
        minimap_y = SCREEN_Y - minimap_size - 80
        
        # 小地图背景
        minimap_surface = pygame.Surface((minimap_size, minimap_size), pygame.SRCALPHA)
        minimap_surface.fill((50, 50, 50, 180))
        screen.blit(minimap_surface, (minimap_x, minimap_y))
        
        # 小地图边框
        pygame.draw.rect(screen, (255, 255, 255), 
                        (minimap_x, minimap_y, minimap_size, minimap_size), 2)
        
        # 在小地图上显示玩家位置
        if player_snake.body:
            player_minimap_x = minimap_x + (player_snake.body[0].x / WORLD_X) * minimap_size
            player_minimap_y = minimap_y + (player_snake.body[0].y / WORLD_Y) * minimap_size
            pygame.draw.circle(screen, player_snake.color, 
                             (int(player_minimap_x), int(player_minimap_y)), 3)
        
        # 在小地图上显示AI蛇位置
        if ai_snake.body:
            ai_minimap_x = minimap_x + (ai_snake.body[0].x / WORLD_X) * minimap_size
            ai_minimap_y = minimap_y + (ai_snake.body[0].y / WORLD_Y) * minimap_size
            pygame.draw.circle(screen, ai_snake.color, 
                             (int(ai_minimap_x), int(ai_minimap_y)), 2)
        
        if ai_snake2.body:
            ai2_minimap_x = minimap_x + (ai_snake2.body[0].x / WORLD_X) * minimap_size
            ai2_minimap_y = minimap_y + (ai_snake2.body[0].y / WORLD_Y) * minimap_size
            pygame.draw.circle(screen, ai_snake2.color, 
                             (int(ai2_minimap_x), int(ai2_minimap_y)), 2)
        
        # 在小地图上显示食物位置
        if food.rect.x >= 0:
            food_minimap_x = minimap_x + (food.rect.x / WORLD_X) * minimap_size
            food_minimap_y = minimap_y + (food.rect.y / WORLD_Y) * minimap_size
            pygame.draw.circle(screen, (255, 0, 0), 
                             (int(food_minimap_x), int(food_minimap_y)), 2)
        
        # 小地图标题
        show_text(screen, (minimap_x, minimap_y - 25), "Mini Map", (255, 255, 255), False, 20)
        
        # 绘制设置按钮
        settings_button.draw(screen)
        
        # 绘制设置面板
        settings_panel.draw(screen)
        
        pygame.display.update()
        clock.tick(10)
    
if __name__ == '__main__':
    main()
