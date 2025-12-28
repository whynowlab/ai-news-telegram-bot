"""
News Collector - RSS 피드에서 뉴스 수집
"""
import feedparser
import hashlib
import json
import re
from datetime import datetime, timedelta, timezone
from dataclasses import dataclass, asdict
from typing import List, Optional
from pathlib import Path
from email.utils import parsedate_to_datetime

from config import NEWS_SOURCES, NewsSource, CACHE_HOURS, MAX_NEWS_AGE_HOURS


@dataclass
class NewsItem:
    """수집된 뉴스 아이템"""
    id: str
    title: str
    link: str
    summary: str
    source_name: str
    source_trust: int
    category: str
    published: Optional[str]
    published_dt: Optional[datetime]
    collected_at: str
    
    def to_dict(self):
        d = asdict(self)
        if d.get('published_dt'):
            d['published_dt'] = d['published_dt'].isoformat()
        return d


class NewsCollector:
    def __init__(self, cache_dir: str = "data"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.seen_file = self.cache_dir / "seen_news.json"
        self.seen_ids = self._load_seen_ids()
    
    def _load_seen_ids(self) -> dict:
        if self.seen_file.exists():
            try:
                with open(self.seen_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_seen_ids(self):
        cutoff = datetime.now(timezone.utc) - timedelta(hours=CACHE_HOURS)
        cutoff_str = cutoff.isoformat()
        
        cleaned = {
            k: v for k, v in self.seen_ids.items()
            if v.get('seen_at', '') > cutoff_str
        }
        self.seen_ids = cleaned
        
        with open(self.seen_file, 'w', encoding='utf-8') as f:
            json.dump(self.seen_ids, f, ensure_ascii=False, indent=2)
    
    def _generate_id(self, url: str) -> str:
        return hashlib.md5(url.encode()).hexdigest()[:12]
    
    def _parse_published_datetime(self, entry) -> Optional[datetime]:
        """발행일을 datetime으로 파싱"""
        for attr in ['published_parsed', 'updated_parsed', 'created_parsed']:
            if hasattr(entry, attr) and getattr(entry, attr):
                try:
                    t = getattr(entry, attr)
                    return datetime(t[0], t[1], t[2], t[3], t[4], t[5], tzinfo=timezone.utc)
                except:
                    pass
        
        for attr in ['published', 'updated', 'created']:
            if hasattr(entry, attr) and getattr(entry, attr):
                try:
                    return parsedate_to_datetime(getattr(entry, attr))
                except:
                    pass
        return None
    
    def _is_recent(self, published_dt: Optional[datetime]) -> bool:
        """최신 뉴스인지 확인 (MAX_NEWS_AGE_HOURS 이내)"""
        if not published_dt:
            return True  # 날짜 없으면 일단 포함
        
        now = datetime.now(timezone.utc)
        if published_dt.tzinfo is None:
            published_dt = published_dt.replace(tzinfo=timezone.utc)
        
        age = now - published_dt
        return age <= timedelta(hours=MAX_NEWS_AGE_HOURS)
    
    def _get_summary(self, entry) -> str:
        if hasattr(entry, 'summary') and entry.summary:
            return self._clean_html(entry.summary)[:500]
        if hasattr(entry, 'description') and entry.description:
            return self._clean_html(entry.description)[:500]
        return ""
    
    def _clean_html(self, text: str) -> str:
        clean = re.sub(r'<[^>]+>', '', text)
        clean = re.sub(r'\s+', ' ', clean).strip()
        return clean
    
    def collect_from_source(self, source: NewsSource) -> List[NewsItem]:
        items = []
        
        try:
            feedparser.USER_AGENT = "AI-News-Bot/1.0 (Personal Use)"
            feed = feedparser.parse(source.url)
            
            if feed.bozo and not feed.entries:
                print(f"⚠️ {source.name}: 피드 파싱 실패")
                return items
            
            for entry in feed.entries[:20]:
                link = entry.get('link', '')
                if not link:
                    continue
                
                news_id = self._generate_id(link)
                
                if news_id in self.seen_ids:
                    continue
                
                published_dt = self._parse_published_datetime(entry)
                
                # 최신 뉴스만 필터링
                if not self._is_recent(published_dt):
                    continue
                
                item = NewsItem(
                    id=news_id,
                    title=entry.get('title', 'No Title'),
                    link=link,
                    summary=self._get_summary(entry),
                    source_name=source.name,
                    source_trust=source.base_trust,
                    category=source.category,
                    published=published_dt.isoformat() if published_dt else None,
                    published_dt=published_dt,
                    collected_at=datetime.now(timezone.utc).isoformat()
                )
                
                items.append(item)
            
            print(f"✅ {source.name}: {len(items)}개 새 뉴스")
            
        except Exception as e:
            print(f"❌ {source.name}: 수집 실패 - {e}")
        
        return items
    
    def collect_all(self) -> List[NewsItem]:
        all_items = []
        
        print(f"\n📡 {len(NEWS_SOURCES)}개 소스에서 뉴스 수집 시작...\n")
        
        for source in NEWS_SOURCES:
            items = self.collect_from_source(source)
            all_items.extend(items)
        
        # 최신순 정렬
        all_items.sort(key=lambda x: x.published_dt or datetime.min.replace(tzinfo=timezone.utc), reverse=True)
        
        print(f"\n📊 총 {len(all_items)}개 최신 뉴스 수집 완료\n")
        
        return all_items
    
    def mark_as_seen(self, news_id: str):
        self.seen_ids[news_id] = {
            'seen_at': datetime.now(timezone.utc).isoformat()
        }
        self._save_seen_ids()
    
    def mark_multiple_as_seen(self, news_ids: List[str]):
        now = datetime.now(timezone.utc).isoformat()
        for news_id in news_ids:
            self.seen_ids[news_id] = {'seen_at': now}
        self._save_seen_ids()


if __name__ == "__main__":
    collector = NewsCollector(cache_dir="data")
    items = collector.collect_all()
    
    for item in items[:5]:
        print(f"\n{'='*50}")
        print(f"📰 {item.title}")
        print(f"🕐 {item.published}")
        print(f"⭐ 신뢰도: {item.source_trust}/10 | 소스: {item.source_name}")
