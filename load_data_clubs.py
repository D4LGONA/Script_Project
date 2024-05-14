# http://www.culture.go.kr/openapi/rest/cultureartspaces/performingplace?serviceKey=ipA7GxlvIHVrsFJKg6yO%2FihFWarSbbwT%2BhG6ejOQMISeS9BSPgbgsf08SbC9qwgBEjJlzzj%2FyYMNMbFhrUZ09A%3D%3D&cPage=10&rows=1&RequestTime=20100810:23003422

import requests
import xml.etree.ElementTree as ET

url = 'http://www.culture.go.kr/openapi/rest/cultureartspaces/performingplace'
params = {'serviceKey' : 'ipA7GxlvIHVrsFJKg6yO/ihFWarSbbwT+hG6ejOQMISeS9BSPgbgsf08SbC9qwgBEjJlzzj/yYMNMbFhrUZ09A==',
         'cPage' : '1',
         'rows' : '10'}

response = requests.get(url, params=params)
response.encoding = 'utf-8'
print(response.text)
root = ET.fromstring(response.text)