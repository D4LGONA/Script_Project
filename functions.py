# AIzaSyBenORD7xC7otKoc1M6EmDOZMgAz0u9epY
import requests
from math import *

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


def calculate_distance(lat1, lon1, lat2, lon2):
    # 지구의 반지름 (단위: km)
    R = 6371.0

    # 위도와 경도를 라디안으로 변환
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    # 위도와 경도의 차이 계산
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    # Haversine 공식을 사용하여 두 지점 간의 거리 계산
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance

def get_location_info(latitude, longitude):
    api_key = 'AIzaSyBenORD7xC7otKoc1M6EmDOZMgAz0u9epY'
    url = f'https://maps.googleapis.com/maps/api/geocode/json?latlng={latitude},{longitude}&key={api_key}'

    response = requests.get(url)
    response.encoding = 'utf-8'

    if response.status_code == 200:
        result = response.json()
        if result['results']:
            for component in result['results'][0]['address_components']:
                if 'administrative_area_level_1' in component['types']:
                    return component['long_name']
                if 'administrative_area_level_2' in component['types']:
                    return component['long_name']

    print(f"Response status code: {response.status_code}")
    print(f"Response content: {response.text}")

    return None