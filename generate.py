#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
안양자이 헤리티온 입주 D-DAY 배너 자동 생성
표시 크기 960x150, 선명하게 2배 해상도(1920x300)로 생성
"""
from PIL import Image, ImageDraw, ImageFont
from datetime import date, datetime, timedelta, timezone
import numpy as np
import os

# ===== 설정 (입주 예정일) =====
TARGET = date(2029, 9, 1)
APT_NAME = "안양자이 헤리티온"
# ============================

# 💡 [수정] GitHub 서버(UTC)에서도 무조건 한국 시간(KST) 기준으로 오늘 날짜를 계산하도록 설정
kst_zone = timezone(timedelta(hours=9))
today = datetime.now(kst_zone).date()

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

# 표시 960x150 의 2배 해상도
S = 2
BW, BH = 960, 150          # 기준(표시) 크기
W, H = BW*S, BH*S          # 실제 생성 크기 1920x300

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
    try:
        return ImageFont.truetype(os.path.join(FONT_DIR, name), int(size*S))
    except OSError:
        print(f"경고: {name} 폰트를 찾을 수 없어 기본 폰트를 사용합니다.")
        return ImageFont.load_default()

# 폰트/위치 지정
f_top  = load("NotoSansKR-Regular.ttf", 19)
f_name = load("NotoSansKR-Bold.ttf", 33)
f_dday = load("NotoSansKR-Black.ttf", 92)
f_sub  = load("NotoSansKR-Regular.ttf", 17)

white = (255, 255, 255)
light = (203, 227, 255)
gold  = (255, 217, 102)

# 좌측 정렬 텍스트 출력 함수 (오류 수정 완료)
def text_left(x, y, text, font, fill, shadow=None):
    bbox = draw.textbbox((0, 0), text, font=font)
    yy = y - bbox[1]
    if shadow:
        draw.text((x + 2*S - bbox[0], yy + 2*S), text, font=font, fill=shadow)
    draw.text((x - bbox[0], yy), text, font=font, fill=fill)
    return bbox[2] - bbox[0]

LX = 48*S
def draw_house(cxi, cy
