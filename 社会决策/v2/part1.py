import tkinter as tk
from PIL import Image,ImageTk
import util
from part2 import *

def P1windowControl(window):
    # 第一部分
    if util.FLAG != -1:
        if util.FLAG == 1:
            if util.DEBUG:
                print('【DEBUG】被试对象查看题目说明')
            dispP1inst(window)
        elif util.FLAG == 2:
            if util.DEBUG:
                print('【DEBUG】被试对象开始做测试题')
            dispP1prob(window)
        elif util.FLAG == 3:
            if util.DEBUG:
                print('【DEBUG】被试对象第一部分测试题不通过，即将返回说明部分')
            testFailP1(window)
    if util.FLAG == -1:
        if util.DEBUG:
            print('【DEBUG】被试对象测试通过')
        P2init(window)

    
# 打印第一部分的说明  
def dispP1inst(window):
    frame = tk.Frame(window)
    frame.pack()
    def click():
        util.FLAG = 2
        frame.destroy()
        P1windowControl(window)
    if util.DEBUG:
        tk.Button(frame, text="【DEBUG】防止按不到的确定按钮", command = click).pack()
    tk.Label(frame, text=util.TITLE_PREFIX+'请仔细阅读以下情境'+util.TITLE_SUFFIX,
            font=('KaiTi', util.TITLE_FONT_SIZE)).pack()
    tk.Label(frame, text='某两个城镇突发传染性疾病，医疗物资紧缺。疫情发生后，民间慈善组织自发筹募了一批医疗物资。\n\
但是物资只够供给给其中一个。在分配资源时尚不清楚两个地区病人的情况，因此医疗物资将被随机分配。\n\
假如您现在知道每个区域的病人状况，如下图所示。\n\
您可以改变物资送往的区域，请问您会如何选择。',
            font=('KaiTi', util.TEXT_FONT_SIZE)).pack()
    photo = Image.open("src\\sample.png")
    photo = photo.resize(util.PIC_SIZE) 
    util.PHOTO = ImageTk.PhotoImage(photo)
    imgLabel = tk.Label(frame,image=util.PHOTO).pack()
    tk.Label(frame, text='物资小车的位置标示物资被随机分配送往的区域，如图示例，物资随机送往了处于下方的区域。\n\n\
每一行的小人个数表示该地区的患病人数，如图，上方的患病人数为2人，下方地区的患病人数为5人。\n\n\
小人身上的数字代表个体病情的严重程度，由临床医生评出（1-9评分，1为轻度，9为重度）。\n\
如图，上方地区的患者病情严重程度分别为8、9；下方地区的患者的病情严重程度分别为4、5、5、6、6；\n\n\
总值为该区域病情严重程度的总和，在图中通过条形图表现。\n\
如图中，下方地区的总值大于上方地区的（下方地区的总值条形图更长）；\n\
平均值=总值除以人数，表示人均的病情严重程度。\n\
如图中，下方地区的均值(5.2)小于上方地区的(8.5)（下方的均值条形图更短）。\n\n\
已了解整个情境并明白图片信息后，请点击确认。',
            font=('KaiTi', util.TEXT_FONT_SIZE)).pack()
    tk.Button(frame, text="确定", command = click, font=('KaiTi', util.TEXT_FONT_SIZE)).pack()
    

