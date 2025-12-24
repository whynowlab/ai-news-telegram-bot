"""
AI News Telegram Bot - Main Entry Point

실행 모드:
    --mode realtime : 실시간 체크 (30분마다) - 중요도 8+ 즉시 전송
    --mode batch    : 6시간 배치 - 중요도 5-7 모아서 전송
    --mode daily    : 일일 요약 - 전체 요약 전송
    --mode test     : 연결 테스트
"""
import argparse
import sys
import os
from pathlib import Path

# 모듈 경로 설정
sys.path.insert(0, str(Path(__file__).parent))

from config import Priority, MAX_NEWS_PER_BATCH
from news_collector import NewsCollector
from ai_analyzer import AIAnalyzer
from telegram_bot import TelegramBot


def run_realtime():
    """실시간 모드 - 중요 뉴스 즉시 전송"""
    print("\n" + "="*50)
    print("🚨 실시간 모드 실행")
    print("="*50)
    
    collector = NewsCollector(cache_dir="data")
    analyzer = AIAnalyzer()
    bot = TelegramBot()
    
    # 뉴스 수집
    news_items = collector.collect_all()
    
    if not news_items:
        print("📭 새로운 뉴스가 없습니다")
        return
    
    # AI 분석
    analyzed = analyzer.analyze_batch(news_items)
    
    # 실시간 알림 (중요도 8 이상)
    realtime_news = analyzer.filter_by_priority(analyzed, Priority.REALTIME)
    
    if realtime_news:
        print(f"\n🚨 {len(realtime_news)}개 중요 뉴스 발견!")
        sent_ids = bot.send_realtime_alerts(realtime_news)
        
        # 전송된 뉴스 표시
        collector.mark_multiple_as_seen(sent_ids)
        print(f"✅ {len(sent_ids)}개 실시간 알림 전송 완료")
    else:
        print("📭 실시간 전송할 중요 뉴스 없음")
    
    # 나머지 뉴스도 seen 처리 (다음 배치에서 처리)
    all_ids = [a.news_item.id for a in analyzed if a.news_item.id not in [n.news_item.id for n in realtime_news]]
    collector.mark_multiple_as_seen(all_ids)


def run_batch():
    """배치 모드 - 6시간마다 요약 전송"""
    print("\n" + "="*50)
    print("📢 6시간 배치 모드 실행")
    print("="*50)
    
    collector = NewsCollector(cache_dir="data")
    analyzer = AIAnalyzer()
    bot = TelegramBot()
    
    # 뉴스 수집
    news_items = collector.collect_all()
    
    if not news_items:
        print("📭 새로운 뉴스가 없습니다")
        return
    
    # AI 분석
    analyzed = analyzer.analyze_batch(news_items)
    
    # 배치 전송 (중요도 5 이상)
    batch_news = [a for a in analyzed if a.importance_score >= 5]
    batch_news = batch_news[:MAX_NEWS_PER_BATCH]  # 최대 개수 제한
    
    if batch_news:
        print(f"\n📢 {len(batch_news)}개 뉴스 배치 전송")
        bot.send_batch_news(batch_news, "AI 뉴스 6시간 요약")
        
        # 전송된 뉴스 표시
        sent_ids = [n.news_item.id for n in batch_news]
        collector.mark_multiple_as_seen(sent_ids)
    else:
        print("📭 배치 전송할 뉴스 없음")
    
    # 나머지 뉴스도 seen 처리
    all_ids = [a.news_item.id for a in analyzed]
    collector.mark_multiple_as_seen(all_ids)


def run_daily():
    """일일 모드 - 하루 요약 전송"""
    print("\n" + "="*50)
    print("📰 일일 요약 모드 실행")
    print("="*50)
    
    collector = NewsCollector(cache_dir="data")
    analyzer = AIAnalyzer()
    bot = TelegramBot()
    
    # 뉴스 수집
    news_items = collector.collect_all()
    
    if not news_items:
        print("📭 새로운 뉴스가 없습니다")
        bot.send_message("📭 오늘의 AI 뉴스: 특별한 소식이 없습니다.")
        return
    
    # AI 분석
    analyzed = analyzer.analyze_batch(news_items)
    
    # 전체 요약 전송 (최대 15개)
    top_news = analyzed[:15]
    
    if top_news:
        print(f"\n📰 {len(top_news)}개 뉴스 일일 요약 전송")
        bot.send_batch_news(top_news, "오늘의 AI 뉴스 요약")
        
        # 전송된 뉴스 표시
        all_ids = [a.news_item.id for a in analyzed]
        collector.mark_multiple_as_seen(all_ids)


def run_test():
    """테스트 모드 - 연결 확인"""
    print("\n" + "="*50)
    print("🧪 테스트 모드 실행")
    print("="*50)
    
    # 1. 텔레그램 연결 테스트
    print("\n1️⃣ 텔레그램 봇 연결 테스트...")
    try:
        bot = TelegramBot()
        if bot.test_connection():
            bot.send_message("🤖 AI 뉴스 봇이 정상 작동합니다!")
        else:
            print("❌ 텔레그램 연결 실패")
            return
    except Exception as e:
        print(f"❌ 텔레그램 오류: {e}")
        return
    
    # 2. 뉴스 수집 테스트
    print("\n2️⃣ 뉴스 수집 테스트...")
    try:
        collector = NewsCollector(cache_dir="data")
        items = collector.collect_all()
        print(f"✅ {len(items)}개 뉴스 수집 성공")
    except Exception as e:
        print(f"❌ 뉴스 수집 오류: {e}")
        return
    
    # 3. AI 분석 테스트 (1개만)
    print("\n3️⃣ AI 분석 테스트...")
    if items:
        try:
            analyzer = AIAnalyzer()
            result = analyzer.analyze_single(items[0])
            if result:
                print(f"✅ AI 분석 성공")
                print(f"   제목: {result.korean_title}")
                print(f"   중요도: {result.importance_score}/10")
                
                # 테스트 뉴스 전송
                bot.send_single_news(result)
            else:
                print("❌ AI 분석 실패")
        except Exception as e:
            print(f"❌ AI 분석 오류: {e}")
            return
    
    print("\n" + "="*50)
    print("✅ 모든 테스트 통과!")
    print("="*50)


def main():
    parser = argparse.ArgumentParser(description="AI News Telegram Bot")
    parser.add_argument(
        "--mode",
        choices=["realtime", "batch", "daily", "test"],
        default="test",
        help="실행 모드 선택"
    )
    
    args = parser.parse_args()
    
    # data 디렉토리 확인
    Path("data").mkdir(exist_ok=True)
    
    if args.mode == "realtime":
        run_realtime()
    elif args.mode == "batch":
        run_batch()
    elif args.mode == "daily":
        run_daily()
    elif args.mode == "test":
        run_test()


if __name__ == "__main__":
    main()
