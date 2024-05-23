from tkinter import *
import functions
from tkintermapview import TkinterMapView
import webbrowser

# 아예 chilepage를 따로떼서 북마크 눌렀을때 저기 추가하고
class DetailWindow:
    def __init__(self, parent, title, element, bookmark_callback):
        self.window = Toplevel(parent)
        self.window.title(title)
        self.window.geometry("400x400")

        self.element = element
        self.bookmark_callback = bookmark_callback

        self.setup_ui()

    def setup_ui(self):
        # 상세 정보를 출력할 프레임 생성
        self.label_frame = Frame(self.window, bd=2, relief="solid")
        self.label_frame.grid(row=0, column=0, padx=10, pady=10, sticky='w', columnspan=2)

        map_frame = Frame(self.window, bd=2, relief="solid")
        map_frame.grid(row=1, column=0, padx=10, pady=10, sticky='w')

        button_frame = Frame(self.window, bd=2, relief="solid")
        button_frame.grid(row=1, column=1, padx=10, pady=10, sticky='w')

        name_label = Label(self.label_frame, text="Name: " + self.element.find('culName').text)
        name_label.grid(row=0, sticky='w')

        tel_label = Label(self.label_frame, text="Tel: " + self.element.find('culTel').text)
        tel_label.grid(row=1, sticky='w')

        url_label = Label(self.label_frame, text="URL: click!", cursor="hand2", wraplength=300, justify="left")
        url_label.grid(row=2, sticky='w')
        url_label.bind("<Button-1>", lambda e: webbrowser.open_new(self.element.find('culHomeUrl').text))

        gps_label = Label(self.label_frame,
                          text="Location: " + self.element.find('gpsX').text + ", " + self.element.find('gpsY').text)
        gps_label.grid(row=3, sticky='w')

        gpsX = float(self.element.find('gpsX').text)
        gpsY = float(self.element.find('gpsY').text)

        gpsX = round(gpsX, 4)
        gpsY = round(gpsY, 4)

        addr = functions.get_address(gpsY, gpsX)
        addr_label = Label(self.label_frame, text="address: " + addr, wraplength=380)
        addr_label.grid(row=4, sticky='w')

        map_widget = TkinterMapView(map_frame, width=250, height=250, corner_radius=0)
        map_widget.pack(fill="both", expand=True)

        map_widget.set_position(gpsY, gpsX)
        map_widget.set_zoom(15)

        b = Button(button_frame, text="북마크", command=lambda: self.bookmark_callback(self.element), width=8, height=2)
        b.grid(row=0, column=0, padx=10, pady=10)
        b = Button(button_frame, text="이메일", command=self.email, width=8, height=2)
        b.grid(row=1, column=0, padx=10, pady=10)
        b = Button(button_frame, text="파일", command=self.file, width=8, height=2)
        b.grid(row=2, column=0, padx=10, pady=10)
        b = Button(button_frame, text="텔레그램", command=self.tele, width=8, height=2)
        b.grid(row=3, column=0, padx=10, pady=10)

    def email(self):
        pass

    def file(self):
        pass

    def tele(self):
        pass
