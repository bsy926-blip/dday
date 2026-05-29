#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
안양자이 헤리티온 입주 D-DAY 배너 자동 생성 (960x300 가로형)
매일 GitHub Actions가 실행 -> dday.png 를 새로 그려서 저장
"""
from PIL import Image, ImageDraw, ImageFont
from datetime import date
import numpy as np
import os

# ===== 설정 (입주 예정일) =====
TARGET = date(2029, 9, 1)
APT_NAME = "안양자이 헤리티온"
# ============================

today = date.today()
diff = (TARGET - today).days

if diff > 0:
    dday_text = f"D-{diff}"
    years = diff // 365
    months = (diff % 365) // 30
    sub_text = f"약 {years}년 {months}개월 남았습니다"
elif diff == 0:
    dday_text = "D-DAY"
    sub_text = "드디어 입주일입니다!"
else:
    dday_text = f"D+{abs(diff)}"
    sub_text = "입주를 축하합니다!"

W, H = 960, 300
top = np.array([30, 58, 95])
mid = np.array([44, 82, 130])
bot = np.array([49, 130, 206])

arr = np.zeros((H, W, 3), dtype=np.uint8)
for y in range(H):
    t = y / (H - 1)
    if t < 0.5:
        c = top + (mid - top) * (t / 0.5)
    else:
        c = mid + (bot - mid) * ((t - 0.5) / 0.5)
    arr[y, :] = c
img = Image.fromarray(arr).convert("RGB")
draw = ImageDraw.Draw(img)

FONT_DIR = os.path.join(os.path.dirname(__file__), "fonts")
def load(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)

f_top  = load("NotoSansKR-Regular.ttf", 26)
f_name = load("NotoSansKR-Bold.ttf", 40)
f_dday = load("NotoSansKR-Black.ttf", 130)
f_date = load("NotoSansKR-Regular.ttf", 22)
f_sub  = load("NotoSansKR-Regular.ttf", 22)

white = (255, 255, 255)
light = (203, 227, 255)
gold  = (255, 217, 102)
pale  = (226, 232, 240)

def text_left(x, y, text, font, fill, shadow=None):
    bbox = draw.textbbox((0, 0), text, font=font)
    yy = y - bbox[1]
    if shadow:
        draw.text((x + 2, yy + 3), text, font=font, fill=shadow)
    draw.text((x - bbox[0], yy), text, font=font, fill=fill)
    return bbox[2] - bbox[0]

LX = 55
def draw_house(cxi, cyi, s, color):
    draw.polygon([(cxi, cyi - s*0.55), (cxi - s*0.6, cyi - s*0.05),
                  (cxi + s*0.6, cyi - s*0.05)], fill=color)
    draw.rectangle([cxi - s*0.42, cyi - s*0.05, cxi + s*0.42, cyi + s*0.5], fill=color)

draw_house(LX + 11, 70, 24, light)
text_left(LX + 32, 60, "우리 아파트 입주까지", f_top, light)
text_left(LX, 95, APT_NAME, f_name, white)
text_left(LX, 175, "입주 예정일", f_date, pale)
text_left(LX, 205, f"{TARGET.year}년 {TARGET.month}월 {TARGET.day}일", f_sub, light)

bbox = draw.textbbox((0, 0), dday_text, font=f_dday)
dw = bbox[2] - bbox[0]
RX = W - 55 - dw
dy = 95
draw.text((RX - bbox[0] + 3, dy - bbox[1] + 4), dday_text, font=f_dday, fill=(0, 0, 0))
draw.text((RX - bbox[0], dy - bbox[1]), dday_text, font=f_dday, fill=gold)

sb = draw.textbbox((0, 0), sub_text, font=f_sub)
sw = sb[2] - sb[0]
draw.text((W - 55 - sw - sb[0], 235 - sb[1]), sub_text, font=f_sub, fill=light)

img.save("dday.png")
print(f"생성 완료: {dday_text} ({sub_text}) / 960x300")
