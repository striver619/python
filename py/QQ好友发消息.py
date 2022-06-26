from tkinter import *
import win32gui
import win32con
import win32clipboard as w
LOG_LINE_NUM = 0
class Play():
    def __init__(self, init_window_name):
        self.init_window_name = init_window_name
    def set_init_window(self):
        #构建框架
        self.init_window_name.title("qq消息发送器")
        self.init_window_name.geometry("723x250+10+10")
        self.init_window_name["bg"] = "HotPink"
        self.init_window_name.attributes("-alpha", 0.9)  # 虚化 值越小虚化程度越高
        # 标签
        self.init_data_label = Label(self.init_window_name, text="要发送消息者",fg="DeepSkyBlue", bg="FloralWhite")
        self.init_data_label.grid(row=0, column=1)
        self.name_data_label = Label(self.init_window_name, text="要发送内容",fg="DeepSkyBlue", bg="FloralWhite")
        self.name_data_label.grid(row=0, column=23)
        self.log_label = Label(self.init_window_name, text="@ 2020版权所有 ",fg="DeepSkyBlue", bg="FloralWhite")
        self.log_label.grid(row=12, column=0)
        # 文本框
        self.init_data_Text = Text(self.init_window_name, width=43, height=15)  # 原始数据录入框
        self.init_data_Text.grid(row=1, column=0, rowspan=10, columnspan=10)
        self.log_data_Text = Text(self.init_window_name, width=43, height=15)  # 日志框
        self.log_data_Text.grid(row=2, column=18, columnspan=10)
        # 滚动条
        self.result_data_scrollbar_y = Scrollbar(self.init_window_name)
        self.result_data_scrollbar_y.config(command=self.init_data_Text.yview)
        self.init_data_Text.config(yscrollcommand=self.result_data_scrollbar_y.set)
        self.result_data_scrollbar_y.grid(row=1, column=10, rowspan=10, sticky='NS')
        self.result_data_scrollbar_y = Scrollbar(self.init_window_name)
        self.result_data_scrollbar_y.config(command=self.log_data_Text.yview)
        self.log_data_Text.config(yscrollcommand=self.result_data_scrollbar_y.set)
        self.result_data_scrollbar_y.grid(row=1, column=33, rowspan=10, sticky='NS')
        # 按钮
        self.str_command = Button(self.init_window_name, text="发送3次", bg="Gold", width=10,command=self.Send)  # 调用内部方法  加()为直接调用
        self.str_command.grid(row=2, column=12)
    def Send(self):
        for i in range(0,3):
            a=self.init_data_Text.get(1.0, END).strip().replace("\n", "").encode()
            b = self.log_data_Text.get(1.0, END).strip().replace("\n", "").encode()
            receiver=str(a,encoding="utf-8")
            msg=str(b,encoding="utf-8")
###############################发送qq消息使用下面几行#########
            w.OpenClipboard()
            w.EmptyClipboard()
            w.SetClipboardData(win32con.CF_UNICODETEXT, msg)
            w.CloseClipboard()
            qq = win32gui.FindWindow(None, receiver)
            win32gui.SendMessage(qq, win32con.WM_PASTE, 0, 0)
            win32gui.SendMessage(qq, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
###############################done#########################
if __name__=="__main__":
    init_window = Tk()
    Play(init_window).set_init_window()
    init_window.mainloop()