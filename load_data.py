import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import os
import time

def load_all_data_clubs():
    # http://www.culture.go.kr/openapi/rest/cultureartspaces/performingplace?serviceKey=ipA7GxlvIHVrsFJKg6yO%2FihFWarSbbwT%2BhG6ejOQMISeS9BSPgbgsf08SbC9qwgBEjJlzzj%2FyYMNMbFhrUZ09A%3D%3D&cPage=10&rows=1&RequestTime=20100810:23003422
    url = 'http://www.culture.go.kr/openapi/rest/cultureartspaces/performingplace'
    params = {'serviceKey': 'ipA7GxlvIHVrsFJKg6yO/ihFWarSbbwT+hG6ejOQMISeS9BSPgbgsf08SbC9qwgBEjJlzzj/yYMNMbFhrUZ09A==',
              'rows': '1000'}  # 한 페이지에 표시할 데이터 수를 설정합니다.
    file_path = 'datas/clubs_data.xml'

    # 파일이 존재하는지 확인합니다.
    if os.path.exists(file_path):
        # 파일의 마지막 수정 시간을 가져옵니다.
        file_mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
        current_time = datetime.now()

        # 파일이 이틀 이상 오래된 경우 새로운 데이터를 로드합니다.
        if current_time - file_mod_time <= timedelta(days=2):
            print("기존 파일이 최신입니다. 새로 데이터를 로드하지 않습니다.")
            existing_tree = ET.parse(file_path)
            return existing_tree

    # 모든 데이터를 담을 하나의 XML 요소 생성
    all_data_element = ET.Element('all_data')

    # 페이지별로 데이터를 요청하고 받아옵니다.
    page = 1
    while True:
        params['cPage'] = str(page)
        response = requests.get(url, params=params)
        response.encoding = 'utf-8'
        root = ET.fromstring(response.text)

        # placeList 요소를 찾아 데이터를 추출하고 all_data_element에 추가합니다.
        for place_list in root.findall('.//placeList'):
            all_data_element.append(place_list)

        # 다음 페이지가 있는지 확인합니다.
        total_cnt = int(root.findtext('.//totalCount'))
        print("데이터 로딩중... " + str(len(all_data_element.findall('.//placeList'))) + "개 완료")
        if total_cnt == len(all_data_element.findall('.//placeList')):
            break
        else:
            page += 1

    # 모든 데이터를 포함하는 ElementTree 객체 생성
    all_data_tree = ET.ElementTree(all_data_element)

    # 현재 시간을 추가합니다.
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    timestamp_element = ET.Element('timestamp')
    timestamp_element.text = now
    all_data_element.insert(0, timestamp_element)

    # 모든 데이터를 포함하는 ElementTree 객체 생성
    all_data_tree = ET.ElementTree(all_data_element)

    # XML 파일로 저장
    with open(file_path, 'wb') as xml_file:
        all_data_tree.write(xml_file, encoding='utf-8', xml_declaration=True)
    print("새로운 데이터로 XML 파일을 저장했습니다.")

    return all_data_tree

def load_all_data_performs():
    url = 'http://api.data.go.kr/openapi/tn_pubr_public_cltur_fstvl_api'
    params = {'serviceKey': 'ipA7GxlvIHVrsFJKg6yO/ihFWarSbbwT+hG6ejOQMISeS9BSPgbgsf08SbC9qwgBEjJlzzj/yYMNMbFhrUZ09A==',
              'pageNo': '1', 'numOfRows': '1673', 'type': 'xml'}

    response = requests.get(url, params=params)
    response.encoding = 'utf-8'
    print(response.text)
    root = ET.fromstring(response.text)

