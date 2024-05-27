from tkinter import *
from tkintermapview import TkinterMapView
import functions
from load_data import *

class Page1:
    def on_double_click(self, event):
        index = self.result_list.curselection()[0]
        clicked_text = self.result_list.get(index)
        res = self.search_by_et(clicked_text)

        for element in res:
            DetailWindow(self.frame1, self.parent, clicked_text, element)

    def search(self):
        for widget in self.frame2.winfo_children():
            widget.destroy()

        result_frame = Frame(self.frame2)
        result_frame.grid(row=1, columnspan=3, padx=5, pady=10)

        self.result_list = Listbox(result_frame, width=70, height=20)
        self.result_list.pack(side=LEFT, fill=BOTH, expand=True)

        scrollbar = Scrollbar(result_frame, orient=VERTICAL)
        scrollbar.config(command=self.result_list.yview)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.result_list.config(yscrollcommand=scrollbar.set)
        self.result_list.bind("<Double-1>", self.on_double_click)

        query = self.entry.get()
        datas = self.search_by_et(query)
        self.result_list.delete(0, END)
        for element in datas:
            cul_name = element.find('title').text
            self.result_list.insert(END, cul_name)

    def search_by_et(self, string):
        result = []
        for place_list in self.datas.iter('perforList'):
            cul_name = place_list.find('title').text
            if string in cul_name:
                result.append(place_list)
        return result

    def map(self):
        # 지도를 표시할 새로운 프레임 생성
        self.map_frame = Frame(self.frame2)
        self.map_frame.grid(row=1, column=0, sticky="nsew")

        # 지도 위젯 생성 및 설정
        self.map_widget = TkinterMapView(self.map_frame, width=300, height=350, corner_radius=0)
        self.map_widget.pack(fill="both", expand=True, padx=40)

        # 초기 지도 위치 설정 (위도, 경도 및 확대 수준)
        self.map_widget.set_position(self.x, self.y)
        self.map_widget.set_zoom(15)

        for widget in self.frame2.winfo_children():
            widget.destroy()

        result_frame = Frame(self.frame2)
        result_frame.grid(row=1, columnspan=3, padx=5, pady=10)

        self.result_list = Listbox(result_frame, width=70, height=20)
        self.result_list.pack(side=LEFT, fill=BOTH, expand=True)

        scrollbar = Scrollbar(result_frame, orient=VERTICAL)
        scrollbar.config(command=self.result_list.yview)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.result_list.config(yscrollcommand=scrollbar.set)
        self.result_list.bind("<Double-1>", self.on_double_click)

        query = self.entry.get()
        datas = self.search_by_et(query)
        self.result_list.delete(0, END)
        for element in datas:
            cul_name = element.find('culName').text
            self.result_list.insert(END, cul_name)

    def search_by_et(self, string):
        result = []
        for place_list in self.datas.iter('placeList'):
            cul_name = place_list.find('culName').text
            if string in cul_name:
                result.append(place_list)
        return result

    def __init__(self, parent_frame, x, y):
        self.x = x
        self.y = y
        self.datas = load_data_performs()
        # 프레임1: 이미지, 엔트리, 버튼
        self.frame1 = Frame(parent_frame)
        self.frame1.grid(row=0, column=0, padx=5, pady=10)

        # 이미지 추가
        photo = PhotoImage(file="resources/r1.png")
        resized_photo = photo.subsample(4, 4)
        label = Label(self.frame1, image=resized_photo)
        label.photo = resized_photo
        label.grid(row=0, column=0, sticky=W, padx=5)

        # Entry 위젯 추가
        self.entry = Entry(self.frame1, width=50)  # 프레임에 추가
        self.entry.grid(row=0, column=1, padx=5, pady=10)  # 첫 번째 열에 배치

        # 검색 버튼 추가
        self.search_button = Button(self.frame1, text="검색", command=self.search, width=8, height=2)  # 프레임에 추가
        self.search_button.grid(row=0, column=2, padx=5, pady=10)  # 두 번째 열에 배치

        # 프레임2: 지도, 리스트박스
        self.frame2 = Frame(parent_frame)
        self.frame2.grid(row=1, column=0, padx=5, pady=10)

        # 지도 추가
        self.map()

        # 리스트박스 추가
        self.listbox = Listbox(self.frame2)
        self.listbox.grid(row=1, column=1, sticky="nsew", padx=20)

        # 리스트박스에 아이템 추가
        self.listbox.insert(END, "Item 1")
        self.listbox.insert(END, "Item 2")
        self.listbox.insert(END, "Item 3")

        # 라벨 추가
        self.label = Label(self.frame2, text="리스트박스 위에 라벨")
        self.label.grid(row=0, column=1, sticky="n", padx=20, pady=5)

