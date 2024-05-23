from tkinter import *
from functions import *

# 아예 chilepage를 따로떼서 북마크 눌렀을때 저기 추가하고
class child_page:
    def print_element_info(self, element, parent_frame):
        Label_frame = Frame(parent_frame, bd=2, relief="solid")
        Label_frame.grid(row=0, column=0, padx=10, pady=10, sticky='w', columnspan=2)

        map_frame = Frame(parent_frame, bd=2, relief="solid")
        map_frame.grid(row=1, column=0, padx=10, pady=10, sticky='w')

        button_frame = Frame(parent_frame, bd=2, relief="solid")
        button_frame.grid(row=1, column=1, padx=10, pady=10, sticky='w')

        name_label = Label(Label_frame, text="Name: " + element.find('culName').text)
        name_label.grid(row=0, sticky='w')

        tel_label = Label(Label_frame, text="Tel: " + element.find('culTel').text)
        tel_label.grid(row=1, sticky='w')

        url_label = Label(Label_frame, text="URL: click!", cursor="hand2", wraplength=300, justify="left")
        url_label.grid(row=2, sticky='w')
        url_label.bind("<Button-1>", lambda e: self.open_url(element.find('culHomeUrl').text))

        gps_label = Label(Label_frame,
                          text="Location: " + element.find('gpsX').text + ", " + element.find('gpsY').text)
        gps_label.grid(row=3, sticky='w')

        gpsX = float(element.find('gpsX').text)
        gpsY = float(element.find('gpsY').text)

        # 소수점 4번째 자리까지 반올림
        gpsX = round(gpsX, 4)
        gpsY = round(gpsY, 4)

        # 수정된 위도와 경도를 사용하여 주소 가져오기
        addr = functions.get_address(gpsY, gpsX)
        addr_label = Label(Label_frame, text="address: " + addr, wraplength=380)
        addr_label.grid(row=4, sticky='w')

        map_widget = TkinterMapView(map_frame, width=250, height=250, corner_radius=0)
        map_widget.pack(fill="both", expand=True)

        # 초기 지도 위치 설정 (위도, 경도 및 확대 수준)
        map_widget.set_position(gpsY, gpsX)
        map_widget.set_zoom(15)

        b = Button(button_frame, text="북마크", command=self.search, width=8, height=2)
        b.grid(row=0, column=0, padx=10, pady=10)
        b = Button(button_frame, text="이메일", command=self.search, width=8, height=2)
        b.grid(row=1, column=0, padx=10, pady=10)
        b = Button(button_frame, text="파일", command=self.search, width=8, height=2)
        b.grid(row=2, column=0, padx=10, pady=10)
        b = Button(button_frame, text="텔레그램", command=self.search, width=8, height=2)
        b.grid(row=3, column=0, padx=10, pady=10)
    def __init__(self):
        pass