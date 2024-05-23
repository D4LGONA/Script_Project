from tkinter import *
import functions

class Page3:



    def update_lb(self):
        self.lb.delete(0, END)  # 기존 결과를 지우고 새로운 검색 결과를 표시합니다.
        for element in functions.bookmark_lists:
            # 각 요소에서 공연장 이름을 가져와 리스트박스에 추가합니다.
            cul_name = element.find('culName').text
            self.lb.insert(END, cul_name)

    def __init__(self, parent_frame):
        # 메인 라벨
        # 리스트박스 하나 개크게 만들기
        # 리스트박스 안의 내용은.. functions.bookmarks 리스트에 있음
        self.frame1 = Frame(parent_frame, bd=2, relief="solid")
        self.frame1.grid(row=0, column=0, padx=5, pady=10)

        photo = PhotoImage(file="resources/r3.png")
        resized_photo = photo.subsample(4, 4)
        label = Label(self.frame1, image=resized_photo)
        label.photo = resized_photo
        label.pack(side=LEFT)

        self.frame2 = Frame(parent_frame, bd=2, relief="solid")
        self.frame2.grid(row=1, column=0, padx=5, pady=10)

        # 결과를 출력할 리스트박스 추가
        self.lb = Listbox(self.frame2, width=70, height=20)
        self.lb.pack(side=LEFT, fill=BOTH, expand=True)

        # 스크롤바 추가
        scrollbar = Scrollbar(self.frame2, orient=VERTICAL)
        scrollbar.config(command=self.lb.yview)
        scrollbar.pack(side=RIGHT, fill=Y)

        # 리스트박스와 스크롤바 연결
        self.lb.config(yscrollcommand=scrollbar.set)

        self.update_lb()