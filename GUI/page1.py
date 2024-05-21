from tkinter import *
class Page1:
    # todo: 지도 띄우기.


    def search(self):
        query = self.entry.get()  # 입력된 텍스트 가져오기
        # 여기에 검색을 수행하는 코드를 추가할 수 있습니다.
        print("검색어:", query)
    def __init__(self, parent_frame):
        # 새로운 프레임 생성
        self.frame = Frame(parent_frame)
        self.frame.grid(row=0, column=0, padx=5, pady=10)

        # 이미지 추가
        photo = PhotoImage(file="resources/r1.png")
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