from tkinter import *
from tkinter import ttk
from GUI.page1 import Page1
from GUI.page2 import Page2
import functions

class MainGui:
    def setUI(self):
        # 페이지를 여러개 쓸 예정
        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(fill="both", expand=True)

        self.pages = []
        page1 = Frame(self.notebook)
        self.notebook.add(page1, text="축제 정보 검색")
        self.pages.append(page1)

        page2 = Frame(self.notebook)
        self.notebook.add(page2, text="공연장 정보 검색")
        self.pages.append(page2)


    def load_page_datas(self):
        pass

    def __init__(self):
        self.window = Tk()
        self.window.title("스크립트언어")
        self.window.geometry("600x600")
        self.x, self.y = functions.get_location()

        self.setUI()
        self.page1_instance = Page1(self.pages[0], self.x, self.y)  # page1 인스턴스 생성 및 콜백 함수 전달
        self.page2_instance = Page2(self.pages[1], self.x, self.y)

        self.window.mainloop()

