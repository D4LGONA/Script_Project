import tkinter as tk



class SampleApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title("탭 예제")

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

        self.pages = []
        for i in range(1, 6):
            page = tk.Frame(self.notebook)
            self.notebook.add(page, text=f"탭 {i}")
            label = tk.Label(page, text=f"이것은 {i}번째 탭입니다", font=("Helvetica", 18))
            label.pack(pady=10, padx=10)

            self.pages.append(page)


app = SampleApp()
app.mainloop()
