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
from datetime import date, datetime
import traceback
import functions

# Constants
TOKEN = '7276299407:AAGpq-uyl1Hqodh_kx061KghULdzi0Rxp-E'
MAX_MSG_LENGTH = 300
BASE_URL = 'http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTrade?ServiceKey=' + KEY
DB_USERS = 'users.db'
DB_LOGS = 'logs.db'

# Initialize Bot
bot = telepot.Bot(TOKEN)
cache_list = []

# Function to get apartment data
def getData_place(string):
    res_list = []
    for place_list in functions.places_lists.iter('placeList'):
        cul_name = place_list.find('culName').text
        if string in cul_name:
            res_list.append(place_list)
    res_list.sort(key=lambda e: e.find('culName').text)
    return elements_to_string(res_list)


def elements_to_string(elements):
    body = ''
    for element in elements:
        body += f"#문화 장소 정보#\n"
        body += f"유형: {element.find('culGrpName').text}\n"
        body += f"이름: {element.find('culName').text}\n"
        body += f"전화번호: {element.find('culTel').text}\n"
        body += f"URL: {element.find('culHomeUrl').text}\n"
        body += f"위치: {element.find('gpsY').text}, {element.find('gpsX').text}\n"
        body += f"주소: {functions.get_address(float(element.find('gpsY').text), float(element.find('gpsX').text))}\n\n"

    # 하나의 문자열로 결합
    return body

def places_detail(seq):
    pass


# Function to send a message
def sendMessage(user, msg):
    try:
        bot.sendMessage(user, msg)
    except:
        traceback.print_exc(file=sys.stdout)

# Main function to run the bot
def run(date_param, default_loc='11710'):
    conn = sqlite3.connect(DB_LOGS)
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS logs(user TEXT, log TEXT, PRIMARY KEY(user, log))')
    conn.commit()

    user_conn = sqlite3.connect(DB_USERS)
    user_cursor = user_conn.cursor()
    user_cursor.execute('CREATE TABLE IF NOT EXISTS users(user TEXT, location TEXT, PRIMARY KEY(user, location))')
    user_cursor.execute('SELECT * FROM users')

    for user, loc in user_cursor.fetchall():
        res_list = getData(loc, date_param)
        msg = ''
        for r in res_list:
            try:
                cursor.execute('INSERT INTO logs (user, log) VALUES (?, ?)', (user, r))
            except sqlite3.IntegrityError:
                continue
            if len(msg + r + '\n') > MAX_MSG_LENGTH:
                sendMessage(user, msg)
                msg = r + '\n'
            else:
                msg += r + '\n'
        if msg:
            sendMessage(user, msg)
    conn.commit()
    user_conn.commit()

# Function to reply with apartment data
def replyAptData(date_param, user, loc_param='11710'):
    res_list = getData(loc_param, date_param)
    msg = ''
    for r in res_list:
        if len(msg + r + '\n') > MAX_MSG_LENGTH:
            sendMessage(user, msg)
            msg = r + '\n'
        else:
            msg += r + '\n'
    if msg:
        sendMessage(user, msg)
    else:
        sendMessage(user, f'{date_param} 기간에 해당하는 데이터가 없습니다.')

# Function to save user and location
def save(user, loc_param):
    conn = sqlite3.connect(DB_USERS)
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users(user TEXT, location TEXT, PRIMARY KEY(user, location))')
    try:
        cursor.execute('INSERT INTO users(user, location) VALUES (?, ?)', (user, loc_param))
        sendMessage(user, '저장되었습니다.')
    except sqlite3.IntegrityError:
        sendMessage(user, '이미 해당 정보가 저장되어 있습니다.')
    conn.commit()

# Function to check user's data
def check(user):
    conn = sqlite3.connect(DB_USERS)
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users(user TEXT, location TEXT, PRIMARY KEY(user, location))')
    cursor.execute('SELECT * FROM users WHERE user = ?', (user,))
    for data in cursor.fetchall():
        row = f'id: {data[0]}, location: {data[1]}'
        sendMessage(user, row)

# Function to handle messages
def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type != 'text':
        sendMessage(chat_id, '난 텍스트 이외의 메시지는 처리하지 못해요.')
        return

    text = msg['text']
    args = text.split(' ')

    if text.startswith('안녕') and len(args) > 1:
        sendMessage(chat_id, "안녕하세요!")
    elif text.startswith('장소검색') and len(args) > 1:
        search_string = ' '.join(args[1:])
        st = getData_place(search_string)
        sendMessage(chat_id, st)
    elif text.startswith('공연검색') and len(args) > 1:
        sendMessage(1,"11")
    else:
        sendMessage(chat_id, "무슨 말인지 이해하지 못했어요.")

# Main execution
if __name__ == '__main__':
    today = date.today()
    current_month = today.strftime('%Y%m')

    print(f'[{today}] received token: {TOKEN}')

    pprint(bot.getMe())

    run(current_month)

    bot.message_loop(handle)
    print('Listening...')

    while True:
        time.sleep(10)
