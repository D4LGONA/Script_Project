from GUI.maingui import *


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
import spam

# Constants
TOKEN = '7286917476:AAFtc6Nb3xzjTyW4muJWVAXL6Dw6F9hfFXw'
MAX_MSG_LENGTH = 500

# Initialize Bot
bot = telepot.Bot(TOKEN)
cache_list = []

def b_name(string):
    if string == '드세기둥' or string == '드럼세탁기와기타둥둥':
        text = "해님이가 기타치는 팀 이름!"
    elif string == 'Lacuna' or string == '라쿠나':
        text = '''  98년생 동갑내기들로 구성된 대한민국의 인디밴드. 멤버는 장경민(보컬,기타), 김호(베이스), 오이삭(드럼), 정민혁(기타)이 있다.\n영화 이터널 선샤인에 나오는 기억을 지워주는 회사인 'Lacuna'에서 제목을 따 온 노래를 작곡했고, 이후 밴드명으로 정했다.\n2021년 2월 1일 MPMG WEEK를 통해 해피로봇 레코드 소속 아티스트가 되었다.'''
    else:
        text = "그런거 몰라요."
    return text

# Function to get apartment data
def getData_place(string):
    res_list = []
    for place_list in functions.places_lists.iter('placeList'):
        cul_name = place_list.find('culName').text
        if string in cul_name:
            res_list.append(place_list)
    res_list.sort(key=lambda e: e.find('culName').text)
    return elements_to_string(res_list)

def getData_perform_days(string):
    res_list = []
    for perf_list in functions.perform_lists.iter('perforList'):
        if perf_list == None: continue
        if perf_list.find('title') == None: continue
        if perf_list.find('startDate').text == None or perf_list.find('endDate').text == None: continue
        if spam.is_date_in_range(perf_list.find('startDate').text, perf_list.find('endDate').text, string):
            res_list.append(perf_list)
    res_list.sort(key=lambda e: e.find('title').text)
    return elements_to_string_perf(res_list)

def getData_perform(string):
    res_list = []
    for perf_list in functions.perform_lists.iter('perforList'):
        if perf_list == None: continue
        if perf_list.find('title') == None: continue
        cul_name = perf_list.find('title').text
        if string in cul_name:
            res_list.append(perf_list)
    res_list.sort(key=lambda e: e.find('title').text)
    return elements_to_string_perf(res_list)

def elements_to_string(elements):
    body = ''
    if not elements:
        return "아무것도 없네요!"
    body += f"*문화 장소 정보*\n"
    for element in elements:
        body += f"{element.find('seq').text}"
        body += f" - {element.find('culName').text}\n"
    return body

def elements_to_string_perf(elements):
    body = ''
    if not elements:
        return "아무것도 없네요!"
    body += f"*문화 공연 정보*\n"
    for element in elements:
        body += f"{element.find('seq').text}"
        body += f" - {element.find('title').text}\n"
    return body

def places_detail(seq):
    body = "아무것도 없네요!"

    for element in functions.places_lists.iter('placeList'):
        if element.find("seq").text == seq:
            body = f"*문화 장소 정보*\n"
            body += f"번호: {element.find('seq').text}\n"
            body += f"유형: {element.find('culGrpName').text}\n"
            body += f"이름: {element.find('culName').text}\n"
            body += f"전화번호: {element.find('culTel').text}\n"
            body += f"URL: {element.find('culHomeUrl').text}\n"
            body += f"위치: {element.find('gpsY').text}, {element.find('gpsX').text}\n"
            body += f"주소: {functions.get_address(float(element.find('gpsY').text), float(element.find('gpsX').text))}\n\n"
    return body

def perform_detail(seq):
    body = "아무것도 없네요!"
    for element in functions.perform_lists.iter('perforList'):
        if element.find("seq").text == seq:
            body = f"*문화 공연 정보*\n"
            body += f"번호: {element.find('seq').text}\n"
            body += f"유형: {element.find('realmName').text}\n"
            body += f"이름: {element.find('title').text}\n"
            body += f"기간: {element.find('startDate').text + " - " + element.find('endDate').text}\n"
            body += f"장소: {element.find('place').text}\n\n"
    return body

# Function to send a message
def sendMessage(user, msg):
    tmp = msg
    try:
        while len(tmp) > MAX_MSG_LENGTH:
            send_part = tmp[:MAX_MSG_LENGTH]
            # 메시지의 최대 길이를 초과하는 경우 마지막 줄 바꿈 문자('\n')에서 자르기
            last_newline_index = send_part.rfind('\n')
            if last_newline_index != -1:
                send_part = send_part[:last_newline_index]  # 줄 바꿈 문자 포함하여 자르기
            bot.sendMessage(user, send_part)
            tmp = tmp[len(send_part):]  # 이미 보낸 부분은 제외
        else:
            bot.sendMessage(user, tmp)
    except:
        traceback.print_exc(file=sys.stdout)

# Function to handle messages
def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type != 'text':
        sendMessage(chat_id, '난 텍스트 이외의 메시지는 처리하지 못해요.')
        return

    text = msg['text']
    args = text.split(' ')

    if text.startswith('안녕'):
        sendMessage(chat_id, "안녕하세요! 저의 명령어는 다음과 같아요.\n장소검색 [장소이름]\n장소정보 [장소번호]\n공연검색 [공연이름]\n진행중공연 [YYYYMMDD]\n공연정보 [공연번호]\n[밴드이름] 알아?")
    elif text.startswith('장소검색') and len(args) > 1:
        search_string = ' '.join(args[1:])
        st = getData_place(search_string)
        sendMessage(chat_id, st)
    elif text.startswith('장소정보') and len(args) > 1:
        search_string = ' '.join(args[1:])
        st = places_detail(search_string)
        sendMessage(chat_id, st)
    elif text.startswith('공연검색') and len(args) > 1:
        search_string = ' '.join(args[1:])
        st = getData_perform(search_string)
        sendMessage(chat_id, st)
    elif text.startswith('공연정보') and len(args) > 1:
        search_string = ' '.join(args[1:])
        st = perform_detail(search_string)
        sendMessage(chat_id, st)
    elif text.startswith('진행중공연') and len(args) > 1:
        search_string = ' '.join(args[1:])
        if functions.is_valid_date(search_string):
            st = getData_perform_days(search_string)
            sendMessage(chat_id, st)
        else:
            sendMessage(chat_id, "잘못된 날짜를 입력했네요!")
    elif args[-1] == '알아?':
        sendMessage(chat_id, b_name(args[0]))
    else:
        sendMessage(chat_id, "무슨 말인지 이해하지 못했어요.")

# Main execution
if __name__ == '__main__':

    today = date.today()
    print(f'[{today}] received token: {TOKEN}')
    pprint(bot.getMe())

    bot.message_loop(handle)
    print('Listening...')

    MainGui()

