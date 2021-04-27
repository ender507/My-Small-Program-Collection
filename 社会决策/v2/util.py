import tkinter as tk
from PIL import Image,ImageTk
import random

# 全局常量（在读入config.ini后不再改变，读入时进行变量赋值）
PIC_NUM = 0
DEBUG = False
TITLE_FONT_SIZE = 0
TEXT_FONT_SIZE = 0
PIC_SIZE = (0,0)
TITLE_PREFIX = ""
TITLE_SUFFIX = ""
FAKE_RATE = []
# 全局变量（用于控制不同模块间的交互）
FILE_NAME = ""
FLAG = 1
P2ANS = []
P3ANS = []
TEST_PASS = True
PHOTO = None
KEY = None

p2ans = None
p3ans = None
shuffled_pic1 = None
shuffled_pic2 = None
choice_major_pic = None
test_ans = None 
test1_pos = None
test2_pos = None

def pressKey(event):
    print('pressed', event.char, type(event.char))

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
    global FAKE_RATE
    FAKE_RATE = [random.randint(10,40)/100 for i in range(PIC_NUM)]
        

# 输出实验结果
def writeAns(window):
    global TEST_PASS
    if TEST_PASS:
        pos = 'res\\'
    else:
        pos = 'hanpi\\'
    global FILE_NAME
    with open(pos+FILE_NAME, 'w') as f:
        # 第一轮
        f.write('第一轮\n')
        f.write('第一轮题号,')
        global shuffled_pic1
        global p2ans
        for i in shuffled_pic1:
            f.write(str(i)+',')
        f.write('\n')
        f.write('第一轮选择,')
        for i in shuffled_pic1:
            f.write(p2ans[str(i)][0]+',')
        f.write('\n')
        f.write('第一轮决策时间,')
        for i in shuffled_pic1:
            f.write(p2ans[str(i)][1]+',')
        f.write('\n\n')
        # 第二轮
        f.write('第二轮\n')
        f.write('第二轮题号,')
        global shuffled_pic2
        global p3ans
        for i in shuffled_pic2:
            f.write(str(i)+',')
        f.write('\n')
        f.write('第二轮选择,')
        for i in shuffled_pic2:
            f.write(p3ans[str(i)][0]+',')
        f.write('\n')
        f.write('第二轮决策时间,')
        for i in shuffled_pic1:
            f.write(p3ans[str(i)][1]+',')
        f.write('\n\n')
        # 额外信息
        global choice_major_pic
        f.write('大多数人的选择相同与否（顺序与第二轮对应）,')
        for i in shuffled_pic2:
            if i in choice_major_pic:
                f.write('1,')#相同为1
            else:
                f.write('0,')
        f.write('\n')
        f.write('是否改变,')
        for i in shuffled_pic2:
            if p3ans[str(i)][0] == p2ans[str(i)][0]:
                f.write('0,')#不改为0
            else:
                f.write('1,')
        dispFin(window)

# 打印结束部分
def dispFin(window):
    # frame = tk.Frame(window)
    global TITLE_PREFIX, TITLE_SUFFIX, TITLE_FONT_SIZE, TEXT_FONT_SIZE
    tk.Label(window, text=TITLE_PREFIX+'第三部分结束'+TITLE_SUFFIX,
            font=('KaiTi', TITLE_FONT_SIZE)).pack()
    tk.Label(window, text='\n你完成了全部的测试。感谢你的参与。\n\n',
            font=('KaiTi', TEXT_FONT_SIZE),justify= 'left').pack()
    def click():
        window.destroy()
    tk.Button(window, text="确定", command = window.destroy, font=('KaiTi', TEXT_FONT_SIZE)).pack()
    
    
# config.ini样例：
# PIC_NUM=4
# DEBUG=T
# TITLE_FONT_SIZE=30
# TEXT_FONT_SIZE=15
# PIC_SIZE=500,170
# TITLE_PREFIX_EMPTY_LINE_NUM=2
# TITLE_SUFFIX_EMPTY_LINE_NUM=1
