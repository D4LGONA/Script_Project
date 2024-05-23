from tkinter import *
import functions

class Page3:
    def remove(self):
        selected_index = self.lb.curselection()
        if selected_index:  # 만약 항목이 선택되었다면
            selected_item = self.lb.get(selected_index[0])  # 선택된 항목의 인덱스를 사용하여 해당 항목을 가져옵니다.
            print("Selected item:", selected_item)

            # functions.bookmark_lists에서 선택된 항목을 삭제합니다.
            del functions.bookmark_lists[selected_index[0]]

            # 리스트박스 업데이트
            self.update_lb()
        else:
            print("No item selected.")  # 선택된 항목이 없을 경우에 대한 처리

    def file(self):
        # 파일 경로 설정
        file_path = "datas/bookmark_data.txt"

        # 파일에 저장할 내용 작성
        file_content = ""
        for element in functions.bookmark_lists:
            cul_name = element.find('culName').text
            cul_tel = element.find('culTel').text
            cul_home_url = element.find('culHomeUrl').text
            gps_x = element.find('gpsX').text
            gps_y = element.find('gpsY').text
            address = functions.get_address(float(gps_y), float(gps_x))
            file_content += f"Cultural Name: {cul_name}\n"
            file_content += f"Tel: {cul_tel}\n"
            file_content += f"URL: {cul_home_url}\n"
            file_content += f"Location: {gps_x}, {gps_y}\n"
            file_content += f"Address: {address}\n"
            file_content += "\n"  # 요소 사이에 빈 줄 추가

        # 파일에 내용 저장
        with open(file_path, 'w', encoding="utf-8") as file:
            file.write(file_content)

        print("Bookmark data saved to:", file_path)


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
        self.frame1.grid(row=0, column=0, padx=5, pady=10, sticky="w")

        photo = PhotoImage(file="resources/r3.png")
        resized_photo = photo.subsample(4, 4)
        label = Label(self.frame1, image=resized_photo)
        label.photo = resized_photo
        label.grid(row=0, column=0)

        # 텍스트 폰트 크기 설정
        img_height = resized_photo.height()
        font_size = -int(round(img_height / 2))  # 이미지의 높이의 절반을 폰트 크기로 설정

        # 북마크 텍스트 추가
        bookmark_label = Label(self.frame1, text="bookmark", padx=5, pady=10, font=("Helvetica", font_size))
        bookmark_label.grid(row=0, column=1, sticky="w")

        # 오른쪽 프레임
        self.frame2 = Frame(parent_frame, bd=2, relief="solid")
        self.frame2.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")

        # 리스트박스 추가
        self.lb = Listbox(self.frame2, width=70, height=20)
        self.lb.grid(row=0, column=0, sticky="nsew")  # 리스트박스를 그리드 셀에 배치
        self.lb.grid_columnconfigure(0, weight=1)  # 리스트박스의 열을 확장합니다.

        # 스크롤바 추가
        scrollbar = Scrollbar(self.frame2, orient=VERTICAL)
        scrollbar.config(command=self.lb.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")  # 스크롤바를 리스트박스 오른쪽에 배치

        # 리스트박스와 스크롤바 연결
        self.lb.config(yscrollcommand=scrollbar.set)

        # 버튼 프레임
        button_frame = Frame(self.frame2)
        button_frame.grid(row=0, column=2, padx=5, pady=10)  # 버튼 프레임을 그리드 셀에 배치

        # 버튼 추가
        button1 = Button(button_frame, text="파일", command=self.file)
        button1.pack(pady=5)
        button2 = Button(button_frame, text="삭제", command=self.remove)
        button2.pack(pady=5)
        button3 = Button(button_frame, text="이메일")
        button3.pack(pady=5)
        button4 = Button(button_frame, text="텔레그램")
        button4.pack(pady=5)

        self.update_lb()