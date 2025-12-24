"""
Telegram Bot - 텔레그램으로 뉴스 전송
"""
import requests
from typing import List, Optional
from datetime import datetime

from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, Priority
from ai_analyzer import AnalyzedNews


class TelegramBot:
    def __init__(self):
        if not TELEGRAM_BOT_TOKEN:
            raise ValueError("TELEGRAM_BOT_TOKEN이 설정되지 않았습니다")
        if not TELEGRAM_CHAT_ID:
            raise ValueError("TELEGRAM_CHAT_ID가 설정되지 않았습니다")
        
        self.token = TELEGRAM_BOT_TOKEN
        self.chat_id = TELEGRAM_CHAT_ID
        self.base_url = f"https://api.telegram.org/bot{self.token}"
    
    def _get_priority_emoji(self, priority: Priority) -> str:
        """우선순위별 이모지"""
        return {
            Priority.REALTIME: "🚨",
            Priority.BATCH_6H: "📢",
            Priority.DAILY: "📰"
        }.get(priority, "📰")
    
    def _get_importance_bar(self, score: int) -> str:
        """중요도 시각화"""
        filled = "●" * score
        empty = "○" * (10 - score)
        return f"{filled}{empty}"
    
    def _format_single_news(self, news: AnalyzedNews) -> str:
        """단일 뉴스 포맷팅"""
        emoji = self._get_priority_emoji(news.priority)
        bar = self._get_importance_bar(news.importance_score)
        
        message = f"""{emoji} <b>{news.korean_title}</b>

{news.korean_summary}

⭐ 중요도: {news.importance_score}/10 [{bar}]
📌 출처: {news.news_item.source_name}
🔗 <a href="{news.news_item.link}">원문 보기</a>"""
        
        return message
    
    def _format_batch_news(self, news_list: List[AnalyzedNews], title: str) -> str:
        """배치 뉴스 포맷팅"""
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        header = f"""📋 <b>{title}</b>
🕐 {now} KST
━━━━━━━━━━━━━━━"""
        
        items = []
        for i, news in enumerate(news_list, 1):
            emoji = self._get_priority_emoji(news.priority)
            item = f"""
{i}. {emoji} <b>{news.korean_title}</b>
   {news.korean_summary[:100]}...
   ⭐ {news.importance_score}/10 | 📌 {news.news_item.source_name}
   🔗 <a href="{news.news_item.link}">원문</a>"""
            items.append(item)
        
        return header + "\n".join(items)
    
    def send_message(self, text: str, disable_preview: bool = True) -> bool:
        """메시지 전송"""
        url = f"{self.base_url}/sendMessage"
        
        payload = {
            "chat_id": self.chat_id,
            "text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": disable_preview
        }
        
        try:
            response = requests.post(url, json=payload, timeout=30)
            result = response.json()
            
            if result.get("ok"):
                print("✅ 메시지 전송 성공")
                return True
            else:
                print(f"❌ 전송 실패: {result.get('description')}")
                return False
                
        except Exception as e:
            print(f"❌ 전송 오류: {e}")
            return False
    
    def send_single_news(self, news: AnalyzedNews) -> bool:
        """단일 뉴스 전송 (실시간용)"""
        message = self._format_single_news(news)
        return self.send_message(message)
    
    def send_batch_news(
        self, 
        news_list: List[AnalyzedNews], 
        batch_type: str = "6시간 요약"
    ) -> bool:
        """배치 뉴스 전송"""
        if not news_list:
            print("📭 전송할 뉴스가 없습니다")
            return True
        
        # 10개씩 나눠서 전송 (텔레그램 메시지 길이 제한)
        chunks = [news_list[i:i+5] for i in range(0, len(news_list), 5)]
        
        success = True
        for i, chunk in enumerate(chunks):
            title = f"{batch_type} ({i+1}/{len(chunks)})" if len(chunks) > 1 else batch_type
            message = self._format_batch_news(chunk, title)
            
            if not self.send_message(message):
                success = False
        
        return success
    
    def send_realtime_alerts(self, news_list: List[AnalyzedNews]) -> List[str]:
        """실시간 알림 전송 (중요도 8 이상)"""
        realtime_news = [n for n in news_list if n.priority == Priority.REALTIME]
        
        sent_ids = []
        for news in realtime_news:
            if self.send_single_news(news):
                sent_ids.append(news.news_item.id)
        
        return sent_ids
    
    def send_status(self, message: str) -> bool:
        """상태 메시지 전송"""
        return self.send_message(f"ℹ️ {message}")
    
    def test_connection(self) -> bool:
        """연결 테스트"""
        url = f"{self.base_url}/getMe"
        
        try:
            response = requests.get(url, timeout=10)
            result = response.json()
            
            if result.get("ok"):
                bot_name = result["result"]["username"]
                print(f"✅ 봇 연결 성공: @{bot_name}")
                return True
            else:
                print(f"❌ 봇 연결 실패: {result.get('description')}")
                return False
                
        except Exception as e:
            print(f"❌ 연결 오류: {e}")
            return False


if __name__ == "__main__":
    # 테스트
    bot = TelegramBot()
    
    if bot.test_connection():
        bot.send_message("🤖 AI 뉴스 봇 테스트 메시지입니다!")
