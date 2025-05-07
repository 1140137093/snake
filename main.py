import pygame
import sys
import random
import math
from pygame import Color
from texiao import Firework  # Add this import at the top

# 全局定义
SCREEN_X = 1000
SCREEN_Y = 800
#BACKGROUND_COLOR = Color('blue')

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
        
        font = pygame.font.SysFont("宋体", 32)
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

# 蛇类
# 点以25为单位
class Snake(object):
    # 初始化各种需要的属性 [开始时默认向右/身体块x5]
    def __init__(self, is_ai=False, start_pos=(0,0), color=(20,220,39)):
        self.dirction = pygame.K_RIGHT
        self.body = []
        self.is_ai = is_ai
        self.color = color
        self.score = 0
        
        # 设置起始位置
        self.start_x, self.start_y = start_pos
        for x in range(5):
            self.addnode()
        
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
        self.body.pop()
        
    # 死亡判断
    def isdead(self, other_snake=None):
        # 撞墙
        if self.body[0].x not in range(SCREEN_X):
            return True
        if self.body[0].y not in range(SCREEN_Y):
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
            # 不靠墙太近 25 ~ SCREEN_X-25 之间
            for pos in range(25,SCREEN_X-25,25):
                allpos.append(pos)
            self.rect.left = random.choice(allpos)
            self.rect.top  = random.choice(allpos)
            print(self.rect)
            

def show_text(screen, pos, text, color, font_bold = False, font_size = 60, font_italic = False):   
    #获取系统字体，并设置文字大小  
    cur_font = pygame.font.SysFont("宋体", font_size)  
    #设置是否加粗属性  
    cur_font.set_bold(font_bold)  
    #设置是否斜体属性  
    cur_font.set_italic(font_italic)  
    #设置文字内容  
    text_fmt = cur_font.render(text, 1, color)  
    #绘制文字  
    screen.blit(text_fmt, pos)

class ColorBackground:
    def __init__(self):
        self.hue = 0
        self.colors = [(0, 0, 0) for _ in range(4)]  # 四个角的颜色
        self.update_colors()
        self.background_surface = pygame.Surface((SCREEN_X, SCREEN_Y))
        self.last_update = 0
        
    def update_colors(self):
        # 更新四个角的颜色
        self.hue = (self.hue + 0.5) % 360
        base_hue = self.hue
        for i in range(4):
            hue = (base_hue + i * 90) % 360
            # HSV to RGB conversion
            h = hue / 60
            c = 0.7  # 色彩饱和度
            x = c * (1 - abs(h % 2 - 1))
            
            if 0 <= h < 1: rgb = (c, x, 0)
            elif 1 <= h < 2: rgb = (x, c, 0)
            elif 2 <= h < 3: rgb = (0, c, x)
            elif 3 <= h < 4: rgb = (0, x, c)
            elif 4 <= h < 5: rgb = (x, 0, c)
            else: rgb = (c, 0, x)
            
            # 调整亮度
            m = 0.3
            self.colors[i] = tuple(int((c + m) * 255) for c in rgb)
    
    def draw(self, screen):
        current_time = pygame.time.get_ticks()
        # 每100ms才更新一次背景
        if current_time - self.last_update > 100:
            self.update_colors()
            self.last_update = current_time
            
            # 在临时surface上绘制背景
            for y in range(0, SCREEN_Y, 4):  # 增加步长到4以提高性能
                for x in range(0, SCREEN_X, 4):
                    tx = x / SCREEN_X
                    ty = y / SCREEN_Y
                    
                    c1 = [int(self.colors[0][i] * (1-tx) + self.colors[1][i] * tx) for i in range(3)]
                    c2 = [int(self.colors[2][i] * (1-tx) + self.colors[3][i] * tx) for i in range(3)]
                    color = [int(c1[i] * (1-ty) + c2[i] * ty) for i in range(3)]
                    
                    pygame.draw.rect(self.background_surface, color, (x, y, 4, 4))
                    
        # 直接将预渲染的背景绘制到屏幕上
        screen.blit(self.background_surface, (0, 0))

def main():
    pygame.init()
    screen_size = (SCREEN_X,SCREEN_Y)
    screen = pygame.display.set_mode(screen_size)

    pygame.display.set_caption('Snake')
    clock = pygame.time.Clock()
    isdead = False
    
    # 蛇/食物/特效/背景
    player_snake = Snake(is_ai=False, start_pos=(100,100), color=(20,220,39))
    ai_snake = Snake(is_ai=True, start_pos=(SCREEN_X-200,SCREEN_Y-200), color=(220,20,60))
    food = Food()
    firework = Firework()
    background = ColorBackground()
    
    # Create restart button (initially hidden)
    restart_button = Button(SCREEN_X//2 - 100, 320, 200, 50, "Restart Game", (34, 139, 34), (50, 205, 50))
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                player_snake.changedirection(event.key)
                if (event.key == pygame.K_SPACE or event.key == pygame.K_RETURN) and isdead:
                    return main()
            
            # Handle button events when dead
            if isdead:
                if restart_button.handle_event(event):
                    return main()
                
        # 绘制彩色背景
        background.draw(screen)
        
        # 移动蛇
        if not isdead:
            player_snake.move()
            ai_snake.move()
            ai_snake.ai_move(food)
            
        # 画玩家蛇
        for rect in player_snake.body:
            pygame.draw.rect(screen, player_snake.color, rect, 0)
            
        # 画AI蛇
        for rect in ai_snake.body:
            pygame.draw.rect(screen, ai_snake.color, rect, 0)
            
        # 检查死亡状态
        player_dead = player_snake.isdead(ai_snake)
        ai_dead = ai_snake.isdead(player_snake)
        isdead = player_dead or ai_dead
        
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
        
        # 食物投递
        food.set()
        pygame.draw.rect(screen,(136,0,21),food.rect,0)
        
        # 更新和绘制烟花特效
        firework.update()
        firework.draw(screen)
        
        # 显示分数文字
        show_text(screen,(50,500),'Player: '+str(player_snake.score),(223,223,223))
        show_text(screen,(50,550),'AI: '+str(ai_snake.score),(223,223,223))
        
        pygame.display.update()
        clock.tick(10)
    
if __name__ == '__main__':
    main()