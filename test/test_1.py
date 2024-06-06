#6737669616
#6524393122:AAGNCH0i1f6dOsYikapuhFQnwL-8x5lWwLc

import telepot
bot = telepot.Bot('6524393122:AAGNCH0i1f6dOsYikapuhFQnwL-8x5lWwLc')
bot.getMe()
{'id': 6737669616, 'is_bot': True, 'first_name': '부동산 텔레그램 봇', 'username': 'realestate_prof_youngsik_bot'}
bot.sendMessage('6737669616','비비트트트비비트트트')

from urllib.request import urlopen
url ='http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTrade?serviceKey=sea100UMmw23Xycs33F1EQnumONR%2F9ElxBLzkilU9Yr1oT4TrCot8Y2p0jyuJP72x9rG9D8CN5yuEs6AS2sAiw%3D%3D&LAWD_CD=11110&DEAL_YMD=201712'
response = urlopen(url).read().decode('utf-8')
print(response)


