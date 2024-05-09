import requests
import xml.etree.ElementTree as ET

'''
https://www.data.go.kr/data/15013104/standard.do <- 전국문화축제표준데이터 읽어오는 방법
1. url: http://api.data.go.kr/openapi/tn_pubr_public_cltur_fstvl_api
2. 인증키(해님이 것): ipA7GxlvIHVrsFJKg6yO/ihFWarSbbwT+hG6ejOQMISeS9BSPgbgsf08SbC9qwgBEjJlzzj/yYMNMbFhrUZ09A==
3. 파라미터 값들(순서대로 입력, 만약 사용하지 않는 파라미터라면 **공백으로 놔두지 말고 딕셔너리에서 삭제해야 함**)
 'serviceKey' : 'ipA7GxlvIHVrsFJKg6yO/ihFWarSbbwT+hG6ejOQMISeS9BSPgbgsf08SbC9qwgBEjJlzzj/yYMNMbFhrUZ09A==', -> 수정 x
 'pageNo' : '1', 
 'numOfRows' : '100', 
 'type' : 'xml', -> 수정 x
 'fstvlNm' : '', -> 축제 이름
 'opar' : '', -> 개최장소
 'fstvlStartDate' : '', -> 축제 시작일자: YYYY-MM-DD 형식으로 작성
 'fstvlEndDate' : '', -> 축제 종료일자: YYYY-MM-DD 형식으로 작성
 'fstvlCo' : '', -> 축제내용 ?
 'mnnstNm' : '', -> 주관기관명
 'auspcInsttNm' : '', -> 주최기관명
 'suprtInsttNm' : '', -> 후원기관명
 'phoneNumber' : '',  -> 전화번호
 'homepageUrl' : '', -> 홈페이지
 'relateInfo' : '', ->관련정보
 'rdnmadr' : '', ->도로명주소
 'lnmadr' : '', ->지번주소
 'latitude' : '', ->위도
 'longitude' : '', ->경도
 'referenceDate' : '', ->데이터기준일자?
 'instt_code' : '', ->제공기관코드?
 'instt_nm' : ''->제공기관기관명?
'''


url = 'http://api.data.go.kr/openapi/tn_pubr_public_cltur_fstvl_api'
params ={'serviceKey' : 'ipA7GxlvIHVrsFJKg6yO/ihFWarSbbwT+hG6ejOQMISeS9BSPgbgsf08SbC9qwgBEjJlzzj/yYMNMbFhrUZ09A==', 'pageNo' : '1', 'numOfRows' : '100', 'type' : 'xml'}


response = requests.get(url, params=params)
response.encoding = 'utf-8'
print(response.text)
root = ET.fromstring(response.text)