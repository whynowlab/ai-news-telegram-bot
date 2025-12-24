# 🤖 AI News Telegram Bot

AI/ML 분야의 최신 뉴스를 수집하고, Gemini AI로 분석하여 텔레그램으로 전송하는 봇입니다.

## ✨ 기능

- **신뢰도 기반 소스**: 공식 블로그, 검증된 전문가, 커뮤니티, 학술 자료
- **AI 중요도 분석**: Gemini가 뉴스 중요도를 1-10으로 평가
- **스마트 알림**: 
  - 🚨 **실시간** (30분): 중요도 8+ 즉시 전송
  - 📢 **6시간 배치**: 중요도 5-7 모아서 전송
  - 📰 **일일 요약**: 전체 뉴스 요약
- **한국어 요약**: 영문 뉴스도 한국어로 요약

## 📡 뉴스 소스

| 카테고리 | 소스 | 신뢰도 |
|---------|------|-------|
| 공식 | OpenAI, Anthropic, Google AI, DeepMind, Meta AI | ⭐⭐⭐⭐⭐ |
| 미디어 | MIT Tech Review, The Verge, TechCrunch, Ars Technica | ⭐⭐⭐⭐ |
| 개인 | The Batch (Andrew Ng), Import AI (Jack Clark), Ahead of AI | ⭐⭐⭐⭐ |
| 커뮤니티 | Hacker News, Reddit ML, Reddit LocalLLaMA | ⭐⭐⭐ |
| 학술 | arXiv cs.AI, arXiv cs.LG | ⭐⭐⭐⭐⭐ |

## 🚀 설치 방법

### 1. Fork & Clone
```bash
git clone https://github.com/YOUR_USERNAME/ai-news-telegram-bot.git
cd ai-news-telegram-bot
```

### 2. GitHub Secrets 설정
Repository → Settings → Secrets and variables → Actions

| Secret Name | 값 |
|-------------|---|
| `TELEGRAM_BOT_TOKEN` | 텔레그램 봇 토큰 (@BotFather) |
| `TELEGRAM_CHAT_ID` | 본인 Chat ID |
| `GEMINI_API_KEY` | Google Gemini API 키 |

### 3. Push하면 자동 시작!
```bash
git push origin main
```

## 📅 자동 실행 스케줄

| 워크플로우 | 주기 | 설명 |
|-----------|-----|------|
| `realtime.yml` | 30분마다 | 중요 뉴스 즉시 알림 |
| `batch.yml` | 6시간마다 | 중간 중요도 뉴스 모음 |
| `daily.yml` | 매일 오전 9시 (KST) | 일일 요약 |

## 🧪 로컬 테스트

```bash
# 환경변수 설정
export TELEGRAM_BOT_TOKEN="your_token"
export TELEGRAM_CHAT_ID="your_chat_id"
export GEMINI_API_KEY="your_api_key"

# 의존성 설치
pip install -r requirements.txt

# 테스트 실행
cd src
python main.py --mode test

# 각 모드 실행
python main.py --mode realtime
python main.py --mode batch
python main.py --mode daily
```

## 📁 프로젝트 구조

```
ai-news-telegram-bot/
├── .github/workflows/
│   ├── realtime.yml    # 30분마다 실시간 체크
│   ├── batch.yml       # 6시간 배치
│   ├── daily.yml       # 일일 요약
│   └── test.yml        # 연결 테스트
├── src/
│   ├── config.py       # 설정 및 소스 목록
│   ├── news_collector.py  # RSS 뉴스 수집
│   ├── ai_analyzer.py  # Gemini AI 분석
│   ├── telegram_bot.py # 텔레그램 전송
│   └── main.py         # 메인 실행
├── data/
│   └── seen_news.json  # 중복 방지 캐시 (자동 생성)
├── requirements.txt
└── README.md
```

## 🔧 커스터마이징

### 소스 추가/수정
`src/config.py`의 `NEWS_SOURCES` 리스트 수정

### 중요도 기준 변경
`src/ai_analyzer.py`의 프롬프트 또는 점수 계산 로직 수정

### 알림 주기 변경
`.github/workflows/` 내 cron 표현식 수정

## 📝 라이선스

MIT License - 자유롭게 사용하세요!
