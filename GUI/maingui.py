from tkinter import *
from tkinter import ttk
from GUI.page1 import Page1


class MainGui:
    def setUI(self):
        # 페이지를 여러개 쓸 예정
        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(fill="both", expand=True)

        self.pages = []
        page = Frame(self.notebook)
        self.notebook.add(page, text="main")
        self.pages.append(page)

    def search(self):
        query = self.page1_instance.entry.get()  # 입력된 텍스트 가져오기
        # 여기에 검색을 수행하는 코드를 추가할 수 있습니다.
        print("검색어:", query)

    def load_page_datas(self):
        pass  # 페이지 데이터를 로드하는 코드 추가

    def __init__(self):
        self.window = Tk()
        self.window.title("스크립트언어")
        self.window.geometry("600x600")

        self.setUI()
        self.page1_instance = Page1(self.pages[0], self.search)  # page1 인스턴스 생성 및 콜백 함수 전달

        self.window.mainloop()

