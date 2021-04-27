import tkinter as tk
from PIL import Image,ImageTk
import util
import time
import random
from part3 import *

def P2init(window):
    # 正式题目的顺序随机
    util.shuffled_pic1 = [i for i in range(1, util.PIC_NUM+1)]
    random.shuffle(util.shuffled_pic1)
    if util.DEBUG:
        print('【DEBUG】打乱后图片的顺序为:')
        for each in util.shuffled_pic1:
            print(each, end=' ')
        print()
    # 测试题的位置随机
    util.test_ans = random.randint(0,1)  # 表示第二部分第一个测试题的答案为上（0）或下（1）
    util.test1_pos = random.randint(1, util.PIC_NUM//2 - 1)  # 在第test_pos题后插入测试题
    util.test2_pos = random.randint(util.PIC_NUM//2+1, util.PIC_NUM -1)
    if util.DEBUG:
        print('【DEBUG】第二部分插入的两道测试题的位置为第',end='')
        print(util.test1_pos,'和',util.test2_pos, end='')
        print('题的后面。（此处的编号表示图片的出现顺序而不是图片本身的id号码）\n其中第一道测试题标准答案为',end='')
        if util.test_ans == 0:
            print('上')
        else:
            print('下')
    dispP2inst(window)


# 打印第二部分的说明  
def dispP2inst(window):
    frame = tk.Frame(window)
    frame.pack()
    tk.Label(frame, text=util.TITLE_PREFIX+'理解测试结束'+util.TITLE_SUFFIX,
            font=('KaiTi', util.TITLE_FONT_SIZE)).pack()
    tk.Label(frame, text='恭喜您通过了对情境的理解测试。\n\
再次强调，选择无对错之分，但您的答案对我们非常重要，请按照实际情况认真填写。\n\
点击“确定”键开始正式实验',
            font=('KaiTi', util.TEXT_FONT_SIZE),justify= 'left').pack()
    def click():
        frame.destroy()
        dispP2prob(window, 1)
    tk.Button(frame, text="确定", command = click,font=('KaiTi', util.TEXT_FONT_SIZE)).pack()
    


def dispP2prob(window, counter):
    def pressKey(event):
        tmp = event.char
        if tmp == 'J' or tmp == 'j':
            tmp = '上'
        elif tmp == 'K' or tmp == 'k':
            tmp = '下'
        else:
            if util.DEBUG:
                print('【DEBUG】被试对象没有选择答案就提交，本题重新测试')
            return
        t2 = time.time()
        time_spent = str(format(t2-util.T1, '.3f'))
        if util.DEBUG:
            print('【DEBUG】被试对象选择的答案是:' + tmp + '，用时为' + time_spent + '秒')
        util.P2ANS.append((tmp, time_spent))
        frame.destroy()
        if counter == util.PIC_NUM:
            util.p2ans = dict({})
            for i in range(util.PIC_NUM):
                util.p2ans[str(util.shuffled_pic1[i])] = util.P2ANS[i]
            if util.DEBUG:
                print('【DEBUG】第二部分测试结束。测试结果为：')
            for each in util.p2ans.keys():
                print(each+':'+util.p2ans[each][0], end = ' ')
            print()
            dispP2end(window)
        else:
            if counter == util.test1_pos:
                P2TestProb(window,util.test_ans, counter+1)
            elif counter == util.test2_pos:
                P2TestProb(window,1-util.test_ans, counter+1)
            else:
                dispP2prob(window, counter+1)
    pic_id = util.shuffled_pic1[counter-1]
    if util.DEBUG:
        print('【DEBUG】现在是第二部分，正在展示编号为'+str(pic_id)+'的图片')
    frame = tk.Frame(window)
    frame.bind('<Key>', pressKey)
    frame.focus_set()
    frame.pack()
    tk.Label(frame, text=util.TITLE_PREFIX, font=('KaiTi', util.TITLE_FONT_SIZE)).pack()
    tk.Label(frame, text='如果两地区患病情况如下，您打算将医疗物资运往哪个地区？',
            font=('KaiTi', util.TEXT_FONT_SIZE),justify= 'left').pack()
    photo = Image.open("src\\"+str(pic_id)+".png")
    photo = photo.resize(util.PIC_SIZE) 
    util.PHOTO = ImageTk.PhotoImage(photo)
    imgLabel = tk.Label(frame,image=util.PHOTO).pack()
    tk.Label(frame, text='请做出您的选择',
            font=('KaiTi', util.TEXT_FONT_SIZE),justify= 'left').pack()
    util.T1 = time.time()

def dispP2end(window):
    frame = tk.Frame(window)
    frame.pack()
    tk.Label(frame, text=util.TITLE_PREFIX, font=('KaiTi', util.TITLE_FONT_SIZE)).pack()
    tk.Label(frame, text='第一部分结束，请联系主试（不要做任何按键反应）',
            font=('KaiTi', util.TEXT_FONT_SIZE),justify= 'left').pack()
    def click():
        frame.destroy()
        P3init(window)
    tk.Button(frame, text="主试请点击此处", command = click,font=('KaiTi', util.TEXT_FONT_SIZE)).pack()
    


def P2TestProb(window, true_ans, counter):
    def pressKey(event):
        tmp = event.char
        if tmp == 'J' or tmp == 'j':
            tmp = '上'
        elif tmp == 'K' or tmp == 'k':
            tmp = '下'
        else:
            if util.DEBUG:
                print('【DEBUG】被试对象没有选择答案就提交，本题重新测试')
            return
        if util.DEBUG:
            print('【DEBUG】被试对象选择的答案是:' + tmp)
        if tmp != true_ans:
            util.TEST_PASS = False
        frame.destroy()
        dispP2prob(window, counter)
    if true_ans == 0:
        true_ans = '上'
    else:
        true_ans = '下'
    if util.DEBUG:
        print('【DEBUG】正在展示测试题。本题的标准答案为：',true_ans)
    part = '二'
    frame = tk.Frame(window)
    frame.bind('<Key>', pressKey)
    frame.focus_set()
    frame.pack()
    tk.Label(frame, text=util.TITLE_PREFIX, font=('KaiTi', util.TITLE_FONT_SIZE)).pack()
    photo = Image.open("src\\0.png")
    photo = photo.resize(util.PIC_SIZE) 
    util.PHOTO = ImageTk.PhotoImage(photo)
    imgLabel = tk.Label(frame,image=util.PHOTO).pack()
    tk.Label(frame, text='本题请选择' + true_ans +'方地区',
            font=('KaiTi', util.TEXT_FONT_SIZE),justify= 'left').pack()


