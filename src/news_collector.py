"""
News Collector - RSS 피드에서 뉴스 수집
"""
import feedparser
import hashlib
import json
import os
from datetime import datetime, timedelta, timezone
from dataclasses import dataclass, asdict
from typing import List, Optional
from pathlib import Path

from config import NEWS_SOURCES, NewsSource, CACHE_HOURS


@dataclass
class NewsItem:
    """수집된 뉴스 아이템"""
    id: str                    # 고유 ID (URL 해시)
    title: str                 # 제목
    link: str                  # 원문 링크
    summary: str               # 원문 요약/설명
    source_name: str           # 소스 이름
    source_trust: int          # 소스 신뢰도
    category: str              # 카테고리
    published: Optional[str]   # 발행일
    collected_at: str          # 수집 시간
    
    def to_dict(self):
        return asdict(self)


class NewsCollector:
    def __init__(self, cache_dir: str = "data"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.seen_file = self.cache_dir / "seen_news.json"
        self.seen_ids = self._load_seen_ids()
    
    def _load_seen_ids(self) -> dict:
        """이미 처리한 뉴스 ID 로드"""
        if self.seen_file.exists():
            try:
                with open(self.seen_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_seen_ids(self):
        """처리한 뉴스 ID 저장"""
        # 오래된 항목 정리 (48시간 이상)
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
        """URL 기반 고유 ID 생성"""
        return hashlib.md5(url.encode()).hexdigest()[:12]
    
    def _parse_published_date(self, entry) -> Optional[str]:
        """발행일 파싱"""
        for attr in ['published', 'updated', 'created']:
            if hasattr(entry, attr) and getattr(entry, attr):
                return getattr(entry, attr)
        return None
    
    def _get_summary(self, entry) -> str:
        """요약 추출"""
        # summary 또는 description 필드 확인
        if hasattr(entry, 'summary') and entry.summary:
            return self._clean_html(entry.summary)[:500]
        if hasattr(entry, 'description') and entry.description:
            return self._clean_html(entry.description)[:500]
        return ""
    
    def _clean_html(self, text: str) -> str:
        """HTML 태그 제거"""
        import re
        clean = re.sub(r'<[^>]+>', '', text)
        clean = re.sub(r'\s+', ' ', clean).strip()
        return clean
    
    def collect_from_source(self, source: NewsSource) -> List[NewsItem]:
        """단일 소스에서 뉴스 수집"""
        items = []
        
        try:
            # User-Agent 설정 (Reddit 등에서 필요)
            feedparser.USER_AGENT = "AI-News-Bot/1.0 (Personal Use)"
            
            feed = feedparser.parse(source.url)
            
            if feed.bozo and not feed.entries:
                print(f"⚠️ {source.name}: 피드 파싱 실패")
                return items
            
            for entry in feed.entries[:15]:  # 소스당 최대 15개
                link = entry.get('link', '')
                if not link:
                    continue
                
                news_id = self._generate_id(link)
                
                # 이미 처리한 뉴스 스킵
                if news_id in self.seen_ids:
                    continue
                
                item = NewsItem(
                    id=news_id,
                    title=entry.get('title', 'No Title'),
                    link=link,
                    summary=self._get_summary(entry),
                    source_name=source.name,
                    source_trust=source.base_trust,
                    category=source.category,
                    published=self._parse_published_date(entry),
                    collected_at=datetime.now(timezone.utc).isoformat()
                )
                
                items.append(item)
            
            print(f"✅ {source.name}: {len(items)}개 새 뉴스")
            
        except Exception as e:
            print(f"❌ {source.name}: 수집 실패 - {e}")
        
        return items
    
    def collect_all(self) -> List[NewsItem]:
        """모든 소스에서 뉴스 수집"""
        all_items = []
        
        print(f"\n📡 {len(NEWS_SOURCES)}개 소스에서 뉴스 수집 시작...\n")
        
        for source in NEWS_SOURCES:
            items = self.collect_from_source(source)
            all_items.extend(items)
        
        print(f"\n📊 총 {len(all_items)}개 새 뉴스 수집 완료\n")
        
        return all_items
    
    def mark_as_seen(self, news_id: str):
        """뉴스를 처리됨으로 표시"""
        self.seen_ids[news_id] = {
            'seen_at': datetime.now(timezone.utc).isoformat()
        }
        self._save_seen_ids()
    
    def mark_multiple_as_seen(self, news_ids: List[str]):
        """여러 뉴스를 처리됨으로 표시"""
        now = datetime.now(timezone.utc).isoformat()
        for news_id in news_ids:
            self.seen_ids[news_id] = {'seen_at': now}
        self._save_seen_ids()


if __name__ == "__main__":
    # 테스트
    collector = NewsCollector(cache_dir="data")
    items = collector.collect_all()
    
    for item in items[:5]:
        print(f"\n{'='*50}")
        print(f"📰 {item.title}")
        print(f"🔗 {item.link}")
        print(f"📝 {item.summary[:100]}...")
        print(f"⭐ 신뢰도: {item.source_trust}/10 | 소스: {item.source_name}")
