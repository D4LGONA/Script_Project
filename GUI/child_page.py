from tkinter import *
import functions
from tkintermapview import TkinterMapView
import webbrowser
from tkinter import messagebox
from load_data import *
from PIL import Image, ImageTk
from io import BytesIO
from tkinter import simpledialog
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from itertools import count

class DetailWindow_place:
    def __init__(self, parentFrame, parent, title, element):
        self.topParent = parent
        self.window = Toplevel(parentFrame)
        self.window.title(title)
        self.window.geometry("400x400")

        self.root = parentFrame
        self.element = element
        self.setup_ui()

    def update_animation(self):
        if self.running:
            try:
                # 현재 프레임 인덱스를 업데이트하고 버튼 이미지를 설정합니다
                self.frame_index = (self.frame_index + 1) % len(self.frames)
                self.my_button.configure(image=self.frames[self.frame_index])
                self.root.after(100, self.update_animation)  # 필요에 따라 지연 시간을 조정합니다
            except:
                self.on_closing()

    def on_closing(self):
        self.running = False  # 애니메이션 루프 플래그 비활성화

    def setup_ui(self):
        # 상세 정보를 출력할 프레임 생성
        self.label_frame = Frame(self.window)
        self.label_frame.grid(row=0, column=0, padx=10, pady=10, sticky='w', columnspan=2)

        map_frame = Frame(self.window)
        map_frame.grid(row=1, column=0, padx=10, pady=10, sticky='w')

        button_frame = Frame(self.window)
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
        self.frames = []
        for i in count():
            try:
                frame = PhotoImage(file="resources/bc.gif", format=f"gif -index {i}")
                resized_frame = frame.subsample(8, 8)  # 크기를 조정합니다
                self.frames.append(resized_frame)
            except Exception:
                break

        self.frame_index = 0
        self.my_button = Button(button_frame, text="", image=self.frames[self.frame_index])
        self.my_button.grid(row=3, column=0, padx=10, pady=10)

        self.running = True  # 애니메이션 루프 플래그

        self.update_animation()

    def email(self):
        recipient_email = simpledialog.askstring("이메일 전송", "수신자의 이메일 주소를 입력하세요:")
        if recipient_email:
            try:
                # 이메일 전송을 위한 SMTP 서버 설정
                smtp_server = 'smtp.gmail.com'
                smtp_port = 587  # Gmail SMTP 포트 번호
                sender_email = 'elephant2297@tukorea.ac.kr'  # 보내는 사람의 이메일 주소
                sender_password = 'pxhe zyov urbc itoe'  # 보내는 사람의 이메일 비밀번호

                # 이메일 제목과 내용 작성
                subject = "문화 장소 정보"
                body = f"#문화 장소 정보#\n"
                body += f"이름: {self.element.find('culName').text}\n"
                body += f"전화번호: {self.element.find('culTel').text}\n"
                body += f"URL: {self.element.find('culHomeUrl').text}\n"
                body += f"위치: {self.element.find('gpsY').text}, {self.element.find('gpsX').text}\n"
                body += f"주소: {functions.get_address(float(self.element.find('gpsY').text), float(self.element.find('gpsX').text))}\n"

                # MIME 메시지 생성
                message = MIMEMultipart()
                message['From'] = formataddr(('Sender', sender_email))
                message['To'] = recipient_email
                message['Subject'] = subject
                message.attach(MIMEText(body, 'plain'))

                # SMTP 서버에 연결하여 이메일 전송
                with smtplib.SMTP(smtp_server, smtp_port) as server:
                    server.starttls()
                    server.login(sender_email, sender_password)
                    server.sendmail(sender_email, recipient_email, message.as_string())

                messagebox.showinfo("이메일 전송", "이메일을 성공적으로 전송했습니다.")
            except Exception as e:
                messagebox.showerror("이메일 전송 오류", f"이메일을 전송하는 중 오류가 발생했습니다: {e}")

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

    def bookmark(self, element):
        t = len(functions.bookmark_lists)
        functions.bookmark_lists.append(element)
        if t != len(functions.bookmark_lists):
            self.topParent.page3_instance.update_lb()
            messagebox.showinfo("북마크", element.find('culName').text+" 저장 완료!")


