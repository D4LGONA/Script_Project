from tkinter import *
from tkinter import ttk
from load_data import *
from GUI.child_page import *
from tkinter import messagebox
from functions import *
from tkinter.ttk import Combobox


class Page2:
    def graph(self):
        selected_category = self.category_combobox.get()
        if selected_category == '공연장':
            main("datas/locations_clubs.txt", self.frame1)
        elif selected_category == '미술관':
            main("datas/locations_arts.txt", self.frame1)
        elif selected_category == '박물관':
            main("datas/locations_mus.txt", self.frame1)
        elif selected_category == "문화/복지/시군구회관":
            main("datas/locations_halls.txt", self.frame1)
        elif selected_category == '도서관':
            main("datas/locations_libs.txt", self.frame1)
        else:
            messagebox.showerror("에러", "콤보박스의 값을 변경해야 함!")


    def reset_frame2(self):
        for widget in self.frame2.winfo_children():
            widget.destroy()
        self.map()

        self.listbox_list = []

        self.listbox = Listbox(self.frame2)
        self.listbox.grid(row=1, column=1, sticky="nsew", padx=20)
        self.listbox.bind("<Double-1>", self.on_double_click2)

        # 데이터를 가나다순으로 정렬하여 리스트박스에 삽입
        sorted_data = sorted(self.lb_datas.iter('placeList'), key=lambda e: e.find('culName').text)
        for e in sorted_data:
            self.listbox.insert(END, e.find('culName').text)
            self.listbox_list.append(e)

        self.label = Label(self.frame2, text="근처에 있는 문화공간들!")
        self.label.grid(row=0, column=1, sticky="n", padx=20, pady=5)


    def map(self):
        self.map_frame = Frame(self.frame2)
        self.map_frame.grid(row=1, column=0, sticky="nsew")

        self.map_widget = TkinterMapView(self.map_frame, width=300, height=350, corner_radius=0)
        self.map_widget.pack(fill="both", expand=True, padx=40)

        for e in self.datas.iter('placeList'):
            gpsX = float(e.find('gpsX').text)
            gpsY = float(e.find('gpsY').text)
            try:
                self.map_widget.set_marker(gpsY, gpsX, e.find('culName').text)
            except:
                pass

        self.map_widget.set_position(self.x, self.y)
        self.map_widget.set_zoom(15)

    def open_url(self, string):
        webbrowser.open_new(string)

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
            cul_name = element.find('culName').text
            self.result_list.insert(END, cul_name)

    def search_by_et(self, string):
        selected_category = self.category_combobox.get()
        result = []
        self.listbox_list = []

        for place_list in self.datas.iter('placeList'):
            cul_name = place_list.find('culName').text
            if string in cul_name and (selected_category == '전체' or place_list.find('culGrpName').text == selected_category):
                result.append(place_list)
                self.listbox_list.append(place_list)
        result.sort(key=lambda e: e.find('culName').text)
        self.listbox_list.sort(key=lambda e: e.find('culName').text)
        return result

    def on_double_click(self, event):
        index = self.result_list.curselection()[0]
        clicked = self.listbox_list[index]
        DetailWindow_place(self.frame1, self.parent, clicked.find('culName').text, clicked)

    def on_double_click2(self, event):
        index = self.listbox.curselection()[0]
        clicked = self.listbox_list[index]
        DetailWindow_place(self.frame1, self.parent, clicked.find('culName').text, clicked)

    def on_image_click(self):
        self.reset_frame2()

    def __init__(self, parent_frame, x, y, parent):
        self.parent = parent
        self.x = x
        self.y = y
        td1 = load_all_data_clubs()
        td2 = load_all_data_mus()
        td3 = load_all_data_arts()
        td4 = load_all_data_halls()
        td5 = load_all_data_libs()
        troot = td1.getroot()
        troot.extend(td2.getroot())
        troot.extend(td3.getroot())
        troot.extend(td4.getroot())
        troot.extend(td5.getroot())
        self.datas = ET.ElementTree(troot)


        all_data_element = ET.Element('all_data')
        for e in self.datas.iter('placeList'):
            if calculate_distance(float(e.find('gpsY').text), float(e.find('gpsX').text), self.x, self.y) < 10: # todo: 거리를 어떻게할까
                all_data_element.append(e)

        self.lb_datas = ET.ElementTree(all_data_element)

        self.frame1 = Frame(parent_frame)
        self.frame1.grid(row=0, column=0, padx=5, pady=10)

        photo = PhotoImage(file="resources/r2.png")
        resized_photo = photo.subsample(4, 4)
        button = Button(self.frame1, image=resized_photo, command=self.on_image_click, bd=0, highlightthickness=0)
        button.photo = resized_photo
        button.grid(row=0, column=0, sticky=W, padx=5, rowspan=2)

        self.entry = Entry(self.frame1, width=50)
        self.entry.grid(row=0, column=1, padx=5, pady=10)

        self.search_button = Button(self.frame1, text="검색", command=self.search, width=8, height=2)
        self.search_button.grid(row=0, column=2, padx=5, pady=0)

        self.graph_button = Button(self.frame1, text="그래프", command=self.graph, width=8, height=2)
        self.graph_button.grid(row=1, column=2, padx=5, pady=0)

        self.category_combobox = Combobox(self.frame1, values=["전체", "공연장", "미술관", "박물관", "문화/복지/시군구회관", "도서관"], state="readonly")
        self.category_combobox.set("전체")  # 초기값 설정
        self.category_combobox.grid(row=1, column=1, padx=5, pady=10)

        self.frame2 = Frame(parent_frame)
        self.frame2.grid(row=1, column=0, padx=5, pady=10)

        self.reset_frame2()