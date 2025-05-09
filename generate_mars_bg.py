from PIL import Image, ImageDraw, ImageFilter
import random

# ����������ɫ����
width, height = 1920, 1080
img = Image.new('RGB', (width, height), (180, 60, 30))
draw = ImageDraw.Draw(img)

# ��һЩ���Ǳ����"����"��"��ʯ"
for _ in range(80):
    x1 = random.randint(0, width)
    y1 = random.randint(int(height*0.4), height)
    x2 = x1 + random.randint(-200, 200)
    y2 = y1 + random.randint(20, 120)
    color = (random.randint(120, 200), random.randint(40, 80), random.randint(20, 40))
    width_line = random.randint(2, 8)
    draw.line((x1, y1, x2, y2), fill=color, width=width_line)

# ��һЩ"��ʯ��"
for _ in range(30):
    x = random.randint(0, width)
    y = random.randint(int(height*0.5), height)
    r = random.randint(20, 60)
    color = (random.randint(100, 180), random.randint(30, 60), random.randint(20, 40))
    draw.ellipse((x-r, y-r, x+r, y+r), outline=color, width=3)

# �����΢ģ�������
img = img.filter(ImageFilter.GaussianBlur(radius=1))
pixels = img.load()
for i in range(width):
    for j in range(height):
        if random.random() < 0.01:
            r, g, b = pixels[i, j]
            pixels[i, j] = (min(255, r+random.randint(-20, 20)), max(0, g+random.randint(-10, 10)), max(0, b+random.randint(-10, 10)))

img.save('mars_bg2.bmp')
print("���Ǳ���ͼƬ�ѱ���Ϊ mars_bg2.bmp") 