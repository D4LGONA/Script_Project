from tkinter import *
from load_data import *
from tkinter import ttk

class MainGui:
    def setUI(self):
        # 페이지를 여러개 쓸 예정
        # 페이지 1:
        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(fill="both", expand=True)

        self.pages = []
        page = Frame(self.notebook)
        self.notebook.add(page, text=f"탭 {i}")
        self.pages.append(page)




    def __init__(self):
        self.window = Tk()
        self.window.title("스크립트언어")

        self.window.mainloop()

