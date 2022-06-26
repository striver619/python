import urllib.request
import tkinter as tk



class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("获取公网 IP")
        self.geometry("300x100")

        ip = urllib.request.urlopen("http://api.ipify.org").read().decode()
        self.lbl_ip = tk.Label(self, text=f"IP：{ip}", font=("微软雅黑", 20))
        self.lbl_ip.pack(expand=True)


if __name__ == "__main__":
    app = Application()
    app.mainloop()

