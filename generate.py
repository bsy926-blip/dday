#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
안양자이 헤리티온 입주 D-DAY 배너 자동 생성 스크립트
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

W, H = 1200, 600
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

# 폰트 경로 (레포의 fonts 폴더에 넣어둠)
FONT_DIR = os.path.join(os.path.dirname(__file__), "fonts")
def load(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)

f_top  = load("NotoSansKR-Regular.ttf", 40)
f_name = load("NotoSansKR-Bold.ttf", 60)
f_dday = load("NotoSansKR-Black.ttf", 190)
f_date = load("NotoSansKR-Regular.ttf", 36)
f_sub  = load("NotoSansKR-Regular.ttf", 34)

cx = W // 2
def center(y, text, font, fill, shadow=None):
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    x = cx - w // 2 - bbox[0]
    yy = y - bbox[1]
    if shadow:
        draw.text((x + 3, yy + 4), text, font=font, fill=shadow)
    draw.text((x, yy), text, font=font, fill=fill)

white = (255, 255, 255)
light = (203, 227, 255)
gold  = (255, 217, 102)
pale  = (226, 232, 240)

# 집 아이콘
def draw_house(cxi, cyi, s, color):
    draw.polygon([(cxi, cyi - s*0.55), (cxi - s*0.6, cyi - s*0.05),
                  (cxi + s*0.6, cyi - s*0.05)], fill=color)
    draw.rectangle([cxi - s*0.42, cyi - s*0.05, cxi + s*0.42, cyi + s*0.5], fill=color)

label = "우리 아파트 입주까지"
_bbox = draw.textbbox((0, 0), label, font=f_top)
_tw = _bbox[2] - _bbox[0]
draw_house(cx - _tw // 2 - 45, 88, 38, light)

center(70,  label, f_top, light)
center(135, APT_NAME, f_name, white)
center(225, dday_text, f_dday, gold, shadow=(0, 0, 0))
center(470, f"입주 예정일 : {TARGET.year}년 {TARGET.month}월 {TARGET.day}일", f_date, pale)
center(525, sub_text, f_sub, light)

# 둥근 모서리
mask = Image.new("L", (W, H), 0)
ImageDraw.Draw(mask).rounded_rectangle([0, 0, W-1, H-1], radius=40, fill=255)
out = Image.new("RGB", (W, H), (255, 255, 255))
out.paste(img, (0, 0), mask)
out.save("dday.png")
print(f"생성 완료: {dday_text} ({sub_text})")
