from tkinter import *
from tkintermapview import TkinterMapView
import functions
from load_data import *
from GUI.child_page import *

class Page1:
    def reset_frame2(self):
        for widget in self.frame2.winfo_children():
            widget.destroy()
        self.map()

        self.listbox = Listbox(self.frame2)
        self.listbox.grid(row=1, column=1, sticky="nsew", padx=20)
        self.listbox.bind("<Double-1>", self.on_double_click2)

        self.listbox_list = []

        for e in self.lb_datas.iter('perforList'):
            self.listbox.insert(END, e.find('title').text)
            self.listbox_list.append(e)

        self.label = Label(self.frame2, text="현재 진행중인 공연!")
        self.label.grid(row=0, column=1, sticky="n", padx=20, pady=5)

    def map(self):
        self.map_frame = Frame(self.frame2)
        self.map_frame.grid(row=1, column=0, sticky="nsew")

        self.map_widget = TkinterMapView(self.map_frame, width=300, height=350, corner_radius=0)
        self.map_widget.pack(fill="both", expand=True, padx=40)

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
            cul_name = element.find('title').text
            self.result_list.insert(END, cul_name)

    def search_by_et(self, string):
        result = []
        self.listbox_list = []
        for element in self.datas.iter('perforList'):
            if element is None:
                continue
            title_element = element.find('title')
            if title_element is not None and title_element.text:
                cul_name = title_element.text
                if string in cul_name:
                    result.append(element)
                    self.listbox_list.append(element)
        return result


    def on_double_click(self, event):
        index = self.result_list.curselection()[0]
        clicked = self.listbox_list[index]
        DetailWindow_perform(self.frame1, self.parent, clicked.find('title').text, clicked)

    def on_double_click2(self, event):
        index = self.listbox.curselection()[0]
        clicked = self.listbox_list[index]

        DetailWindow_perform(self.frame1, self.parent, clicked.find('title').text, clicked)

    def on_image_click(self):
        self.reset_frame2()

    def __init__(self, parent_frame, x, y, parent):
        self.parent = parent
        self.x = x
        self.y = y
        self.datas = load_data_performs()
        self.lb_datas = load_by_period()

        self.frame1 = Frame(parent_frame)
        self.frame1.grid(row=0, column=0, padx=5, pady=10)

        photo = PhotoImage(file="resources/r1.png")
        resized_photo = photo.subsample(4, 4)
        button = Button(self.frame1, image=resized_photo, command=self.on_image_click, bd=0, highlightthickness=0)
        button.photo = resized_photo
        button.grid(row=0, column=0, sticky=W, padx=5)

        self.entry = Entry(self.frame1, width=50)
        self.entry.grid(row=0, column=1, padx=5, pady=10)

        self.search_button = Button(self.frame1, text="검색", command=self.search, width=8, height=2)
        self.search_button.grid(row=0, column=2, padx=5, pady=10)

        self.frame2 = Frame(parent_frame)
        self.frame2.grid(row=1, column=0, padx=5, pady=10)

        self.reset_frame2()

