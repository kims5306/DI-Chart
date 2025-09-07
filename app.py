from flask import Flask, render_template, jsonify
import requests
import json
import os
from datetime import datetime, timedelta
import schedule
import time
import threading

app = Flask(__name__)

# 전역 변수로 주가 데이터 저장
stock_data = None
last_update = None

def fetch_stock_data():
    """네이버에서 DI 주식 데이터를 가져오는 함수"""
    global stock_data, last_update
    
    try:
        url = "https://m.stock.naver.com/api/stock/001530/daily"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            stock_data = data
            last_update = datetime.now()
            print(f"주가 데이터 업데이트 완료: {last_update}")
            return True
        else:
            print(f"API 요청 실패. 상태 코드: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"데이터 가져오기 오류: {e}")
        return False

def scheduled_update():
    """스케줄된 업데이트 함수"""
    print("스케줄된 업데이트 실행 중...")
    fetch_stock_data()

# 스케줄 설정 (매일 오전 9시, 오후 3시에 업데이트)
schedule.every().day.at("09:00").do(scheduled_update)
schedule.every().day.at("15:00").do(scheduled_update)

def run_scheduler():
    """스케줄러 실행 함수"""
    while True:
        schedule.run_pending()
        time.sleep(60)  # 1분마다 체크

@app.route('/')
def index():
    """메인 페이지"""
    return render_template('index.html')

@app.route('/api/stock-data')
def get_stock_data():
    """주가 데이터 API 엔드포인트"""
    global stock_data, last_update
    
    if stock_data is None:
        # 데이터가 없으면 즉시 가져오기
        fetch_stock_data()
    
    return jsonify({
        'data': stock_data,
        'last_update': last_update.isoformat() if last_update else None
    })

@app.route('/api/update')
def manual_update():
    """수동 업데이트 API 엔드포인트"""
    success = fetch_stock_data()
    return jsonify({
        'success': success,
        'last_update': last_update.isoformat() if last_update else None
    })

if __name__ == '__main__':
    # 초기 데이터 로드
    print("초기 주가 데이터 로드 중...")
    fetch_stock_data()
    
    # 스케줄러를 별도 스레드에서 실행
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()
    
    # Flask 앱 실행
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=False)
