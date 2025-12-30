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

# === News Sources (총 53개) ===
NEWS_SOURCES = [
    # === AI 기업 공식 블로그 (10개) ===
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
    NewsSource(
        name="Amazon AI Blog",
        url="https://aws.amazon.com/blogs/machine-learning/feed/",
        source_type="rss",
        base_trust=9,
        category="official"
    ),
    NewsSource(
        name="Apple ML Research",
        url="https://machinelearning.apple.com/rss.xml",
        source_type="rss",
        base_trust=9,
        category="official"
    ),
    
    # === AI 인플루언서 X/트위터 (10개) ===
    NewsSource(
        name="Sam Altman (OpenAI CEO)",
        url="https://rsshub.app/twitter/user/sama",
        source_type="rss",
        base_trust=10,
        category="influencer"
    ),
    NewsSource(
        name="Yann LeCun (Meta AI)",
        url="https://rsshub.app/twitter/user/ylecun",
        source_type="rss",
        base_trust=10,
        category="influencer"
    ),
    NewsSource(
        name="Andrej Karpathy",
        url="https://rsshub.app/twitter/user/karpathy",
        source_type="rss",
        base_trust=10,
        category="influencer"
    ),
    NewsSource(
        name="Demis Hassabis (DeepMind)",
        url="https://rsshub.app/twitter/user/demaborowski",
        source_type="rss",
        base_trust=10,
        category="influencer"
    ),
    NewsSource(
        name="Jim Fan (NVIDIA)",
        url="https://rsshub.app/twitter/user/DrJimFan",
        source_type="rss",
        base_trust=9,
        category="influencer"
    ),
    NewsSource(
        name="Emad Mostaque",
        url="https://rsshub.app/twitter/user/EMostaque",
        source_type="rss",
        base_trust=8,
        category="influencer"
    ),
    NewsSource(
        name="Harrison Chase (LangChain)",
        url="https://rsshub.app/twitter/user/hwchase17",
        source_type="rss",
        base_trust=8,
        category="influencer"
    ),
    NewsSource(
        name="Swyx (AI Engineer)",
        url="https://rsshub.app/twitter/user/swyx",
        source_type="rss",
        base_trust=8,
        category="influencer"
    ),
    NewsSource(
        name="Elvis (AI News)",
        url="https://rsshub.app/twitter/user/oaborowski",
        source_type="rss",
        base_trust=7,
        category="influencer"
    ),
    NewsSource(
        name="AI Breakfast",
        url="https://rsshub.app/twitter/user/AiBreakfast",
        source_type="rss",
        base_trust=7,
        category="influencer"
    ),
    
    # === AI 전문 뉴스 (3개) ===
    NewsSource(
        name="Google News AI",
        url="https://news.google.com/rss/search?q=artificial+intelligence+OR+ChatGPT+OR+OpenAI+OR+Claude+AI&hl=en-US&gl=US&ceid=US:en",
        source_type="rss",
        base_trust=7,
        category="news"
    ),
    NewsSource(
        name="Google News AI 한국",
        url="https://news.google.com/rss/search?q=ChatGPT+OR+GPT+OR+OpenAI+OR+Anthropic+OR+Claude+OR+Gemini+OR+LLM&hl=ko&gl=KR&ceid=KR:ko",
        source_type="rss",
        base_trust=7,
        category="news"
    ),
    NewsSource(
        name="The Guardian AI",
        url="https://www.theguardian.com/technology/artificialintelligenceai/rss",
        source_type="rss",
        base_trust=8,
        category="news"
    ),
    
    # === AI 전문 미디어 (6개) ===
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
    
    # === AI 전문가 블로그 (7개) ===
    NewsSource(
        name="Simon Willison Blog",
        url="https://simonwillison.net/atom/everything/",
        source_type="rss",
        base_trust=9,
        category="expert"
    ),
    NewsSource(
        name="Lil'Log (Lilian Weng)",
        url="https://lilianweng.github.io/index.xml",
        source_type="rss",
        base_trust=9,
        category="expert"
    ),
    NewsSource(
        name="AI Snake Oil",
        url="https://www.aisnakeoil.com/feed",
        source_type="rss",
        base_trust=8,
        category="expert"
    ),
    NewsSource(
        name="The Batch (DeepLearning.AI)",
        url="https://www.deeplearning.ai/the-batch/feed/",
        source_type="rss",
        base_trust=9,
        category="expert"
    ),
    NewsSource(
        name="Sebastian Raschka",
        url="https://magazine.sebastianraschka.com/feed",
        source_type="rss",
        base_trust=8,
        category="expert"
    ),
    NewsSource(
        name="Chip Huyen",
        url="https://huyenchip.com/feed.xml",
        source_type="rss",
        base_trust=8,
        category="expert"
    ),
    NewsSource(
        name="Jay Alammar",
        url="https://jalammar.github.io/feed.xml",
        source_type="rss",
        base_trust=8,
        category="expert"
    ),
    
    # === AI 커뮤니티 (5개) ===
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
    NewsSource(
        name="Reddit ChatGPT",
        url="https://www.reddit.com/r/ChatGPT/hot/.rss?limit=15",
        source_type="rss",
        base_trust=6,
        category="community"
    ),
    NewsSource(
        name="Reddit OpenAI",
        url="https://www.reddit.com/r/OpenAI/hot/.rss?limit=15",
        source_type="rss",
        base_trust=6,
        category="community"
    ),
    
    # === AI 논문 (5개) ===
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
    NewsSource(
        name="arXiv cs.CV",
        url="https://rss.arxiv.org/rss/cs.CV",
        source_type="rss",
        base_trust=9,
        category="academic"
    ),
    NewsSource(
        name="Papers With Code",
        url="https://paperswithcode.com/latest.rss",
        source_type="rss",
        base_trust=9,
        category="academic"
    ),
    
    # === AI 영상 (3개) ===
    NewsSource(
        name="Two Minute Papers",
        url="https://www.youtube.com/feeds/videos.xml?channel_id=UCbfYPyITQ-7l4upoX8nvctg",
        source_type="rss",
        base_trust=8,
        category="video"
    ),
    NewsSource(
        name="Yannic Kilcher",
        url="https://www.youtube.com/feeds/videos.xml?channel_id=UCZHmQk67mSJgfCCTn7xBfew",
        source_type="rss",
        base_trust=8,
        category="video"
    ),
    NewsSource(
        name="AI Explained",
        url="https://www.youtube.com/feeds/videos.xml?channel_id=UCNJ1Ymd5yFuUPtn21xtRbbw",
        source_type="rss",
        base_trust=8,
        category="video"
    ),
    
    # === AI 뉴스레터 (4개) ===
    NewsSource(
        name="Import AI",
        url="https://importai.substack.com/feed",
        source_type="rss",
        base_trust=8,
        category="newsletter"
    ),
    NewsSource(
        name="Last Week in AI",
        url="https://lastweekin.ai/feed",
        source_type="rss",
        base_trust=8,
        category="newsletter"
    ),
    NewsSource(
        name="The Rundown AI",
        url="https://www.therundown.ai/feed",
        source_type="rss",
        base_trust=7,
        category="newsletter"
    ),
    NewsSource(
        name="Ben's Bites",
        url="https://bensbites.beehiiv.com/feed",
        source_type="rss",
        base_trust=7,
        category="newsletter"
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
