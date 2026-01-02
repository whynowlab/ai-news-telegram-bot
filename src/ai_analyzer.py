"""
AI Analyzer - Gemini API를 사용한 뉴스 분석 및 요약
"""
import requests
import json
import re
import time
from typing import List, Optional, Tuple
from dataclasses import dataclass

from config import GEMINI_API_KEY, Priority, HIGH_IMPORTANCE_KEYWORDS
from news_collector import NewsItem


@dataclass
class AnalyzedNews:
    """분석된 뉴스"""
    news_item: NewsItem
    korean_title: str
    korean_summary: str
    importance_score: int
    priority: Priority
    reason: str


class AIAnalyzer:
    def __init__(self):
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY가 설정되지 않았습니다")
        
        self.api_key = GEMINI_API_KEY
        self.api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={self.api_key}"
    
    def _check_keyword_importance(self, text: str) -> int:
        """키워드 기반 중요도 보너스"""
        text_lower = text.lower()
        bonus = 0
        
        for keyword in HIGH_IMPORTANCE_KEYWORDS:
            if keyword.lower() in text_lower:
                bonus += 1
        
        return min(bonus, 3)
    
    def _call_gemini(self, prompt: str) -> Optional[str]:
        """Gemini API 호출"""
        payload = {
            "contents": [
                {"parts": [{"text": prompt}]}
            ],
            "generationConfig": {
                "temperature": 0.2,
                "maxOutputTokens": 1000
            }
        }
        
        try:
            response = requests.post(
                self.api_url,
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                return data["candidates"][0]["content"]["parts"][0]["text"].strip()
            else:
                print(f"    ⚠️ Gemini API: {response.status_code}")
                return None
                
        except requests.exceptions.Timeout:
            print(f"    ⚠️ Gemini API: 타임아웃")
            return None
        except Exception as e:
            print(f"    ⚠️ Gemini API: {e}")
            return None
    
    def _extract_json(self, text: str) -> Optional[dict]:
        """텍스트에서 JSON 추출 (여러 방법 시도)"""
        # 1. 마크다운 코드블록 제거
        text = re.sub(r'```json\s*', '', text)
        text = re.sub(r'```\s*', '', text)
        text = text.strip()
        
        # 2. 전체 텍스트 파싱 시도
        try:
            return json.loads(text)
        except:
            pass
        
        # 3. JSON 객체 패턴 찾기 (중첩 브라켓 처리)
        try:
            start = text.find('{')
            if start != -1:
                depth = 0
                for i, char in enumerate(text[start:], start):
                    if char == '{':
                        depth += 1
                    elif char == '}':
                        depth -= 1
                        if depth == 0:
                            json_str = text[start:i+1]
                            return json.loads(json_str)
        except:
            pass
        
        # 4. 필드별 추출 시도 (이스케이프된 따옴표 처리)
        try:
            result = {}
            
            match = re.search(r'"korean_title"\s*:\s*"((?:[^"\\]|\\.)*)"', text)
            if match:
                result['korean_title'] = match.group(1).replace('\\"', '"')
            
            match = re.search(r'"korean_summary"\s*:\s*"((?:[^"\\]|\\.)*)"', text)
            if match:
                result['korean_summary'] = match.group(1).replace('\\"', '"')
            
            match = re.search(r'"importance_score"\s*:\s*(\d+)', text)
            if match:
                result['importance_score'] = int(match.group(1))
            
            match = re.search(r'"reason"\s*:\s*"((?:[^"\\]|\\.)*)"', text)
            if match:
                result['reason'] = match.group(1).replace('\\"', '"')
            
            if result:
                return result
        except:
            pass
        
        return None
    
    def _translate_to_korean(self, title: str, summary: str) -> Tuple[str, str]:
        """제목과 요약을 한국어로 번역"""
        prompt = f"""다음 영어 텍스트를 한국어로 번역해주세요. 반드시 아래 형식으로만 응답하세요.

제목: {title[:100]}
요약: {summary[:300]}

응답 형식:
제목: [한국어 제목 30자 이내]
요약: [한국어 요약 2문장]"""

        try:
            result = self._call_gemini(prompt)
            if result:
                kr_title = title[:50]
                kr_summary = summary[:200]
                
                for line in result.strip().split('\n'):
                    line = line.strip()
                    if line.startswith('제목:'):
                        kr_title = line.replace('제목:', '').strip()[:50]
                    elif line.startswith('요약:'):
                        kr_summary = line.replace('요약:', '').strip()[:200]
                
                return kr_title, kr_summary
        except Exception as e:
            print(f"    ⚠️ 번역 실패: {e}")
        
        return title[:50], summary[:200]
    
    def analyze_single(self, news: NewsItem) -> Optional[AnalyzedNews]:
        """단일 뉴스 분석"""
        
        prompt = f"""다음 AI/기술 뉴스를 분석해주세요.

**원문 제목**: {news.title}
**원문 요약**: {news.summary}
**소스**: {news.source_name} (신뢰도: {news.source_trust}/10)
**카테고리**: {news.category}

다음 형식의 JSON으로만 응답해주세요 (다른 텍스트 없이):
{{"korean_title": "한국어로 번역한 핵심 제목 (30자 이내)", "korean_summary": "한국어로 요약 (2-3문장, 핵심 내용만)", "importance_score": 5, "reason": "중요도 판단 이유 (1문장)"}}

**중요도 기준**:
- 9-10: 주요 AI 기업의 새 모델 출시, 획기적인 연구 발표, 중요 정책/규제
- 7-8: 주목할 만한 기술 발전, 주요 인물의 중요 발언
- 5-6: 일반적인 업계 뉴스, 흥미로운 연구
- 3-4: 사소한 업데이트, 일상적인 뉴스
- 1-2: 광고성, 반복적인 내용

반드시 JSON 형식으로만 응답하세요. 줄바꿈 없이 한 줄로 응답하세요."""

        try:
            text = self._call_gemini(prompt)
            
            if not text:
                return self._create_fallback(news)
            
            result = self._extract_json(text)
            
            if not result:
                print(f"    ⚠️ JSON 추출 실패, 번역 시도")
                return self._create_fallback(news)
            
            # 키워드 보너스 적용
            keyword_bonus = self._check_keyword_importance(
                f"{news.title} {news.summary}"
            )
            
            base_score = result.get('importance_score', 5)
            if not isinstance(base_score, int):
                try:
                    base_score = int(base_score)
                except:
                    base_score = 5
            
            trust_bonus = (news.source_trust - 5) * 0.2
            final_score = min(10, max(1, int(base_score + keyword_bonus + trust_bonus)))
            
            # 우선순위 결정
            if final_score >= 8:
                priority = Priority.REALTIME
            elif final_score >= 5:
                priority = Priority.BATCH_6H
            else:
                priority = Priority.DAILY
            
            korean_title = result.get('korean_title', news.title)[:50]
            korean_summary = result.get('korean_summary', news.summary)[:200]
            
            # summary가 너무 짧으면 번역 재시도
            if len(korean_summary) < 30:
                print(f"    ⚠️ 요약 너무 짧음, 번역 재시도")
                _, korean_summary = self._translate_to_korean(news.title, news.summary)
            
            return AnalyzedNews(
                news_item=news,
                korean_title=korean_title,
                korean_summary=korean_summary,
                importance_score=final_score,
                priority=priority,
                reason=result.get('reason', '')[:100]
            )
            
        except Exception as e:
            print(f"    ❌ 분석 실패: {e}")
            return self._create_fallback(news)
    
    def _create_fallback(self, news: NewsItem) -> AnalyzedNews:
        """분석 실패 시 번역 후 기본값 생성"""
        keyword_bonus = self._check_keyword_importance(f"{news.title} {news.summary}")
        base_score = 5 + keyword_bonus
        trust_bonus = (news.source_trust - 5) * 0.2
        final_score = min(10, max(1, int(base_score + trust_bonus)))
        
        if final_score >= 8:
            priority = Priority.REALTIME
        elif final_score >= 5:
            priority = Priority.BATCH_6H
        else:
            priority = Priority.DAILY
        
        # 번역 시도
        kr_title, kr_summary = self._translate_to_korean(news.title, news.summary)
        
        return AnalyzedNews(
            news_item=news,
            korean_title=kr_title,
            korean_summary=kr_summary,
            importance_score=final_score,
            priority=priority,
            reason="자동 분류"
        )
    
    def analyze_batch(self, news_list: List[NewsItem]) -> List[AnalyzedNews]:
        """여러 뉴스 일괄 분석"""
        analyzed = []
        
        print(f"\n🤖 {len(news_list)}개 뉴스 AI 분석 중... (Gemini)\n")
        
        for i, news in enumerate(news_list):
            print(f"  [{i+1}/{len(news_list)}] {news.title[:40]}...")
            result = self.analyze_single(news)
            if result:
                analyzed.append(result)
                print(f"    → 중요도: {result.importance_score}/10 ({result.priority.value})")
            time.sleep(0.3)
        
        # 중요도순 정렬
        analyzed.sort(key=lambda x: x.importance_score, reverse=True)
        
        print(f"\n✅ {len(analyzed)}개 뉴스 분석 완료\n")
        
        return analyzed
    
    def filter_by_priority(
        self, 
        analyzed_list: List[AnalyzedNews], 
        priority: Priority
    ) -> List[AnalyzedNews]:
        """우선순위별 필터링"""
        return [a for a in analyzed_list if a.priority == priority]


if __name__ == "__main__":
    from news_collector import NewsCollector
    
    collector = NewsCollector(cache_dir="data")
    items = collector.collect_all()
    
    if items:
        analyzer = AIAnalyzer()
        analyzed = analyzer.analyze_batch(items[:3])
        
        for a in analyzed:
            print(f"\n{'='*50}")
            print(f"📰 {a.korean_title}")
            print(f"📝 {a.korean_summary}")
            print(f"⭐ 중요도: {a.importance_score}/10")
            print(f"🚀 우선순위: {a.priority.value}")
            print(f"💡 이유: {a.reason}")
