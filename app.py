from flask import Flask, render_template, jsonify, send_from_directory
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
    # 현재 프로젝트 루트에 있는 index.html을 그대로 서빙
    return send_from_directory(os.path.dirname(__file__), 'index.html')

@app.route('/CI.png')
def serve_ci_image():
    """루트 경로에 있는 CI.png 이미지 서빙 (404 방지)"""
    return send_from_directory(os.path.dirname(__file__), 'CI.png')

@app.route('/favicon.ico')
def serve_favicon():
    """브라우저 기본 파비콘 요청에 대해 204로 응답하여 404 콘솔 경고 방지"""
    return ('', 204)

@app.route('/health')
def health():
    """Render Health Check Endpoint"""
    return jsonify({ 'status': 'ok' })

@app.route('/api/stock-data')
def get_stock_data():
    """주가 데이터 API 엔드포인트"""
    global stock_data, last_update
    
    if stock_data is None:
        # 데이터가 없으면 즉시 가져오기 시도
        success = fetch_stock_data()
        if not success:
            # 프론트엔드가 기대하는 스키마를 유지하여 오류 메시지 방지
            return jsonify({
                'data': { 'priceInfos': [] },
                'last_update': None
            })

    # 응답 스키마 강제 정규화
    normalized = None
    try:
        if isinstance(stock_data, dict) and 'priceInfos' in stock_data:
            normalized = { 'priceInfos': stock_data['priceInfos'] }
        elif isinstance(stock_data, dict) and 'data' in stock_data and isinstance(stock_data['data'], dict) and 'priceInfos' in stock_data['data']:
            normalized = { 'priceInfos': stock_data['data']['priceInfos'] }
        else:
            # 알 수 없는 구조일 때 비어있는 리스트로 방어
            normalized = { 'priceInfos': [] }
    except Exception:
        normalized = { 'priceInfos': [] }

    return jsonify({
        'data': normalized,
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
