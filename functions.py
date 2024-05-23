# AIzaSyBenORD7xC7otKoc1M6EmDOZMgAz0u9epY
import requests

bookmark_lists = []

def get_location(): # 현재 위치 가져오는 함수
    api_key = 'AIzaSyBenORD7xC7otKoc1M6EmDOZMgAz0u9epY'
    url = f'https://www.googleapis.com/geolocation/v1/geolocate?key={api_key}'
    data = {
        "considerIp": "true"
    }
    response = requests.post(url, json=data)
    if response.status_code == 200:
        location_data = response.json()
        latitude = location_data['location']['lat']
        longitude = location_data['location']['lng']
        return latitude, longitude
    else:
        print("Unable to fetch location information")
        return None


def get_address(latitude, longitude):
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