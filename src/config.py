"""
AI News Telegram Bot - Configuration
"""
import os
from dataclasses import dataclass
from enum import Enum

# === API Keys ===
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# === Priority Levels ===
class Priority(Enum):
    REALTIME = "realtime"      # 즉시 전송 (중요도 8-10)
    BATCH_6H = "batch_6h"      # 6시간 배치 (중요도 5-7)
    DAILY = "daily"            # 일일 요약 (중요도 1-4)

# === Source Configuration ===
@dataclass
class NewsSource:
    name: str
    url: str
    source_type: str  # rss, reddit, twitter_nitter, hackernews
    base_trust: int   # 1-10 기본 신뢰도
    category: str     # official, personal, community, academic

# === News Sources ===
NEWS_SOURCES = [
    # === 공식 블로그 (최고 신뢰도) ===
    NewsSource(
        name="OpenAI Blog",
        url="https://openai.com/news/rss.xml",
        source_type="rss",
        base_trust=10,
        category="official"
    ),
    NewsSource(
        name="Anthropic Research",
        url="https://www.anthropic.com/research/rss.xml",
        source_type="rss",
        base_trust=10,
        category="official"
    ),
    NewsSource(
        name="Google AI Blog",
        url="https://blog.google/technology/ai/rss/",
        source_type="rss",
        base_trust=10,
        category="official"
    ),
    NewsSource(
        name="DeepMind Blog",
        url="https://deepmind.google/blog/rss.xml",
        source_type="rss",
        base_trust=10,
        category="official"
    ),
    NewsSource(
        name="Microsoft AI Blog",
        url="https://blogs.microsoft.com/ai/feed/",
        source_type="rss",
        base_trust=10,
        category="official"
    ),
    
    # === 신뢰할 수 있는 뉴스 매체 ===
    NewsSource(
        name="MIT Technology Review AI",
        url="https://www.technologyreview.com/topic/artificial-intelligence/feed",
        source_type="rss",
        base_trust=9,
        category="official"
    ),
    NewsSource(
        name="Wired AI",
        url="https://www.wired.com/feed/tag/ai/latest/rss",
        source_type="rss",
        base_trust=8,
        category="official"
    ),
    NewsSource(
        name="TechCrunch AI",
        url="https://techcrunch.com/category/artificial-intelligence/feed/",
        source_type="rss",
        base_trust=8,
        category="official"
    ),
    NewsSource(
        name="VentureBeat AI",
        url="https://venturebeat.com/category/ai/feed/",
        source_type="rss",
        base_trust=8,
        category="official"
    ),
    
    # === 개인 뉴스레터 (검증된 전문가) ===
    NewsSource(
        name="Simon Willison Blog",
        url="https://simonwillison.net/atom/everything/",
        source_type="rss",
        base_trust=9,
        category="personal"
    ),
    NewsSource(
        name="Lil'Log (Lilian Weng)",
        url="https://lilianweng.github.io/index.xml",
        source_type="rss",
        base_trust=9,
        category="personal"
    ),
    NewsSource(
        name="AI Snake Oil",
        url="https://www.aisnakeoil.com/feed",
        source_type="rss",
        base_trust=8,
        category="personal"
    ),
    
    # === 학술 ===
    NewsSource(
        name="arXiv cs.AI",
        url="https://rss.arxiv.org/rss/cs.AI",
        source_type="rss",
        base_trust=9,
        category="academic"
    ),
    NewsSource(
        name="arXiv cs.LG",
        url="https://rss.arxiv.org/rss/cs.LG",
        source_type="rss",
        base_trust=9,
        category="academic"
    ),
    NewsSource(
        name="arXiv cs.CL",
        url="https://rss.arxiv.org/rss/cs.CL",
        source_type="rss",
        base_trust=9,
        category="academic"
    ),
    
    # === YouTube (영상) ===
    NewsSource(
        name="Two Minute Papers",
        url="https://www.youtube.com/feeds/videos.xml?channel_id=UCbfYPyITQ-7l4upoX8nvctg",
        source_type="rss",
        base_trust=8,
        category="personal"
    ),
    NewsSource(
        name="Yannic Kilcher",
        url="https://www.youtube.com/feeds/videos.xml?channel_id=UCZHmQk67mSJgfCCTn7xBfew",
        source_type="rss",
        base_trust=8,
        category="personal"
    ),
]

# === Importance Keywords (중요도 높이는 키워드) ===
HIGH_IMPORTANCE_KEYWORDS = [
    # 주요 모델/제품 출시
    "gpt-5", "gpt5", "claude 4", "claude-4", "gemini 2", "llama 4",
    "release", "launch", "announce", "발표", "출시",
    
    # 주요 기업
    "openai", "anthropic", "google deepmind", "meta ai",
    
    # 중요 이벤트
    "breakthrough", "sota", "state-of-the-art", "benchmark",
    "agi", "safety", "alignment", "regulation", "법안",
    
    # 주요 인물
    "sam altman", "dario amodei", "demis hassabis", "yann lecun",
    "andrej karpathy", "ilya sutskever",
]

# === Filter Keywords (제외할 키워드) ===
EXCLUDE_KEYWORDS = [
    "sponsor", "advertisement", "promoted", "job posting",
]

# === Settings ===
MAX_NEWS_PER_BATCH = 10  # 배치당 최대 뉴스 수
SUMMARY_MAX_LENGTH = 300  # 요약 최대 글자 수
CACHE_HOURS = 48  # 중복 체크 기간 (시간)
