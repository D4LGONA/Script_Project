# AIzaSyBenORD7xC7otKoc1M6EmDOZMgAz0u9epY
import requests
from math import *
import tkinter as tk
from collections import Counter
import xml.etree.ElementTree as ET
from datetime import datetime

bookmark_lists = []
places_lists = ET.ElementTree()
perform_lists = ET.ElementTree()

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



def read_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = file.readlines()
    data = [line.strip() for line in data if line.strip()]
    return data

def count_locations(data):
    return Counter(data)

def create_canvas_graph(root, location_counts):
    canvas_width = 1000
    canvas_height = 800
    canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
    canvas.pack()

    max_count = max(location_counts.values())
    x_offset = 50
    y_offset = 700
    bar_width = 30
    spacing = 20  # Reduced spacing between bars

    for i, (location, count) in enumerate(location_counts.items()):
        bar_height = (count / max_count) * 500  # Scale bar height to fit canvas
        x_position = x_offset + i * (bar_width + spacing)
        canvas.create_rectangle(x_position, y_offset - bar_height, x_position + bar_width, y_offset, fill="skyblue")
        canvas.create_text(x_position + bar_width / 2, y_offset + 10, text=location, anchor=tk.N, angle=45, font=("Arial", 8))
        canvas.create_text(x_position + bar_width / 2, y_offset - bar_height - 10, text=str(count), anchor=tk.S, font=("Arial", 8))

def main(file_path, parent=None):
    data = read_data(file_path)
    location_counts = count_locations(data)

    if parent is None:
        root = tk.Tk()
    else:
        root = tk.Toplevel(parent)

    root.title("그래프")

    # Set the window size to match the canvas size
    window_width = 1000
    window_height = 800
    root.geometry(f"{window_width}x{window_height}")

    create_canvas_graph(root, location_counts)

    if parent is None:
        root.mainloop()

def is_valid_date(date_string):
    try:
        # 날짜 형식을 지정하여 datetime 객체로 변환 시도
        datetime.strptime(date_string, '%Y%m%d')
        return True
    except ValueError:
        return False


