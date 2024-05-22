from tkinter import *
from tkinter import ttk
from load_data import *
import webbrowser
from tkintermapview import TkinterMapView

# todo: 위도경도로 주소받아오기
# todo: tkintermap에 마커 추가하기

class Page2:
    def reset_frame2(self):
        for widget in self.frame2.winfo_children():
            widget.destroy()
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

    def open_url(self, string):
        webbrowser.open_new(string)

    def print_element_info(self, element, parent_frame):
        type_label = Label(parent_frame, text="Type: " + element.find('culGrpName').text)
        type_label.pack(anchor='w')

        name_label = Label(parent_frame, text="Name: " + element.find('culName').text)
        name_label.pack(anchor='w')

        tel_label = Label(parent_frame, text="Tel: " + element.find('culTel').text)
        tel_label.pack(anchor='w')

        url_label = Label(parent_frame, text="URL: " + element.find('culHomeUrl').text, cursor="hand2", wraplength=300, justify="left")
        url_label.pack(anchor='w')
        url_label.bind("<Button-1>", lambda e: self.open_url(element.find('culHomeUrl').text))


        gps_label = Label(parent_frame,
                          text="Location: " + element.find('gpsX').text + ", " + element.find('gpsY').text)
        gps_label.pack(anchor='w')


    def search(self):
        # 결과를 출력할 프레임 생성
        for widget in self.frame2.winfo_children():
            widget.destroy()

        result_frame = Frame(self.frame2)
        result_frame.grid(row=1, columnspan=3, padx=5, pady=10)

        # 결과를 출력할 리스트박스 추가
        self.result_list = Listbox(result_frame, width=70, height=20)
        self.result_list.pack(side=LEFT, fill=BOTH, expand=True)

        # 스크롤바 추가
        scrollbar = Scrollbar(result_frame, orient=VERTICAL)
        scrollbar.config(command=self.result_list.yview)
        scrollbar.pack(side=RIGHT, fill=Y)

        # 리스트박스와 스크롤바 연결
        self.result_list.config(yscrollcommand=scrollbar.set)

        # 리스트박스 더블클릭 이벤트 바인딩
        self.result_list.bind("<Double-1>", self.on_double_click)

        query = self.entry.get()
        datas = self.search_by_et(query)
        # 결과 출력
        self.result_list.delete(0, END)  # 기존 결과를 지우고 새로운 검색 결과를 표시합니다.
        for element in datas:
            # 각 요소에서 공연장 이름을 가져와 리스트박스에 추가합니다.
            cul_name = element.find('culName').text
            self.result_list.insert(END, cul_name)



    def search_by_et(self, string):
        result = []
        for place_list in self.datas.iter('placeList'):
            cul_name = place_list.find('culName').text
            if string in cul_name:
                result.append(place_list)
        return result

    def on_double_click(self, event):
        index = self.result_list.curselection()[0]
        clicked_text = self.result_list.get(index)
        print("Clicked:", clicked_text)
        self.open_new_window(clicked_text)

    def open_new_window(self, clicked_text):
        new_window = Toplevel(self.frame1)
        new_window.title(clicked_text)
        new_window.geometry("400x400")
        label = Label(new_window, text=f"You clicked: {clicked_text}")
        label.pack()

        res = self.search_by_et(clicked_text)

        for i in res:
            self.print_element_info(i, new_window)

        # 새로운 창을 child_windows 리스트에 추가
        self.child_windows.append(new_window)

    def on_image_click(self):
        print("이미지 클릭!")
        self.reset_frame2()

    def __init__(self, parent_frame, x, y):
        self.x = x
        self.y = y
        self.datas = load_all_data_clubs()

        self.child_windows = []

        # 새로운 프레임 생성
        self.frame1 = Frame(parent_frame)
        self.frame1.grid(row=0, column=0, padx=5, pady=10)

        # 이미지 추가
        photo = PhotoImage(file="resources/r2.png")
        resized_photo = photo.subsample(4, 4)
        button = Button(self.frame1, image=resized_photo, command=self.on_image_click, bd=0, highlightthickness=0)
        button.photo = resized_photo  # 참조 유지를 위해 필요함
        button.grid(row=0, column=0, sticky=W, padx=5)


        # Entry 위젯 추가
        self.entry = Entry(self.frame1, width=50)  # 프레임에 추가
        self.entry.grid(row=0, column=1, padx=5, pady=10)  # 첫 번째 열에 배치

        # 검색 버튼 추가
        self.search_button = Button(self.frame1, text="검색", command=self.search, width=8, height=2)  # 프레임에 추가
        self.search_button.grid(row=0, column=2, padx=5, pady=10)  # 두 번째 열에 배치

        # 프레임2: 지도, 리스트박스
        self.frame2 = Frame(parent_frame)
        self.frame2.grid(row=1, column=0, padx=5, pady=10)

        self.reset_frame2()



