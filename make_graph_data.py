import load_data
import functions
import time

with open('test/locations.txt', 'w') as file:
    res = load_data.load_all_data_clubs()
    # res의 모든 요소에 대해 반복
    for e in res.iter('placeList'):
        # 각 요소의 위도와 경도 정보 추출
        latitude = float(e.find('gpsY').text)
        longitude = float(e.find('gpsX').text)

        # get_location_info 함수 호출
        location = functions.get_location_info(latitude, longitude)

        # get_location_info 함수가 None을 반환하면 1초를 기다렸다 다시 실행합니다.
        while location is None:
            print("Location 정보를 가져오는 데 실패했습니다. 1초 기다립니다...")
            time.sleep(1)  # 1초 대기
            location = functions.get_location_info(latitude, longitude)

        # 결과 출력 또는 다른 작업 수행
        file.write(f"{location}\n")

