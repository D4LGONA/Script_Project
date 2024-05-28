from tkinter import *
from tkinter import ttk
from GUI.page1 import Page1
from GUI.page2 import Page2
from GUI.page3 import Page3
import functions

class MainGui:
    def setUI(self):
        # 페이지를 여러개 쓸 예정
        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(fill="both", expand=True)

        self.pages = []
        page1 = Frame(self.notebook)
        self.notebook.add(page1, text="문화공연 정보 검색")
        self.pages.append(page1)

        page2 = Frame(self.notebook)
        self.notebook.add(page2, text="문화공간 정보 검색")
        self.pages.append(page2)

        page3 = Frame(self.notebook)
        self.notebook.add(page3, text="북마크")
        self.pages.append(page3)

    def __init__(self):
        self.window = Tk()
        self.window.title("스크립트언어")
        self.window.geometry("600x600")
        self.x, self.y = functions.get_location()

        self.setUI()
        self.page1_instance = Page1(self.pages[0], self.x, self.y, self)
        self.page2_instance = Page2(self.pages[1], self.x, self.y, self)
        self.page3_instance = Page3(self.pages[2], self)

        self.window.mainloop()

