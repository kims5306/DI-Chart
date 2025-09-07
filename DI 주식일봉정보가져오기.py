import requests

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

print(response.text)