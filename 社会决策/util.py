import tkinter as tk
from PIL import Image,ImageTk

# 全局常量（在读入config.ini后不再改变，读入时进行变量赋值）
PIC_NUM = 0
DEBUG = False
TITLE_FONT_SIZE = 0
TEXT_FONT_SIZE = 0
PIC_SIZE = (0,0)
TITLE_PREFIX = ""
TITLE_SUFFIX = ""
# 全局变量（用于控制不同模块间的交互）
FILE_NAME = ""
FLAG = 1
P2ANS = []
P3ANS = []
TEST_PASS = True

def createWindow():
    window = tk.Tk()
    window.title('社会决策实验')
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
            elif status[0] == "TITLE_FONT_SIZE":
                global TITLE_FONT_SIZE
                TITLE_FONT_SIZE = int(status[1])
            elif status[0] == "TEXT_FONT_SIZE":
                global TEXT_FONT_SIZE
                TEXT_FONT_SIZE = int(status[1])
            elif status[0] == "PIC_SIZE":
                pic_size = status[1].split(',')
                global PIC_SIZE
                PIC_SIZE = (int(pic_size[0]),int(pic_size[1]))
            elif status[0] == "TITLE_PREFIX_EMPTY_LINE_NUM":
                global TITLE_PREFIX
                for i in range(int(status[1])):
                    TITLE_PREFIX += '\n'
            elif status[0] == "TITLE_SUFFIX_EMPTY_LINE_NUM":
                global TITLE_SUFFIX
                for i in range(int(status[1])):
                    TITLE_SUFFIX += '\n' 

def testProb(part, true_ans):
    if true_ans == 0:
        true_ans = '上'
    else:
        true_ans = '下'
    global DEBUG
    if DEBUG:
        print('【DEBUG】正在展示测试题。本题的标准答案为：',true_ans)
    if part == 2:
        part = '二'
    else:
        part = '三'
    window = createWindow()
    tk.Label(window, text=TITLE_PREFIX+'第'+part+'部分'+TITLE_SUFFIX,
            font=('Arial', TITLE_FONT_SIZE)).pack()
    photo = Image.open("src\\test.png")
    photo = photo.resize(PIC_SIZE) 
    photo = ImageTk.PhotoImage(photo)
    imgLabel = tk.Label(window,image=photo).pack()
    tk.Label(window, text='本题请选择' + true_ans +'方地区',
            font=('Arial', TEXT_FONT_SIZE),justify= 'left').pack()
    ans = tk.StringVar()
    tk.Radiobutton(window, text='上方地区',variable=ans, value='上',font=('Arial', TEXT_FONT_SIZE)).pack()
    tk.Radiobutton(window, text='下方地区',variable=ans, value='下',font=('Arial', TEXT_FONT_SIZE)).pack()
    def click():
        global DEBUG
        tmp = ans.get()
        if tmp == "":
            if DEBUG:
                print('【DEBUG】被试对象没有选择答案就提交，本题重新测试')
            return
        if DEBUG:
            print('【DEBUG】被试对象选择的答案是:' + tmp)
        if tmp != true_ans:
            global TEST_PASS
            TEST_PASS = False
        window.destroy()
    tk.Button(window, text="确定", command = click,font=('Arial', TEXT_FONT_SIZE)).pack()
    window.mainloop()

# 测试失败
def testFail():
    global DEBUG
    if DEBUG:
        print('【DEBUG】被试对象测试不通过')
    window = createWindow()
    tk.Label(window, text=TITLE_PREFIX+'很抱歉，你没能通过测试'+TITLE_SUFFIX,
             font=('Arial', TITLE_FONT_SIZE)).pack()
    tk.Button(window, text="确定", command = window.destroy).pack()
    window.mainloop()
# config.ini样例：
# PIC_NUM=4
# DEBUG=T
# TITLE_FONT_SIZE=30
# TEXT_FONT_SIZE=15
# PIC_SIZE=500,170
# TITLE_PREFIX_EMPTY_LINE_NUM=2
# TITLE_SUFFIX_EMPTY_LINE_NUM=1
