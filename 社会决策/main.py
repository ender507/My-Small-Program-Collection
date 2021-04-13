import tkinter as tk
from PIL import Image,ImageTk
import random
import util
from part1 import *
from part2 import *
from part3 import *

# 打印初始画面并获取被试者信息，返回输出结果表单的文件名
def dispWelcome(window):
    # 欢迎标题
    tk.Label(window, text='欢迎参加本实验！',
            font=('Arial', 30), width=30, height=5).pack()    # 输入相关信息
    tk.Label(window, text="请输入被试编号:", font=('Arial', 20)).pack()
    test_id = tk.StringVar()
    ipt1 = tk.Entry(window, textvariable = test_id)
    test_id.set("")
    ipt1.pack()
    tk.Label(window, text="请输入您的年龄（填写数字即可）:", font=('Arial', 20)).pack()
    age = tk.StringVar()
    ipt2 = tk.Entry(window, textvariable = age)
    age.set("")
    ipt2.pack()
    tk.Label(window, text="请输入您的性别（填写男或女）:", font=('Arial', 20)).pack()
    gender = tk.StringVar()
    ipt3 = tk.Entry(window, textvariable = gender)
    gender.set("")
    ipt3.pack()
    # 确定按钮
    def clickWelcome():
        tid = test_id.get()
        gen = gender.get()
        ag = age.get()
        file_name = str("%s_%s_%s.csv" %(tid, ag, gen))
        util.FILE_NAME = file_name.replace(" ","")
        window.destroy()
    tk.Button(window, text="确定", command = clickWelcome, font=('Arial', 10)).pack()

# 打印说明部分   
def dispInst(window):
    l = tk.Label(window, text='实验说明',
            font=('Arial', 30), width=30, height=5).pack()
    l2 = tk.Label(window, text='该实验共分为三个部分\n\
第一部分为测试，全部正确后，即可进入后面的部分\n\
第二部分和第三部分为正式部分\n\
请您仔细作答\n\n\n点击按钮后即可进入第一部分',
            font=('Arial', 20)).pack()
    tk.Button(window, text="确定", command = window.destroy, font=('Arial', 10)).pack()

# 打印结束部分
def dispFin():
    window = util.createWindow()
    tk.Label(window, text='\n\n\n第三部分结束',
            font=('Arial', 30)).pack()
    tk.Label(window, text='\n你完成了全部的测试。感谢你的参与。\n\n',
            font=('Arial', 15),justify= 'left').pack()
    def click():
        window.destroy()
    tk.Button(window, text="确定", command = window.destroy).pack()
    window.mainloop()

# 输出实验结果
def writeAns(p2ans, p3ans, shuffled_pic1, shuffled_pic2, choice_major_pic):
    with open('res\\'+util.FILE_NAME, 'w') as f:
        f.write(',')
        for i in range(util.PIC_NUM):
            f.write('第'+str(i+1)+'题,')
        f.write('\n一,')
        for i in shuffled_pic1:
            f.write(str(i)+',')
        f.write('\n,')
        for i in shuffled_pic1:
            f.write(p2ans[str(i)]+',')
        f.write('\n二,')
        for i in shuffled_pic2:
            f.write(str(i)+',')
        f.write('\n,')
        for i in shuffled_pic2:
            f.write(p3ans[str(i)]+',')
        f.write('\n所挑选多数人选择和被试选择相同的题号,')
        for i in range(1, 1+util.PIC_NUM):
            if i in choice_major_pic:
                f.write(str(i)+',')
        f.write('\n所挑选多数人选择和被试选择不同的题号,')
        for i in range(1, 1+util.PIC_NUM):
            if i not in choice_major_pic:
                f.write(str(i)+',')
        f.write('\n')

if __name__ == '__main__':
    util.initConfig()
    #dispP2inst()
    #exit()
    # 欢迎页面
    window = util.createWindow()
    dispWelcome(window)
    window.mainloop()
    if util.DEBUG:
        print('【DEBUG】依据被试对象的信息，输出的表格命名为：' + util.FILE_NAME)
    # 说明部分
    window = util.createWindow()
    dispInst(window)
    window.mainloop()
    # 第一部分
    while util.FLAG != -1:
        if util.FLAG == 1:
            if util.DEBUG:
                print('【DEBUG】被试对象查看题目说明')
            dispP1_1()
        elif util.FLAG == 2:
            if util.DEBUG:
                print('【DEBUG】被试对象开始做测试题')
            dispP1_2()
        elif util.FLAG == 3:
            dispP1_3()
            if util.DEBUG:
                print('【DEBUG】被试对象测试不通过')
            exit()
    if util.DEBUG:
        print('【DEBUG】被试对象测试通过')
    # 第二部分
    shuffled_pic = [i for i in range(1, util.PIC_NUM+1)]
    random.shuffle(shuffled_pic)
    if util.DEBUG:
        print('【DEBUG】打乱后图片的顺序为:')
        for each in shuffled_pic:
            print(each, end=' ')
        print()
    dispP2inst()
    for each in shuffled_pic:
        dispP2prob(each)
    p2ans = dict({})
    for i in range(util.PIC_NUM):
        p2ans[str(shuffled_pic[i])] = util.P2ANS[i]
    if util.DEBUG:
        print('【DEBUG】第二部分测试结束。测试结果为：')
        for each in p2ans.keys():
            print(each+':'+p2ans[each], end = ' ')
        print()
    # 第三部分
    shuffled_pic2 = [i for i in range(1, util.PIC_NUM+1)]   
    choice_major_pic = random.sample(shuffled_pic2, util.PIC_NUM//2) # 随机选择一半，被试者选择的选项为“大多数”
    random.shuffle(shuffled_pic2) # 第三部分题目按照新的顺序出现
    if util.DEBUG:
        print('【DEBUG】被试者选择的选项被当做“大多数人的选择”的图片编号为：')
        for each in choice_major_pic:
            print(each, end=' ')
        print()
        print('【DEBUG】打乱后图片的顺序为:')
        for each in shuffled_pic2:
            print(each, end=' ')
        print()
    dispP3inst()
    for each in shuffled_pic2:
        up_is_major = False
        # 如果之前选了上，且该题在choice_major_pic中
        if p2ans[str(each)]=='上' and (each in choice_major_pic):
            up_is_major = True
        # 如果之前选了下，且该题不在choice_major_pic
        if p2ans[str(each)]=='下' and (each not in choice_major_pic):
            up_is_major = True
        dispP3prob(each, up_is_major)
    p3ans = dict({})
    for i in range(util.PIC_NUM):
        p3ans[str(shuffled_pic2[i])] = util.P3ANS[i]
    if util.DEBUG:
        print('【DEBUG】第三部分测试结束。测试结果为：')
        for each in p3ans.keys():
            print(each+':'+p3ans[each], end = ' ')
        print()
    writeAns(p2ans, p3ans, shuffled_pic, shuffled_pic2, choice_major_pic)
    dispFin()
