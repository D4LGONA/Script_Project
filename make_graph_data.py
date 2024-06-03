import load_data
import time
from r_geo_test import *

# 공연장 데이터용
'''
with open('datas/locations_clubs.txt', 'w', encoding='utf-8') as file:
    res = load_data.load_all_data_clubs()
    # res의 모든 요소에 대해 반복
    cnt = 0
    for e in res.iter('placeList'):
        print(cnt)
        # 각 요소의 위도와 경도 정보 추출
        try:
            # 각 요소의 위도와 경도 정보 추출
            latitude = float(e.find('gpsY').text)
            longitude = float(e.find('gpsX').text)

            # get_location_info 함수 호출
            location = get_location_details(latitude, longitude)
            cnt += 1

            if location is None: continue

            # 결과 출력 또는 다른 작업 수행
            file.write(f"{location}\n")
        except:
            cnt += 1
            continue
'''

# 박물관 데이터용
with open('datas/locations_mus.txt', 'w', encoding='utf-8') as file:
    res = load_data.load_all_data_mus()
    # res의 모든 요소에 대해 반복
    cnt = 0
    for e in res.iter('placeList'):
        print(cnt)
        # 각 요소의 위도와 경도 정보 추출
        try:
            # 각 요소의 위도와 경도 정보 추출
            latitude = float(e.find('gpsY').text)
            longitude = float(e.find('gpsX').text)

            # get_location_info 함수 호출
            location = get_location_details(latitude, longitude)
            cnt += 1

            if location is None: continue

            # 결과 출력 또는 다른 작업 수행
            file.write(f"{location}\n")
        except:
            cnt += 1
            continue

# 도서관 데이터용
with open('datas/locations_libs.txt', 'w', encoding='utf-8') as file:
    res = load_data.load_all_data_libs()
    # res의 모든 요소에 대해 반복
    cnt = 0
    for e in res.iter('placeList'):
        print(cnt)
        # 각 요소의 위도와 경도 정보 추출
        try:
            # 각 요소의 위도와 경도 정보 추출
            latitude = float(e.find('gpsY').text)
            longitude = float(e.find('gpsX').text)

            # get_location_info 함수 호출
            location = get_location_details(latitude, longitude)
            cnt += 1

            if location is None: continue

            # 결과 출력 또는 다른 작업 수행
            file.write(f"{location}\n")
        except:
            cnt += 1
            continue

with open('datas/locations_halls.txt', 'w', encoding='utf-8') as file:
    res = load_data.load_all_data_halls()
    # res의 모든 요소에 대해 반복
    cnt = 0
    for e in res.iter('placeList'):
        print(cnt)
        # 각 요소의 위도와 경도 정보 추출
        try:
            # 각 요소의 위도와 경도 정보 추출
            latitude = float(e.find('gpsY').text)
            longitude = float(e.find('gpsX').text)

            # get_location_info 함수 호출
            location = get_location_details(latitude, longitude)
            cnt += 1

            if location is None: continue

            # 결과 출력 또는 다른 작업 수행
            file.write(f"{location}\n")
        except:
            cnt += 1
            continue

with open('datas/locations_arts.txt', 'w', encoding='utf-8') as file:
    res = load_data.load_all_data_arts()
    # res의 모든 요소에 대해 반복
    cnt = 0
    for e in res.iter('placeList'):
        print(cnt)
        # 각 요소의 위도와 경도 정보 추출
        try:
            # 각 요소의 위도와 경도 정보 추출
            latitude = float(e.find('gpsY').text)
            longitude = float(e.find('gpsX').text)

            # get_location_info 함수 호출
            location = get_location_details(latitude, longitude)
            cnt += 1

            if location is None: continue

            # 결과 출력 또는 다른 작업 수행
            file.write(f"{location}\n")
        except:
            cnt += 1
            continue