# 打印第一部分的测试题 
def dispP1prob(window):
    frame = tk.Frame(window)
    frame.pack()
    def click3():
        util.FLAG = -1
        frame.destroy()
        P1windowControl(window)
    if util.DEBUG:
        tk.Button(frame, text="【DEBUG】跳过测试", command = click3).pack()
    tk.Label(frame, text=util.TITLE_PREFIX+'测试题'+util.TITLE_SUFFIX,font=('KaiTi', util.TITLE_FONT_SIZE)).pack()
    tk.Label(frame, text='请依据图片完成下面的测试题：',font=('KaiTi', util.TEXT_FONT_SIZE)).pack()
    photo = Image.open("src\\test.png")
    photo = photo.resize(util.PIC_SIZE) 
    util.PHOTO = ImageTk.PhotoImage(photo)
    imgLabel = tk.Label(frame,image=util.PHOTO).pack()
    ans = [tk.StringVar()for i in range(5)]
    tk.Label(frame, text='1. 如果不作出改变，物资将送往哪个地区？',font=('KaiTi', util.TEXT_FONT_SIZE)).pack()
    tk.Radiobutton(frame, text='上方地区',variable=ans[0], value='A',font=('KaiTi', util.TEXT_FONT_SIZE-2)).pack()
    tk.Radiobutton(frame, text='下方地区',variable=ans[0], value='B',font=('KaiTi', util.TEXT_FONT_SIZE-2)).pack()
    tk.Label(frame, text='2. 小人的个数表示？',font=('KaiTi', util.TEXT_FONT_SIZE)).pack()
    tk.Radiobutton(frame, text='该地的人口密度',variable=ans[1], value='A',font=('KaiTi', util.TEXT_FONT_SIZE-2)).pack()
    tk.Radiobutton(frame, text='患病人数',variable=ans[1], value='B',font=('KaiTi', util.TEXT_FONT_SIZE-2)).pack()
    tk.Label(frame, text='3. 小人身上的红色数字代表？',font=('KaiTi', util.TEXT_FONT_SIZE)).pack()
    tk.Radiobutton(frame, text='该个体患病的严重程度',variable=ans[2], value='A',font=('KaiTi', util.TEXT_FONT_SIZE-2)).pack()
    tk.Radiobutton(frame, text='该个体的治愈概率',variable=ans[2], value='B',font=('KaiTi', util.TEXT_FONT_SIZE-2)).pack()
    tk.Label(frame, text='4. 就平均值（红色条形图）而言，哪个地区的更大？',font=('KaiTi', util.TEXT_FONT_SIZE)).pack()
    tk.Radiobutton(frame, text='上方地区',variable=ans[3], value='A',font=('KaiTi', util.TEXT_FONT_SIZE-2)).pack()
    tk.Radiobutton(frame, text='下方地区',variable=ans[3], value='B',font=('KaiTi', util.TEXT_FONT_SIZE-2)).pack()
    tk.Label(frame, text='5. 就病情总值（红色条形图）而言，哪个地区的更大？',font=('KaiTi', util.TEXT_FONT_SIZE)).pack()
    tk.Radiobutton(frame, text='上方地区',variable=ans[4], value='A',font=('KaiTi', util.TEXT_FONT_SIZE-2)).pack()
    tk.Radiobutton(frame, text='下方地区',variable=ans[4], value='B',font=('KaiTi', util.TEXT_FONT_SIZE-2)).pack()
    # 最后的按钮
    def click1():
        util.FLAG = 1
        frame.destroy()
        P1windowControl(window)
    def click2():
        util.FLAG = 3
        if ans[0].get() == 'B' and ans[1].get() == 'B' and ans[2].get() == 'A'\
           and ans[3].get() == 'A' and ans[4].get() == 'B' :
            util.FLAG = -1
        frame.destroy()
        P1windowControl(window)
    tk.Button(frame, text="返回查看说明", command = click1, font=('KaiTi', util.TEXT_FONT_SIZE-8)).pack()
    tk.Button(frame, text="提交", command = click2, font=('KaiTi', util.TEXT_FONT_SIZE)).pack()

    
# 第一部分测试不通过
def testFailP1(window):
    frame = tk.Frame(window)
    frame.pack()
    tk.Label(frame, text=util.TITLE_PREFIX+'很抱歉，你没能通过测试'+util.TITLE_SUFFIX,
             font=('KaiTi', util.TITLE_FONT_SIZE)).pack()
    tk.Label(frame, text='请确保完全读懂题意后再进行测试',font=('KaiTi', util.TEXT_FONT_SIZE)).pack()
    def click():
        util.FLAG = 1
        frame.destroy()
        P1windowControl(window)
    tk.Button(frame, text="确定", command=click).pack()
    
