import tkinter as tk
from PIL import Image,ImageTk
import util

# 打印第一部分的说明  
def dispP1_1():
    window = util.createWindow()
    def click():
        util.FLAG = 2
        window.destroy()
    if util.DEBUG:
        tk.Button(window, text="【DEBUG】防止按不到的确定按钮", command = click).pack()
    tk.Label(window, text=util.TITLE_PREFIX+'题目说明'+util.TITLE_SUFFIX,
            font=('Arial', util.TITLE_FONT_SIZE)).pack()
    tk.Label(window, text='请仔细阅读以下情形：\n\
    某两个城镇突发传染性疾病，医疗物资紧缺。疫情发生后，民间慈善组织自发\n\
筹募了一批医疗物资。但是物资只够供给给其中一个。在分配资源时尚不清楚\n\
两个地区病人的情况，因此医疗物资将被随机分配。假如您现在知道每个区域\n\
的病人状况，如下图所示。您可以改变物资送往的区域，请问您会如何选择。',
            font=('Arial', util.TEXT_FONT_SIZE),justify= 'left').pack()
    photo = Image.open("src\\sample.png")
    photo = photo.resize(util.PIC_SIZE) 
    photo = ImageTk.PhotoImage(photo)
    imgLabel = tk.Label(window,image=photo).pack()
    tk.Label(window, text='物资小车的位置标示物资被随机分配送往的区域，\n\
如图示例，物资随机送往了处于下方的区域。\n\n\
每一行的小人个数表示该地区的患病人数，如图，上方的患病人数为2人，下方地\n\
区的患病人数为5人。\n\n\
小人身上的数字代表个体病情的严重程度，由临床医生评出（1-9评分，1为轻度，\n\
9为重度）。如图，上方地区的患者病情严重程度分别为8、9；下方地区的患者\n\
的病情严重程度分别为4、5、5、6、6；\n\n\
总值为该区域病情严重程度的总和，在图中通过条形图表现。如图中，下方地区的总\n\
值大于上方地区的（下方地区的总值条形图更长）；\n\
平均值=总值除以人数，表示人均的病情严重程度。如图中，下方地区的均值(5.2)\n\
小于上方地区的(8.5)（下方的均值条形图更短）。\n\n\
已了解整个情境并明白图片信息后，请点击确认。',
            font=('Arial', util.TEXT_FONT_SIZE),justify= 'left').pack()
    tk.Button(window, text="确定", command = click).pack()
    window.mainloop()

# 打印第一部分的测试题 
def dispP1_2():
    window = util.createWindow()
    def click3():
        util.FLAG = -1
        window.destroy()
    if util.DEBUG:
        tk.Button(window, text="【DEBUG】跳过测试", command = click3).pack()
    tk.Label(window, text=util.TITLE_PREFIX+'测试题'+util.TITLE_SUFFIX,font=('Arial', util.TITLE_FONT_SIZE)).pack()
    tk.Label(window, text='请依据图片完成下面的测试题：',font=('Arial', util.TEXT_FONT_SIZE)).pack()
    photo = Image.open("src\\test.png")
    photo = photo.resize(util.PIC_SIZE) 
    photo = ImageTk.PhotoImage(photo)
    imgLabel = tk.Label(window,image=photo).pack()
    ans = [tk.StringVar()for i in range(5)]
    tk.Label(window, text='1. 如果不作出改变，物资将送往哪个地区？',font=('Arial', util.TEXT_FONT_SIZE)).pack()
    tk.Radiobutton(window, text='上方地区',variable=ans[0], value='A').pack()
    tk.Radiobutton(window, text='下方地区',variable=ans[0], value='B').pack()
    tk.Label(window, text='2. 小人的个数表示？',font=('Arial', util.TEXT_FONT_SIZE)).pack()
    tk.Radiobutton(window, text='该地的人口密度',variable=ans[1], value='A').pack()
    tk.Radiobutton(window, text='患病人数',variable=ans[1], value='B').pack()
    tk.Label(window, text='3. 小人身上的红色数字代表？',font=('Arial', util.TEXT_FONT_SIZE)).pack()
    tk.Radiobutton(window, text='该个体患病的严重程度',variable=ans[2], value='A').pack()
    tk.Radiobutton(window, text='该个体的治愈概率',variable=ans[2], value='B').pack()
    tk.Label(window, text='4. 就平均值（红色条形图）而言，哪个地区的更大？',font=('Arial', util.TEXT_FONT_SIZE)).pack()
    tk.Radiobutton(window, text='上方地区',variable=ans[3], value='A').pack()
    tk.Radiobutton(window, text='下方地区',variable=ans[3], value='B').pack()
    tk.Label(window, text='5. 就病情总值（红色条形图）而言，哪个地区的更大？',font=('Arial', util.TEXT_FONT_SIZE)).pack()
    tk.Radiobutton(window, text='上方地区',variable=ans[4], value='A').pack()
    tk.Radiobutton(window, text='下方地区',variable=ans[4], value='B').pack()
    # 最后的按钮
    def click1():
        util.FLAG = 1
        window.destroy()
    def click2():
        util.FLAG = 3
        if ans[0].get() == 'B' and ans[1].get() == 'B' and ans[2].get() == 'A'\
           and ans[3].get() == 'A' and ans[4].get() == 'B' :
            util.FLAG = -1
        window.destroy()
    tk.Button(window, text="返回查看说明", command = click1).pack()
    tk.Button(window, text="提交", command = click2).pack()
    window.mainloop()
    

