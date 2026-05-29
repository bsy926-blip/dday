# 안양자이 헤리티온 입주 D-DAY 자동 배너

매일 새벽에 자동으로 "D-숫자" 배너 이미지를 새로 그려서 저장합니다.
카페 대문에는 이미지 주소만 넣어두면 매일 자동 갱신됩니다.

---

## 처음 한 번만 세팅하기 (약 10~15분)

### 1단계. GitHub 가입
- https://github.com 접속 → 우측 상단 Sign up → 이메일/비번 입력해서 무료 가입

### 2단계. 새 저장소(레포) 만들기
- 가입 후 우측 상단 + 버튼 → New repository
- Repository name 칸에 아무 이름 입력 (예: `dday`)
- **Public** 선택 (꼭 Public 이어야 이미지가 카페에서 보입니다)
- 아래 초록색 Create repository 버튼 클릭

### 3단계. 파일 올리기
- 만들어진 저장소 화면에서 "uploading an existing file" 링크 클릭
  (또는 Add file → Upload files)
- 이 폴더 안의 **모든 파일과 폴더**를 드래그해서 올립니다:
  - generate.py
  - fonts 폴더 (안에 폰트 3개)
  - .github 폴더 (안에 workflows/update.yml)
  - dday.png
- ※ 폴더째 올라가지 않으면, github에서 폴더를 만들어 그 안에 올리세요.
- 맨 아래 Commit changes 클릭

### 4단계. 자동 실행 권한 켜기
- 저장소 상단 메뉴 Settings → 왼쪽 Actions → General
- 맨 아래 "Workflow permissions" 에서
  **Read and write permissions** 선택 → Save

### 5단계. 한 번 직접 실행해서 테스트
- 상단 메뉴 Actions 탭 클릭
- 좌측 "디데이 배너 매일 갱신" 클릭 → 우측 "Run workflow" 버튼 클릭
- 1~2분 뒤 초록색 체크가 뜨면 성공!

### 6단계. 이미지 주소 확인
- 저장소 첫 화면에서 dday.png 클릭 → "Download" 또는 이미지 우클릭 → 이미지 주소 복사
- 주소는 보통 이런 형태입니다:
  `https://raw.githubusercontent.com/(내아이디)/dday/main/dday.png`

---

## 카페 대문에 넣기

아래 코드의 주소 부분을 위에서 복사한 내 주소로 바꿔서, 카페 대문 HTML에 붙여넣으세요.
(cafe_embed.html 파일 참고)

```html
<img src="https://raw.githubusercontent.com/내아이디/dday/main/dday.png?v=1"
     alt="입주 D-DAY" style="max-width:100%;border-radius:20px;">
```

끝! 이제 매일 새벽 0시 10분에 자동으로 숫자가 바뀝니다.

---

## 자주 묻는 질문

**Q. 돈 드나요?**
공개(Public) 저장소는 GitHub Actions가 완전 무료입니다. 평생 무료입니다.

**Q. 날짜나 단지명을 바꾸고 싶어요.**
generate.py 파일 맨 위의 TARGET(날짜)와 APT_NAME(단지명)만 수정하면 됩니다.

**Q. 이미지가 카페에서 안 바뀌어요.**
브라우저가 옛 이미지를 기억하는 경우입니다. 코드의 `?v=1` 을 `?v=2`, `?v=3`
처럼 숫자만 바꿔주면 새로 불러옵니다.
