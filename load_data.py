import requests
import xml.etree.ElementTree as ET


def load_all_data_clubs():
    # http://www.culture.go.kr/openapi/rest/cultureartspaces/performingplace?serviceKey=ipA7GxlvIHVrsFJKg6yO%2FihFWarSbbwT%2BhG6ejOQMISeS9BSPgbgsf08SbC9qwgBEjJlzzj%2FyYMNMbFhrUZ09A%3D%3D&cPage=10&rows=1&RequestTime=20100810:23003422
    url = 'http://www.culture.go.kr/openapi/rest/cultureartspaces/performingplace'
    params = {'serviceKey': 'ipA7GxlvIHVrsFJKg6yO/ihFWarSbbwT+hG6ejOQMISeS9BSPgbgsf08SbC9qwgBEjJlzzj/yYMNMbFhrUZ09A==',
              'rows': '1000'}  # 한 페이지에 표시할 데이터 수를 설정합니다.

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

    return all_data_tree

def load_all_data_performs():
    url = 'http://api.data.go.kr/openapi/tn_pubr_public_cltur_fstvl_api'
    params = {'serviceKey': 'ipA7GxlvIHVrsFJKg6yO/ihFWarSbbwT+hG6ejOQMISeS9BSPgbgsf08SbC9qwgBEjJlzzj/yYMNMbFhrUZ09A==',
              'pageNo': '1', 'numOfRows': '1673', 'type': 'xml'}

    response = requests.get(url, params=params)
    response.encoding = 'utf-8'
    print(response.text)
    root = ET.fromstring(response.text)

def load_data():
    # http://www.culture.go.kr/openapi/rest/publicperformancedisplays/realm?serviceKey=ipA7GxlvIHVrsFJKg6yO%2FihFWarSbbwT%2BhG6ejOQMISeS9BSPgbgsf08SbC9qwgBEjJlzzj%2FyYMNMbFhrUZ09A%3D%3D&sortStdr=2&cPage=1&rows=100
    url = 'http://www.culture.go.kr/openapi/rest/publicperformancedisplays/realm'
    params = {'serviceKey': 'ipA7GxlvIHVrsFJKg6yO/ihFWarSbbwT+hG6ejOQMISeS9BSPgbgsf08SbC9qwgBEjJlzzj/yYMNMbFhrUZ09A==',
              'sortStdr' : '2', # 출력정렬방식 - 1:등록일, 2:공연명, 3:지역
              'rows': '1000' }  # 한 페이지에 표시할 데이터 수를 설정합니다.

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
        for perfor_list in root.findall('.//perforList'):
            all_data_element.append(perfor_list)

        # 다음 페이지가 있는지 확인합니다.
        total_cnt = int(root.findtext('.//totalCount'))
        print(total_cnt)
        print("데이터 로딩중... " + str(len(all_data_element.findall('.//perforList'))) + "개 완료")
        if total_cnt == len(all_data_element.findall('.//perforList')):
            break
        else:
            page += 1

    # 모든 데이터를 포함하는 ElementTree 객체 생성
    all_data_tree = ET.ElementTree(all_data_element)

    return all_data_tree