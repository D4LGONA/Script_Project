# AIzaSyBenORD7xC7otKoc1M6EmDOZMgAz0u9epY
import requests

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
