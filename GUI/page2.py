from tkinter import *
from tkinter import ttk
from load_data import *
import webbrowser

class Page2:
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
        new_window = Toplevel(self.frame)
        new_window.title(clicked_text)
        new_window.geometry("400x400")
        label = Label(new_window, text=f"You clicked: {clicked_text}")
        label.pack()

        res = self.search_by_et(clicked_text)

        for i in res:
            self.print_element_info(i, new_window)

        # 새로운 창을 child_windows 리스트에 추가
        self.child_windows.append(new_window)

    def __init__(self, parent_frame):
        self.datas = load_all_data_clubs()

        self.child_windows = []

        # 새로운 프레임 생성
        self.frame = Frame(parent_frame)
        self.frame.grid(row=0, column=0, padx=5, pady=10)

        # 이미지 추가
        photo = PhotoImage(file="resources/r2.png")
        resized_photo = photo.subsample(4, 4)
        label = Label(self.frame, image=resized_photo)
        label.photo = resized_photo
        label.grid(row=0, column=0, sticky=W, padx=5)

        # Entry 위젯 추가
        self.entry = Entry(self.frame, width=50)  # 프레임에 추가
        self.entry.grid(row=0, column=1, padx=5, pady=10)  # 첫 번째 열에 배치

        # 검색 버튼 추가
        self.search_button = Button(self.frame, text="검색", command=self.search)  # 프레임에 추가
        self.search_button.grid(row=0, column=2, padx=5, pady=10)  # 두 번째 열에 배치

        # 결과를 출력할 프레임 생성
        result_frame = Frame(self.frame)
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
