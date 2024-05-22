import requests

# Google API 키를 직접 하드코딩
GEOCODING_API_KEY = 'your_google_api_key_here'


def get_address(lat, lng):
    # Google Geocoding API의 엔드포인트
    url = 'https://maps.googleapis.com/maps/api/geocode/json'

    # 요청에 필요한 파라미터
    params = {
        'latlng': f'{lat},{lng}',
        'key': GEOCODING_API_KEY
    }

    # API 요청을 보냅니다.
    response = requests.get(url, params=params)

    if response.status_code == 200:
        # JSON 응답을 파싱합니다.
        data = response.json()

        if 'results' in data and len(data['results']) > 0:
            # 첫 번째 결과의 formatted_address를 반환합니다.
            return data['results'][0]['formatted_address']
        else:
            return '주소를 찾을 수 없습니다.'
    else:
        return f'에러가 발생했습니다: {response.status_code}'


# 테스트 좌표 (예: 서울의 위도와 경도)
latitude = 37.5665
longitude = 126.9780

# 주소를 가져옵니다.
address = get_address(latitude, longitude)
print(f'주소: {address}')
