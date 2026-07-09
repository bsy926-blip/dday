name: 디데이 배너 매일 갱신

on:
  schedule:
    - cron: '30 16 * * *' # 매일 한국시간 새벽 1시 30분 자동 재생성
  workflow_dispatch:      # 💡 [핵심] 수동 실행 버튼을 만드는 치트키 코드
  push:                   # 💡 [핵심] 파일이 바뀌면 즉시 런을 돌리는 코드
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.x'

      - name: Install Dependencies
        run: |
          python -m pip install --upgrade pip
          pip install pillow numpy

      - name: Run Script
        run: python generate.py

      - name: Commit and Push Changes
        run: |
          git config --global user.name "github-actions[bot]"
          git config --global user.email "41898282+github-actions[bot]@users.noreply.github.com"
          git add dday.png
          git diff-index --quiet HEAD || git commit -m "자동 갱신: dday.png"
          git push
