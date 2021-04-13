import tkinter as tk
from PIL import Image,ImageTk

# 全局常量（在读入config.ini后不再改变，读入时进行变量赋值）
FILE_NAME = ""
PIC_NUM = 0
DEBUG = False
# 全局变量（用于控制不同模块间的交互）
FLAG = 1
P2ANS = []
P3ANS = []

def createWindow():
    window = tk.Tk()
    window.title('社会决策实验')
    # window.geometry('900x600')
    window.state('zoomed')
    return window

def initConfig():
    with open('config.ini','r') as f:
        for eachLine in f:
            status = eachLine.split('=')
            status[1] = status[1][:-1]
            if status[0] == "PIC_NUM":
                global PIC_NUM
                PIC_NUM = int(status[1])
            elif status[0] == "DEBUG" and status[1] == "T":
                global DEBUG
                DEBUG = True
