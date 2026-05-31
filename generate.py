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
TARGET = date(2029, 9, 30)
APT_NAME = "안양자이 헤리티온"
# ============================

# GitHub 서버에서도 무조건 한국 시간(KST) 기준으로 오늘 날짜를 계산하도록 설정
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

# 좌측 정렬 텍스트 출력 함수
def text_left(x, y, text, font, fill, shadow=None):
    bbox = draw.textbbox((0, 0), text, font=font)
    yy = y - bbox[1]
    if shadow:
        draw.text((x + 2*S - bbox[0], yy + 2*S), text, font=font, fill=shadow)
    draw.text((x - bbox[0], yy), text, font=font, fill=fill)
    return bbox[2] - bbox[0]

LX = 48*S
# 💡 [이 부분이 잘려 있었습니다] 정상적으로 복구된 집 아이콘 함수
def draw_house(cxi, cyi, s, color):
    draw.polygon([(cxi, cyi - s*0.55), (cxi - s*0.6, cyi - s*0.05),
                  (cxi + s*0.6, cyi - s*0.05)], fill=color)
    draw.rectangle([cxi - s*0.42, cyi - s*0.05, cxi + s*0.42, cyi + s*0.5], fill=color)

# 왼쪽 영역 그리기
draw_house(LX + 10*S, 34*S, 17*S, light)
text_left(LX + 26*S, 31*S, "우리 아파트 입주까지", f_top, light)
text_left(LX, 56*S, APT_NAME, f_name, white)
text_left(LX, 105*S, f"입주 예정일 : {TARGET.year}년 {TARGET.month}월 {TARGET.day}일", f_sub, light)

# 오른쪽 큰 D-DAY 그리기 (세로 중앙)
bbox = draw.textbbox((0, 0), dday_text, font=f_dday)
dw = bbox[2] - bbox[0]
dh = bbox[3] - bbox[1]
RX = W - 50*S - dw
dy = (H - dh)//2

draw.text((RX - bbox[0] + 3*S, dy - bbox[1] + 3*S), dday_text, font=f_dday, fill=(0, 0, 0, 100))
draw.text((RX - bbox[0], dy - bbox[1]), dday_text, font=f_dday, fill=gold)

# D-DAY 아래 작은 안내
sb = draw.textbbox((0, 0), sub_text, font=f_sub)
sw = sb[2] - sb[0]
draw.text((W - 50*S - sw - sb[0], 122*S - sb[1]), sub_text, font=f_sub, fill=light)

# 이미지 저장
img.save("dday.png")
print(f"생성 완료: {dday_text} ({sub_text}) / {W}x{H} (표시 {BW}x{BH})")
