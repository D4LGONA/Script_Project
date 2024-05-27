from tkinter import *
import functions
from tkintermapview import TkinterMapView
import webbrowser
from tkinter import messagebox
from load_data import *
from PIL import Image, ImageTk
from io import BytesIO

# 아예 chilepage를 따로떼서 북마크 눌렀을때 저기 추가하고
class DetailWindow_place:
    def __init__(self, parentFrame, parent, title, element):
        self.topParent = parent
        self.window = Toplevel(parentFrame)
        self.window.title(title)
        self.window.geometry("400x400")

        self.element = element
        self.setup_ui()

    def setup_ui(self):
        # 상세 정보를 출력할 프레임 생성
        self.label_frame = Frame(self.window, bd=2, relief="solid")
        self.label_frame.grid(row=0, column=0, padx=10, pady=10, sticky='w', columnspan=2)

        map_frame = Frame(self.window, bd=2, relief="solid")
        map_frame.grid(row=1, column=0, padx=10, pady=10, sticky='w')

        button_frame = Frame(self.window, bd=2, relief="solid")
        button_frame.grid(row=1, column=1, padx=10, pady=10, sticky='w')

        name_label = Label(self.label_frame, text="Name: " + self.element.find('culName').text)
        name_label.grid(row=0, sticky='w')

        tel_label = Label(self.label_frame, text="Tel: " + self.element.find('culTel').text)
        tel_label.grid(row=1, sticky='w')

        url_label = Label(self.label_frame, text="URL: click!", cursor="hand2", wraplength=300, justify="left")
        url_label.grid(row=2, sticky='w')
        url_label.bind("<Button-1>", lambda e: webbrowser.open_new(self.element.find('culHomeUrl').text))

        gps_label = Label(self.label_frame,
                          text="Location: " + self.element.find('gpsX').text + ", " + self.element.find('gpsY').text)
        gps_label.grid(row=3, sticky='w')

        gpsX = float(self.element.find('gpsX').text)
        gpsY = float(self.element.find('gpsY').text)

        gpsX = round(gpsX, 4)
        gpsY = round(gpsY, 4)

        addr = functions.get_address(gpsY, gpsX)
        addr_label = Label(self.label_frame, text="address: " + addr, wraplength=380)
        addr_label.grid(row=4, sticky='w')

        map_widget = TkinterMapView(map_frame, width=250, height=250, corner_radius=0)
        map_widget.pack(fill="both", expand=True)

        map_widget.set_marker(gpsY, gpsX)

        map_widget.set_position(gpsY, gpsX)
        map_widget.set_zoom(15)

        b = Button(button_frame, text="북마크", command=lambda: self.bookmark(self.element), width=8, height=2)
        b.grid(row=0, column=0, padx=10, pady=10)
        b = Button(button_frame, text="이메일", command=self.email, width=8, height=2)
        b.grid(row=1, column=0, padx=10, pady=10)
        b = Button(button_frame, text="파일", command=lambda: self.file(self.element), width=8, height=2)
        b.grid(row=2, column=0, padx=10, pady=10)
        b = Button(button_frame, text="텔레그램", command=self.tele, width=8, height=2)
        b.grid(row=3, column=0, padx=10, pady=10)

    def email(self):
        pass

    def file(self, element):
        cul_name = element.find('culName').text
        file_path = "datas/" + cul_name + ".txt"

        # 파일에 저장할 내용 작성
        file_content = ""
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

        # 파일에 내용 저장
        with open(file_path, 'w', encoding="utf-8") as file:
            file.write(file_content)

        messagebox.showinfo("저장", file_path + "에 저장됨!")

    def tele(self): # todo
        pass

    def bookmark(self, element):
        t = len(functions.bookmark_lists)
        functions.bookmark_lists.append(element)
        if t != len(functions.bookmark_lists):
            self.topParent.page3_instance.update_lb()
            messagebox.showinfo("북마크", element.find('culName').text+" 저장 완료!")


class DetailWindow_perform:
    def __init__(self, parentFrame, parent, title, element):
        self.topParent = parent
        self.window = Toplevel(parentFrame)
        self.window.title(title)
        self.window.geometry("400x400")

        self.element = element
        self.setup_ui()

    def setup_ui(self):
        # 상세 정보를 출력할 프레임 생성
        self.label_frame = Frame(self.window, bd=2, relief="solid")
        self.label_frame.grid(row=0, column=0, padx=10, pady=10, sticky='w', columnspan=2)

        map_frame = Frame(self.window, bd=2, relief="solid")
        map_frame.grid(row=1, column=0, padx=10, pady=10, sticky='w')

        button_frame = Frame(self.window, bd=2, relief="solid")
        button_frame.grid(row=1, column=1, padx=10, pady=10, sticky='w')

        name_label = Label(self.label_frame, text="Name: " + self.element.find('title').text)
        name_label.grid(row=0, sticky='w')

        tel_label = Label(self.label_frame, text="Period: " + self.element.find('startDate').text+ " - "+self.element.find('endDate').text)
        tel_label.grid(row=1, sticky='w')

        url_label = Label(self.label_frame, text="URL: click!", cursor="hand2", wraplength=300, justify="left")
        url_label.grid(row=2, sticky='w')
        url_label.bind("<Button-1>", lambda e: webbrowser.open_new(self.element.find('culHomeUrl').text))

        gps_label = Label(self.label_frame,
                          text="place: " + self.element.find('place').text)
        gps_label.grid(row=3, sticky='w')

        url = self.element.find('thumbnail').text
        print(url)
        response = requests.get(url)
        image_data = response.content
        content_type = response.headers['Content-Type']

        # Content-Type이 이미지인지 확인
        if 'image' in content_type:
            image_data = response.content
            with open("image_data.jpg", "wb") as f:
                f.write(image_data)
        else:
            print("이미지 형식이 아닙니다:", content_type)

        image = Image.open(BytesIO(image_data))
        photo = ImageTk.PhotoImage(image)
        label = Label(map_frame, image=photo)
        label.pack()

        b = Button(button_frame, text="북마크", command=lambda: self.bookmark(self.element), width=8, height=2)
        b.grid(row=0, column=0, padx=10, pady=10)
        b = Button(button_frame, text="이메일", command=self.email, width=8, height=2)
        b.grid(row=1, column=0, padx=10, pady=10)
        b = Button(button_frame, text="파일", command=lambda: self.file(self.element), width=8, height=2)
        b.grid(row=2, column=0, padx=10, pady=10)
        b = Button(button_frame, text="텔레그램", command=self.tele, width=8, height=2)
        b.grid(row=3, column=0, padx=10, pady=10)

    def email(self):
        pass

    def file(self, element):
        cul_name = element.find('culName').text
        file_path = "datas/" + cul_name + ".txt"

        # 파일에 저장할 내용 작성
        file_content = ""
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

        # 파일에 내용 저장
        with open(file_path, 'w', encoding="utf-8") as file:
            file.write(file_content)

        messagebox.showinfo("저장", file_path + "에 저장됨!")

    def tele(self): # todo
        pass

    def bookmark(self, element):
        t = len(functions.bookmark_lists)
        functions.bookmark_lists.append(element)
        if t != len(functions.bookmark_lists):
            self.topParent.page3_instance.update_lb()
            messagebox.showinfo("북마크", element.find('culName').text+" 저장 완료!")