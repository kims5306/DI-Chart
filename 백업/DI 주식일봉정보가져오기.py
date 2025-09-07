import requests
import json
from datetime import datetime

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'origin': 'https://m.stock.naver.com',
    'priority': 'u=1, i',
    'referer': 'https://m.stock.naver.com/domestic/stock/001530/total',
    'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
}

params = {
    'periodType': 'dayCandle',
}

response = requests.get('https://api.stock.naver.com/chart/domestic/item/001530', params=params, headers=headers)

# 응답이 성공적인 경우 JSON 파일로 저장
if response.status_code == 200:
    try:
        # 응답 데이터를 JSON으로 파싱
        data = response.json()
        
        # 현재 시간을 파일명에 포함
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'stock_data_001530_{timestamp}.json'
        
        # JSON 파일로 저장 (한글 깨짐 방지를 위해 ensure_ascii=False 사용)
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f'데이터가 성공적으로 저장되었습니다: {filename}')
        print(f'저장된 데이터 미리보기:')
        print(json.dumps(data, ensure_ascii=False, indent=2)[:500] + '...')
        
    except json.JSONDecodeError:
        print('응답을 JSON으로 파싱할 수 없습니다.')
        print('원본 응답:', response.text)
else:
    print(f'API 요청 실패. 상태 코드: {response.status_code}')
    print('응답 내용:', response.text)