def load_data_performs():
    # http://www.culture.go.kr/openapi/rest/publicperformancedisplays/realm?serviceKey=ipA7GxlvIHVrsFJKg6yO%2FihFWarSbbwT%2BhG6ejOQMISeS9BSPgbgsf08SbC9qwgBEjJlzzj%2FyYMNMbFhrUZ09A%3D%3D&sortStdr=2&cPage=1&rows=100
    url = 'http://www.culture.go.kr/openapi/rest/publicperformancedisplays/period'
    params = {'serviceKey': 'ipA7GxlvIHVrsFJKg6yO/ihFWarSbbwT+hG6ejOQMISeS9BSPgbgsf08SbC9qwgBEjJlzzj/yYMNMbFhrUZ09A==',
              'sortStdr' : '2', # 출력정렬방식 - 1:등록일, 2:공연명, 3:지역
              'rows': '1000',
              'from': '20100101',
              'to':'20250101'}  # 한 페이지에 표시할 데이터 수를 설정합니다.

    file_path = 'datas/performs_data.xml'

    # 파일이 존재하는지 확인합니다.
    if os.path.exists(file_path):
        # 파일의 마지막 수정 시간을 가져옵니다.
        file_mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
        current_time = datetime.now()

        # 파일이 이틀 이상 오래된 경우 새로운 데이터를 로드합니다.
        if current_time - file_mod_time <= timedelta(days=2):
            print("기존 파일이 최신입니다. 새로 데이터를 로드하지 않습니다.")
            existing_tree = ET.parse(file_path)
            return existing_tree

    # 모든 데이터를 담을 하나의 XML 요소 생성
    all_data_element = ET.Element('all_data')

    # 페이지별로 데이터를 요청하고 받아옵니다.
    page = 1
    while True:
        params['cPage'] = str(page)
        response = requests.get(url, params=params)
        response.encoding = 'utf-8'
        root = ET.fromstring(response.text)

        # placeList 요소를 찾아 데이터를 추출하고 all_data_element에 추가합니다.
        for place_list in root.findall('.//perforList'):
            all_data_element.append(place_list)

        # 다음 페이지가 있는지 확인합니다.
        total_cnt = int(root.findtext('.//totalCount'))
        print("데이터 로딩중... " + str(len(all_data_element.findall('.//perforList'))) + "개 완료")
        if total_cnt == len(all_data_element.findall('.//perforList')):
            break
        else:
            page += 1

    # 모든 데이터를 포함하는 ElementTree 객체 생성
    all_data_tree = ET.ElementTree(all_data_element)

    # 현재 시간을 추가합니다.
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    timestamp_element = ET.Element('timestamp')
    timestamp_element.text = now
    all_data_element.insert(0, timestamp_element)

    # 모든 데이터를 포함하는 ElementTree 객체 생성
    all_data_tree = ET.ElementTree(all_data_element)

    # XML 파일로 저장
    with open(file_path, 'wb') as xml_file:
        all_data_tree.write(xml_file, encoding='utf-8', xml_declaration=True)
    print("새로운 데이터로 XML 파일을 저장했습니다.")

    return all_data_tree

def load_by_period():
    url = 'http://www.culture.go.kr/openapi/rest/publicperformancedisplays/period'
    # 현재 시간을 타임스탬프로 가져오기
    current_timestamp = time.time()

    # 타임스탬프를 날짜로 변환하기
    current_date = time.strftime("%Y%m%d", time.localtime(current_timestamp))

    # params 설정
    params = {
        'serviceKey': 'ipA7GxlvIHVrsFJKg6yO/ihFWarSbbwT+hG6ejOQMISeS9BSPgbgsf08SbC9qwgBEjJlzzj/yYMNMbFhrUZ09A==',
        'sortStdr': '2',  # 출력정렬방식 - 1:등록일, 2:공연명, 3:지역
        'rows': '1000',
        'from': current_date,
        'to': current_date  # 현재 날짜로 설정
    }

    all_data_element = ET.Element('all_data')

    # 페이지별로 데이터를 요청하고 받아옵니다.
    page = 1
    while True:
        params['cPage'] = str(page)
        response = requests.get(url, params=params)
        response.encoding = 'utf-8'
        root = ET.fromstring(response.text)

        # placeList 요소를 찾아 데이터를 추출하고 all_data_element에 추가합니다.
        for place_list in root.findall('.//perforList'):
            all_data_element.append(place_list)

        # 다음 페이지가 있는지 확인합니다.
        total_cnt = int(root.findtext('.//totalCount'))
        if total_cnt == len(all_data_element.findall('.//perforList')):
            break
        else:
            page += 1

    # 모든 데이터를 포함하는 ElementTree 객체 생성
    all_data_tree = ET.ElementTree(all_data_element)

    return all_data_tree

def get_detail(seq):
    url = 'http://www.culture.go.kr/openapi/rest/publicperformancedisplays/d/'
    params = {'serviceKey': 'ipA7GxlvIHVrsFJKg6yO/ihFWarSbbwT+hG6ejOQMISeS9BSPgbgsf08SbC9qwgBEjJlzzj/yYMNMbFhrUZ09A==', 'seq': seq}

    response = requests.get(url, params=params)
    response.encoding = 'utf-8'
    root = ET.fromstring(response.text)
    # URL 값을 찾아서 반환
    url_element = root.find('.//url')
    if url_element is not None:
        return url_element.text
