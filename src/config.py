"""
AI News Telegram Bot - Configuration
(OpenRouter 버전)
"""
import os
from dataclasses import dataclass
from enum import Enum

# === API Keys ===
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# OpenRouter API 키 (Gemini 대체)
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")

# 기존 Gemini 키 (더 이상 사용 안함, 호환성 유지)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# === Priority Levels ===
class Priority(Enum):
    REALTIME = "realtime"
    BATCH_6H = "batch_6h"
    DAILY = "daily"

# === Source Configuration ===
@dataclass
class NewsSource:
    name: str
    url: str
    source_type: str
    base_trust: int
    category: str

# === News Sources ===
NEWS_SOURCES = [
    # === 공식 블로그 (최고 신뢰도 10) ===
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
    NewsSource(
        name="Meta AI Blog",
        url="https://ai.meta.com/blog/rss/",
        source_type="rss",
        base_trust=10,
        category="official"
    ),
    NewsSource(
        name="NVIDIA AI Blog",
        url="https://blogs.nvidia.com/feed/",
        source_type="rss",
        base_trust=10,
        category="official"
    ),
    NewsSource(
        name="Hugging Face Blog",
        url="https://huggingface.co/blog/feed.xml",
        source_type="rss",
        base_trust=9,
        category="official"
    ),
    
    # === 신뢰할 수 있는 뉴스 매체 (8-9) ===
    NewsSource(
        name="MIT Technology Review AI",
        url="https://www.technologyreview.com/topic/artificial-intelligence/feed",
        source_type="rss",
        base_trust=9,
        category="media"
    ),
    NewsSource(
        name="Wired AI",
        url="https://www.wired.com/feed/tag/ai/latest/rss",
        source_type="rss",
        base_trust=8,
        category="media"
    ),
    NewsSource(
        name="TechCrunch AI",
        url="https://techcrunch.com/category/artificial-intelligence/feed/",
        source_type="rss",
        base_trust=8,
        category="media"
    ),
    NewsSource(
        name="VentureBeat AI",
        url="https://venturebeat.com/category/ai/feed/",
        source_type="rss",
        base_trust=8,
        category="media"
    ),
    NewsSource(
        name="The Verge AI",
        url="https://www.theverge.com/rss/ai-artificial-intelligence/index.xml",
        source_type="rss",
        base_trust=8,
        category="media"
    ),
    NewsSource(
        name="Ars Technica AI",
        url="https://feeds.arstechnica.com/arstechnica/technology-lab",
        source_type="rss",
        base_trust=8,
        category="media"
    ),
    NewsSource(
        name="Reuters Tech",
        url="https://www.reutersagency.com/feed/?taxonomy=best-topics&post_type=best&best-topics=tech",
        source_type="rss",
        base_trust=9,
        category="media"
    ),
    
    # === 개인 뉴스레터/블로그 (검증된 전문가 8-9) ===
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
    NewsSource(
        name="The Batch (DeepLearning.AI)",
        url="https://www.deeplearning.ai/the-batch/feed/",
        source_type="rss",
        base_trust=9,
        category="personal"
    ),
    NewsSource(
        name="Sebastian Raschka",
        url="https://magazine.sebastianraschka.com/feed",
        source_type="rss",
        base_trust=8,
        category="personal"
    ),
    NewsSource(
        name="Chip Huyen",
        url="https://huyenchip.com/feed.xml",
        source_type="rss",
        base_trust=8,
        category="personal"
    ),
    
    # === 커뮤니티 (7-8) ===
    NewsSource(
        name="Hacker News AI",
        url="https://hnrss.org/newest?q=AI+OR+LLM+OR+GPT+OR+Claude+OR+Gemini&points=100",
        source_type="rss",
        base_trust=7,
        category="community"
    ),
    NewsSource(
        name="Reddit MachineLearning",
        url="https://www.reddit.com/r/MachineLearning/hot/.rss?limit=20",
        source_type="rss",
        base_trust=7,
        category="community"
    ),
    NewsSource(
        name="Reddit LocalLLaMA",
        url="https://www.reddit.com/r/LocalLLaMA/hot/.rss?limit=15",
        source_type="rss",
        base_trust=7,
        category="community"
    ),
    
    # === 학술 (9) ===
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
    
    # === YouTube (영상 8) ===
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
    NewsSource(
        name="AI Explained",
        url="https://www.youtube.com/feeds/videos.xml?channel_id=UCNJ1Ymd5yFuUPtn21xtRbbw",
        source_type="rss",
        base_trust=8,
        category="personal"
    ),
]

# === Importance Keywords ===
HIGH_IMPORTANCE_KEYWORDS = [
    "gpt-5", "gpt5", "claude 4", "claude-4", "gemini 3", "llama 4",
    "release", "launch", "announce", "발표", "출시",
    "openai", "anthropic", "google deepmind", "meta ai",
    "breakthrough", "sota", "state-of-the-art", "benchmark",
    "agi", "safety", "alignment", "regulation", "법안",
    "sam altman", "dario amodei", "demis hassabis", "yann lecun",
    "andrej karpathy", "ilya sutskever",
]

EXCLUDE_KEYWORDS = [
    "sponsor", "advertisement", "promoted", "job posting",
]

# === Settings ===
MAX_NEWS_PER_BATCH = 10
SUMMARY_MAX_LENGTH = 300
CACHE_HOURS = 48
MAX_NEWS_AGE_HOURS = 24