class DetailWindow_perform:
    def get_detail(self, element):
        val = element.find('seq').text
        r_value = get_detail(val)
        print(r_value)
        if r_value:
            webbrowser.open_new(r_value)
        else:
            messagebox.showerror("사이트", "사이트 정보 없음!")

    def update_animation(self):
        if self.running:
            try:
                # 현재 프레임 인덱스를 업데이트하고 버튼 이미지를 설정합니다
                self.frame_index = (self.frame_index + 1) % len(self.frames)
                self.my_button.configure(image=self.frames[self.frame_index])
                self.root.after(100, self.update_animation)  # 필요에 따라 지연 시간을 조정합니다
            except:
                self.on_closing()

    def on_closing(self):
        self.running = False  # 애니메이션 루프 플래그 비활성화

    def __init__(self, parentFrame, parent, title, element):
        self.topParent = parent
        self.window = Toplevel(parentFrame)
        self.window.title(title)
        self.window.geometry("400x400")

        self.element = element
        self.root = parentFrame
        self.setup_ui()

    def setup_ui(self):
        # 상세 정보를 출력할 프레임 생성
        self.label_frame = Frame(self.window)
        self.label_frame.grid(row=0, column=0, padx=10, pady=10, sticky='w', columnspan=2)

        map_frame = Frame(self.window)
        map_frame.grid(row=1, column=0, padx=10, pady=10, sticky='w')

        button_frame = Frame(self.window)
        button_frame.grid(row=1, column=1, padx=10, pady=10, sticky='w')

        name_label = Label(self.label_frame, text="Name: " + self.element.find('title').text)
        name_label.grid(row=0, sticky='w')

        tel_label = Label(self.label_frame, text="Period: " + self.element.find('startDate').text+ " - "+self.element.find('endDate').text)
        tel_label.grid(row=1, sticky='w')

        url_label = Label(self.label_frame, text="URL: click!", cursor="hand2", wraplength=300, justify="left")
        url_label.grid(row=2, sticky='w')
        url_label.bind("<Button-1>", lambda e: self.get_detail(self.element))

        gps_label = Label(self.label_frame,
                          text="Place: " + self.element.find('place').text)
        gps_label.grid(row=3, sticky='w')

        # 좌표정보가 있는 경우
        if self.element.find('gpsX').text is not None and self.element.find('gpsY').text is not None:
            gps_x = float(self.element.find('gpsX').text)
            gps_y = float(self.element.find('gpsY').text)

            map_widget = TkinterMapView(map_frame, width=250, height=250, corner_radius=0)
            map_widget.set_position(gps_y, gps_x)
            map_widget.set_marker(gps_y, gps_x, text=self.element.find('title').text)
            map_widget.pack(fill="both", expand=True)

        else:
            # Thumbnail 이미지 표시
            thumbnail_url = self.element.find('thumbnail').text
            if thumbnail_url:
                try:
                    response = requests.get(thumbnail_url)
                    image_data = response.content
                    image = Image.open(BytesIO(image_data))
                    image.thumbnail((250, 250))
                    photo = ImageTk.PhotoImage(image)

                    # 이미지를 띄울 라벨 생성
                    label = Label(map_frame, image=photo)
                    label.image = photo  # 이미지가 GC에 의해 삭제되지 않도록 참조를 유지합니다.
                    label.pack()
                except:
                    photo = ImageTk.PhotoImage(file='resources/no_image.png')

                    # 이미지를 띄울 라벨 생성
                    label = Label(map_frame, image=photo)
                    label.image = photo  # 이미지가 GC에 의해 삭제되지 않도록 참조를 유지합니다.
                    label.pack()

        b = Button(button_frame, text="북마크", command=lambda: self.bookmark(self.element), width=8, height=2)
        b.grid(row=0, column=0, padx=10, pady=10)
        b = Button(button_frame, text="이메일", command=self.email, width=8, height=2)
        b.grid(row=1, column=0, padx=10, pady=10)
        b = Button(button_frame, text="파일", command=lambda: self.file(self.element), width=8, height=2)
        b.grid(row=2, column=0, padx=10, pady=10)
        self.frames = []
        for i in count():
            try:
                frame = PhotoImage(file="resources/bc.gif", format=f"gif -index {i}")
                resized_frame = frame.subsample(8, 8)  # 크기를 조정합니다
                self.frames.append(resized_frame)
            except Exception:
                break

        self.frame_index = 0
        self.my_button = Button(button_frame, text="",  image=self.frames[self.frame_index])
        self.my_button.grid(row=3, column=0, padx=10, pady=10)

        self.running = True  # 애니메이션 루프 플래그

        self.update_animation()

    def email(self):
        recipient_email = simpledialog.askstring("이메일 전송", "수신자의 이메일 주소를 입력하세요:")
        if recipient_email:
            try:
                # 이메일 전송을 위한 SMTP 서버 설정
                smtp_server = 'smtp.gmail.com'
                smtp_port = 587  # Gmail SMTP 포트 번호
                sender_email = 'elephant2297@tukorea.ac.kr'  # 보내는 사람의 이메일 주소
                sender_password = 'pxhe zyov urbc itoe'  # 보내는 사람의 이메일 비밀번호

                # 이메일 제목과 내용 작성
                subject = "문화 공연 정보"
                body = f"#문화 공연 정보#\n"
                body += f"이름: {self.element.find('title').text}\n"
                body += f"기간: {self.element.find('startDate').text + " - " + self.element.find('endDate').text}\n"
                body += f"장소: {self.element.find('place').text}\n"

                # MIME 메시지 생성
                message = MIMEMultipart()
                message['From'] = formataddr(('Sender', sender_email))
                message['To'] = recipient_email
                message['Subject'] = subject
                message.attach(MIMEText(body, 'plain'))

                # SMTP 서버에 연결하여 이메일 전송
                with smtplib.SMTP(smtp_server, smtp_port) as server:
                    server.starttls()
                    server.login(sender_email, sender_password)
                    server.sendmail(sender_email, recipient_email, message.as_string())

                messagebox.showinfo("이메일 전송", "이메일을 성공적으로 전송했습니다.")
            except Exception as e:
                messagebox.showerror("이메일 전송 오류", f"이메일을 전송하는 중 오류가 발생했습니다: {e}")


    def file(self, element):
        cul_name = element.find('title').text
        file_path = "datas/" + cul_name + ".txt"

        # 파일에 저장할 내용 작성
        file_content = ""
        cul_period = element.find('startDate').text + " - " + element.find('endDate').text
        cul_place = element.find('place').text
        file_content += f"Name: {cul_name}\n"
        file_content += f"Period: {cul_period}\n"
        file_content += f"Place: {cul_place}\n"

        print(file_content)

        # 파일에 내용 저장
        with open(file_path, 'w', encoding="utf-8") as file:
            file.write(file_content)

        messagebox.showinfo("저장", file_path + "에 저장됨!")


    def bookmark(self, element):
        t = len(functions.bookmark_lists)
        functions.bookmark_lists.append(element)
        if t != len(functions.bookmark_lists):
            self.topParent.page3_instance.update_lb()
            messagebox.showinfo("북마크", element.find('title').text+" 저장 완료!")