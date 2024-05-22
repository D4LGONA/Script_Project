import requests

def get_address_from_coordinates(latitude, longitude):
    # Google Maps API 키
    api_key = 'AIzaSyBenORD7xC7otKoc1M6EmDOZMgAz0u9epY'

    # Google Maps Geocoding API 요청 URL
    url = f'https://maps.googleapis.com/maps/api/geocode/json?latlng={latitude},{longitude}&key={api_key}'

    # API에 요청을 보냄
    response = requests.get(url)
    data = response.json()

    # 결과에서 주소 추출
    if 'results' in data and len(data['results']) > 0:
        address = data['results'][0]['formatted_address']
        return address
    else:
        return "주소를 찾을 수 없습니다."

# 예시 위도와 경도
latitude = 37.5000
longitude = 126.9780

# 주소 가져오기
address = get_address_from_coordinates(latitude, longitude)
print("주소:", address)