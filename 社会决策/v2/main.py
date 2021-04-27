import tkinter as tk
import util
from part1 import *


# 打印初始画面并获取被试者信息，返回输出结果表单的文件名
def dispWelcome(window):
    # 欢迎标题
    frame = tk.Frame(window)
    frame.pack()
    if util.DEBUG:
        tk.Label(frame, text=util.TITLE_PREFIX+'警告：程序正在以【DEBUG】模式运行，如果您正在进行正式实验，请联系主试进行调整'+util.TITLE_SUFFIX,
             font=('KaiTi', util.TITLE_FONT_SIZE)).pack()
    tk.Label(frame, text=util.TITLE_PREFIX+'欢迎参加本实验！'+util.TITLE_SUFFIX,
             font=('KaiTi', util.TITLE_FONT_SIZE)).pack()
    tk.Label(frame, text="请输入被试编号:", font=('KaiTi', util.TEXT_FONT_SIZE)).pack()
    test_id = tk.StringVar()
    ipt1 = tk.Entry(frame, textvariable = test_id, font=('KaiTi', util.TEXT_FONT_SIZE+10))
    test_id.set("")
    ipt1.pack()
    tk.Label(frame, text="请输入您的年龄（填写数字即可）:", font=('KaiTi',util.TEXT_FONT_SIZE)).pack()
    age = tk.StringVar()
    ipt2 = tk.Entry(frame, textvariable = age, font=('KaiTi', util.TEXT_FONT_SIZE+10))
    age.set("")
    ipt2.pack()
    tk.Label(frame, text="请输入您的性别（填写男或女）:", font=('KaiTi',util.TEXT_FONT_SIZE)).pack()
    gender = tk.StringVar()
    ipt3 = tk.Entry(frame, textvariable = gender, font=('KaiTi', util.TEXT_FONT_SIZE+10))
    gender.set("")
    ipt3.pack()
    # 确定按钮
    def clickWelcome():
        tid = test_id.get()
        gen = gender.get()
        ag = age.get()
        file_name = str("%s_%s_%s.csv" %(tid, ag, gen))
        util.FILE_NAME = file_name.replace(" ","")
        if util.DEBUG:
            print('【DEBUG】依据被试对象的信息，输出的表格命名为：' + util.FILE_NAME)
        frame.destroy()
        dispInst(window)
    tk.Button(frame, text="确定", command = clickWelcome, font=('KaiTi', util.TEXT_FONT_SIZE)).pack()

# 打印说明部分   
def dispInst(window):
    frame = tk.Frame(window)
    frame.pack()
    l = tk.Label(frame, text=util.TITLE_PREFIX+'指导语'+util.TITLE_SUFFIX,
            font=('KaiTi', util.TITLE_FONT_SIZE)).pack()
    l2 = tk.Label(frame, text='欢迎参与实验，本实验为个人决策情境，\n\
请仔细阅读实验情境并在确保理解的前提下，进行正式实验。\n\n\
您的选择对我们非常重要，决策无对错之分，请按照实际情况认真选择。\n\n\
点击“确认”后进入实验情境',
            font=('KaiTi', util.TEXT_FONT_SIZE)).pack()
    def click():
        frame.destroy()
        P1windowControl(window)
    tk.Button(frame, text="确定", command = click, font=('KaiTi', util.TEXT_FONT_SIZE)).pack()
    
       

if __name__ == '__main__':
    util.initConfig()
    # 创建窗口
    window = tk.Tk()
    # window.attributes('-fullscreen', True)
    window.title('社会决策实验')
    window.state('zoomed')
    dispWelcome(window) 
    window.mainloop()
    
