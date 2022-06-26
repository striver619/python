# 作者：        Eason
# 微信公众号：   优特编程
# 微信：        eason-link
# 网站：        https://www.xuepy.com

import os
import tkinter as tk


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("UTE.CC ")
        self.geometry("300x200")
        
        tk.Label(self, text="通过窗口执行程序", bd=1, relief=tk.SUNKEN, anchor=tk.W).pack(side=tk.BOTTOM, fill=tk.X)
        
        self.init_menu()
        
    def init_menu(self):
        self.menubar = tk.Menu(self)
        
        file_menu = tk.Menu(self.menubar, tearoff=0)
        file_menu.add_command(label="新建")
        file_menu.add_separator()
        file_menu.add_command(label="退出", command=lambda:self.quit())
        self.menubar.add_cascade(label="文件", menu=file_menu)

        file_app = tk.Menu(self.menubar, tearoff=0)
        # c:\links 快捷方式目录必须正确
        for lnk in os.listdir(r"c:\links"):
            file_app.add_command(label=lnk.removesuffix(" - 快捷方式.lnk"),     #使用python3.9以上
                                 command=lambda target=f"c:\\links\\{lnk}": os.startfile(target))
    
        self.menubar.add_cascade(label="程序", menu=file_app)
        
        self.config(menu=self.menubar)
        
if __name__ == "__main__":
    app = App()
    app.mainloop()
