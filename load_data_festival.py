import requests
import xml.etree.ElementTree as ET

url = 'http://api.data.go.kr/openapi/tn_pubr_public_cltur_fstvl_api'
params ={'serviceKey' : 'ipA7GxlvIHVrsFJKg6yO/ihFWarSbbwT+hG6ejOQMISeS9BSPgbgsf08SbC9qwgBEjJlzzj/yYMNMbFhrUZ09A==', 'pageNo' : '1', 'numOfRows' : '1673', 'type' : 'xml'}

response = requests.get(url, params=params)
response.encoding = 'utf-8'
print(response.text)
root = ET.fromstring(response.text)