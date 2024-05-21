
# AIzaSyBenORD7xC7otKoc1M6EmDOZMgAz0u9epY

import requests

def get_location_with_google_geolocation(api_key):
    url = f'https://www.googleapis.com/geolocation/v1/geolocate?key={api_key}'
    data = {
        "considerIp": "true"
    }
    response = requests.post(url, json=data)
    if response.status_code == 200:
        location_data = response.json()
        latitude = location_data['location']['lat']
        longitude = location_data['location']['lng']
        return {
            'Latitude': latitude,
            'Longitude': longitude
        }
    else:
        print("Unable to fetch location information")
        return None

# 사용 예시
api_key = 'AIzaSyBenORD7xC7otKoc1M6EmDOZMgAz0u9epY'
location_info = get_location_with_google_geolocation(api_key)
if location_info:
    print("Location Information:")
    for key, value in location_info.items():
        print(f"{key}: {value}")
