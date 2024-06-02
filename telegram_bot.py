#!/usr/bin/python
# coding=utf-8

import sys
import time
import sqlite3
import telepot
from pprint import pprint
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from datetime import date, datetime, timedelta
import traceback

#!/usr/bin/python
# coding=utf-8

import sys
import time
import sqlite3
import telepot
from pprint import pprint
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from datetime import date, datetime, timedelta
import traceback

key = '여기에 API KEY를 입력하세요'
TOKEN = '7276299407:AAGpq-uyl1Hqodh_kx061KghULdzi0Rxp-E'
MAX_MSG_LENGTH = 300
baseurl = 'http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTrade?ServiceKey='+key
bot = telepot.Bot(TOKEN)

def getData(loc_param, date_param):
    res_list = []
    url = baseurl+'&LAWD_CD='+loc_param+'&DEAL_YMD='+date_param
    #print(url)
    res_body = urlopen(url).read()
    #print(res_body)
    soup = BeautifulSoup(res_body, 'html.parser')
    items = soup.findAll('item')
    for item in items:
        item = re.sub('<.*?>', '|', item.text)
        parsed = item.split('|')
        try:
            row = parsed[3]+'/'+parsed[6]+'/'+parsed[7]+', '+parsed[4]+' '+parsed[5]+', '+parsed[8]+'m², '+parsed[11]+'F, '+parsed[1].strip()+'만원\n'
        except IndexError:
            row = item.replace('|', ',')

        if row:
            res_list.append(row.strip())
    return res_list

def sendMessage(user, msg):
    try:
        bot.sendMessage(user, msg)
    except:
        traceback.print_exc(file=sys.stdout)

def run(date_param, param='11710'):
    conn = sqlite3.connect('logs.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS logs( user TEXT, log TEXT, PRIMARY KEY(user, log) )')
    conn.commit()

    user_cursor = sqlite3.connect('users.db').cursor()
    user_cursor.execute('CREATE TABLE IF NOT EXISTS users( user TEXT, location TEXT, PRIMARY KEY(user, location) )')
    user_cursor.execute('SELECT * from users')

    for data in user_cursor.fetchall():
        user, param = data[0], data[1]
        print(user, date_param, param)
        res_list = getData( param, date_param )
        msg = ''
        for r in res_list:
            try:
                cursor.execute('INSERT INTO logs (user,log) VALUES ("%s", "%s")'%(user,r))
            except sqlite3.IntegrityError:
                # 이미 해당 데이터가 있다는 것을 의미합니다.
                pass
            else:
                print( str(datetime.now()).split('.')[0], r )
                if len(r+msg)+1>MAX_MSG_LENGTH:
                    sendMessage( user, msg )
                    msg = r+'\n'
                else:
                    msg += r+'\n'
        if msg:
            sendMessage( user, msg )
    conn.commit()

if __name__=='__main__':
    today = date.today()
    current_month = today.strftime('%Y%m')

    print( '[',today,']received token :', TOKEN )

    pprint( bot.getMe() )

    run(current_month)



def replyAptData(date_param, user, loc_param='11710'):
    print(user, date_param, loc_param)
    res_list = getData( loc_param, date_param )
    msg = ''
    for r in res_list:
        print( str(datetime.now()).split('.')[0], r )
        if len(r+msg)+1>MAX_MSG_LENGTH:
            sendMessage( user, msg )
            msg = r+'\n'
        else:
            msg += r+'\n'
    if msg:
        sendMessage( user, msg )
    else:
        sendMessage( user, '%s 기간에 해당하는 데이터가 없습니다.'%date_param )

def save( user, loc_param ):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users( user TEXT, location TEXT, PRIMARY KEY(user, location) )')
    try:
        cursor.execute('INSERT INTO users(user, location) VALUES ("%s", "%s")' % (user, loc_param))
    except sqlite3.IntegrityError:
        sendMessage( user, '이미 해당 정보가 저장되어 있습니다.' )
        return
    else:
        sendMessage( user, '저장되었습니다.' )
        conn.commit()

def check( user ):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users( user TEXT, location TEXT, PRIMARY KEY(user, location) )')
    cursor.execute('SELECT * from users WHERE user="%s"' % user)
    for data in cursor.fetchall():
        row = 'id:' + str(data[0]) + ', location:' + data[1]
        sendMessage( user, row )


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type != 'text':
        sendMessage(chat_id, '난 텍스트 이외의 메시지는 처리하지 못해요.')
        return

    text = msg['text']
    args = text.split(' ')

    if text.startswith('안녕') and len(args)>1:
        sendMessage(chat_id, "안녕하세요!")
    else:
        sendMessage(chat_id, "무슨 말인지 이해하지 못했어요.")


today = date.today()
current_month = today.strftime('%Y%m')

print( '[',today,']received token :', TOKEN )

bot = telepot.Bot('7276299407:AAGpq-uyl1Hqodh_kx061KghULdzi0Rxp-E')
pprint( bot.getMe() )

bot.message_loop(handle)

print('Listening...')

while 1:
  time.sleep(10)