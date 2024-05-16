import tkinter as tk
import webbrowser

def open_url():
    webbrowser.open_new(url_label.cget("text"))

root = tk.Tk()

# 클릭 가능한 URL 표시 레이블
url_label = tk.Label(root, text="https://www.example.com", fg="blue", cursor="hand2")
url_label.pack(padx=10, pady=10)

# URL 클릭 시 이벤트 바인딩
url_label.bind("<Button-1>", lambda e: open_url())

root.mainloop()
