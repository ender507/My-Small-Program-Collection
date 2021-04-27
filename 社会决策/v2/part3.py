import tkinter as tk
from PIL import Image,ImageTk
import util
import time
import random

def P3init(window):
    util.shuffled_pic2 = [i for i in range(1, util.PIC_NUM+1)]
    util.choice_major_pic = random.sample(util.shuffled_pic2, util.PIC_NUM//2) # 随机选择一半，被试者选择的选项为“大多数”
    random.shuffle(util.shuffled_pic2) # 第三部分题目按照新的顺序出现
    if util.DEBUG:
        print('【DEBUG】被试者选择的选项被当做“大多数人的选择”的图片编号为：')
        for each in util.choice_major_pic:
            print(each, end=' ')
        print()
        print('【DEBUG】打乱后图片的顺序为:')
        for each in util.shuffled_pic2:
            print(each, end=' ')
        print()
    # 测试题的位置随机
    util.test_ans = random.randint(0,1)  # 表示第三部分第一个测试题的答案为上（0）或下（1）
    util.test1_pos = random.randint(1, util.PIC_NUM//2 - 1)  # 在第test_pos题后插入测试题
    util.test2_pos = random.randint(util.PIC_NUM//2 + 1, util.PIC_NUM - 1)
    if util.DEBUG:
        print('【DEBUG】第三部分插入的两道测试题的位置为第',end='')
        print(util.test1_pos,'和',util.test2_pos, end='')
        print('题的后面。（此处的编号表示图片的出现顺序而不是图片本身的id号码）\n其中第一道测试题标准答案为',end='')
        if util.test_ans == 0:
            print('上')
        else:
            print('下')
    util.FLAG = 1
    P3windowControl(window)


def P3windowControl(window):
    if util.FLAG != -1:
        if util.FLAG == 1:
            if util.DEBUG:
                print('【DEBUG】被试对象查看第三部分题目说明')
            dispP3inst(window)
        elif util.FLAG == 2:
            if util.DEBUG:
                print('【DEBUG】被试对象开始做测试题')
            dispP3test(window)
        elif util.FLAG == 3:
            if util.DEBUG:
                print('【DEBUG】被试对象第三部分测试题不通过，即将返回说明部分')
            testFailP3(window)
            util.FLAG = 1
    else:
        if util.DEBUG:
            print('【DEBUG】被试对象测试通过')
        dispP3inst2(window)

def dispP3inst(window):
    util.FLAG = 2
    frame = tk.Frame(window)
    frame.pack()
    tk.Label(frame, text=util.TITLE_PREFIX+'实验二'+util.TITLE_SUFFIX,
            font=('Arial', util.TITLE_FONT_SIZE)).pack()
    tk.Label(frame, text='关于前面您做过的题目，在今年3月份我们通过网络问卷的形式，收集到了另外一批人的决策信息。\n\
在接下来的实验中，您会看到每道题每个选项有多少比例的人选择了该选项。\n\
如下图所示：',
            font=('KaiTi', util.TEXT_FONT_SIZE)).pack()
    photo = Image.open("src\\p3test.png")
    photo = photo.resize((850,480)) 
    util.PHOTO = ImageTk.PhotoImage(photo)
    imgLabel = tk.Label(frame,image=util.PHOTO).pack()
    tk.Label(frame, text='我们发现有64%的人选择将物资送往上方区域，36%的人选择将物资送往下方区域。\n\
在接下来的情境中，我们将提供每种情境下选择人数的百分比的信息。',
            font=('KaiTi', util.TEXT_FONT_SIZE)).pack()
    def click():
        frame.destroy()
        P3windowControl(window)
    tk.Button(frame, text="我已理解图片信息", command = click,font=('KaiTi', util.TEXT_FONT_SIZE)).pack()


# 打印第二部分的说明  
def dispP3inst2(window):
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
        dispP3prob(window, 1)
    tk.Button(frame, text="确定", command = click,font=('KaiTi', util.TEXT_FONT_SIZE)).pack()


def dispP3test(window):
    frame = tk.Frame(window)
    frame.pack()
    tk.Label(frame, text=util.TITLE_PREFIX+'测试题'+util.TITLE_SUFFIX,
            font=('KaiTi', util.TITLE_FONT_SIZE)).pack()
    photo = Image.open("src\\p3test.png")
    photo = photo.resize((850,480)) 
    util.PHOTO = ImageTk.PhotoImage(photo)
    imgLabel = tk.Label(frame,image=util.PHOTO).pack()
    tk.Label(frame, text='在以上情境中，“上方区域（64%人选择）”中的64%表示：',
            font=('KaiTi', util.TEXT_FONT_SIZE)).pack()
    ans = tk.StringVar()
    tk.Radiobutton(frame, text='64%的可能性物资会送往上方区域',variable=ans, value='A',font=('KaiTi', util.TEXT_FONT_SIZE-2)).pack()
    tk.Radiobutton(frame, text='在人群中64%的人会选择将物资送往上方区域',variable=ans, value='B',font=('KaiTi', util.TEXT_FONT_SIZE-2)).pack()
    def click1():
        util.FLAG = 1
        frame.destroy()
        P3windowControl(window)
    def click2():
        util.FLAG = 3
        if ans.get() == 'B':
            util.FLAG = -1
        frame.destroy()
        P3windowControl(window)
    tk.Button(frame, text="返回查看说明", command = click1, font=('KaiTi', util.TEXT_FONT_SIZE-8)).pack()
    tk.Button(frame, text="提交", command = click2, font=('KaiTi', util.TEXT_FONT_SIZE)).pack()
    
    


def dispP3prob(window, counter):
    pic_id = util.shuffled_pic2[counter-1]
    each = pic_id
    up_is_major = False
    # 如果之前选了上，且该题在choice_major_pic中
    if util.p2ans[str(each)][0]=='上' and (each in util.choice_major_pic):
        up_is_major = True
    # 如果之前选了下，且该题不在choice_major_pic
    if util.p2ans[str(each)][0]=='下' and (each not in util.choice_major_pic):
        up_is_major = True
    #-----------------------
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
        util.P3ANS.append((tmp, time_spent))
        frame.destroy()
        if counter == util.PIC_NUM:
            util.p3ans = dict({})
            for i in range(util.PIC_NUM):
                util.p3ans[str(util.shuffled_pic2[i])] = util.P3ANS[i]
            if util.DEBUG:
                print('【DEBUG】第三部分测试结束。测试结果为：')
            for each in util.p3ans.keys():
                print(each+':'+util.p3ans[each][0], end = ' ')
            print()
            util.writeAns(window)
        else:
            if counter == util.test1_pos:
                P3TestProb(window,util.test_ans, counter+1)
            elif counter == util.test2_pos:
                P3TestProb(window,1-util.test_ans, counter+1)
            else:
                dispP3prob(window, counter+1)
    frame = tk.Frame(window)
    frame.bind('<Key>', pressKey)
    frame.focus_set()
    frame.pack()
    if util.DEBUG:
        print('【DEBUG】现在是第三部分，正在展示编号为'+str(pic_id)+'的图片')
    tk.Label(frame, text=util.TITLE_PREFIX, font=('KaiTi', util.TITLE_FONT_SIZE)).pack()
    tk.Label(frame, text='如果两地区患病情况如下，您打算将医疗物资运往哪个地区？',
            font=('KaiTi', util.TEXT_FONT_SIZE),justify= 'left').pack()
    photo = Image.open("src\\"+str(pic_id)+".png")
    photo = photo.resize(util.PIC_SIZE) 
    util.PHOTO = ImageTk.PhotoImage(photo)
    imgLabel = tk.Label(frame,image=util.PHOTO).pack()
    tk.Label(frame, text='请做出您的选择',
            font=('KaiTi', util.TEXT_FONT_SIZE),justify= 'left').pack()
    if up_is_major:
        tk.Label(frame, text='上方地区（'+str(format(1-float(util.FAKE_RATE[pic_id-1]),'.2f'))[2:4]+'%人选择）',font=('KaiTi', util.TEXT_FONT_SIZE)).pack()
        tk.Label(frame, text='下方地区（'+str(format(float(util.FAKE_RATE[pic_id-1]),'.2f'))[2:]+'%人选择）',font=('KaiTi', util.TEXT_FONT_SIZE)).pack()
    else:
        tk.Label(frame, text='上方地区（'+str(format(float(util.FAKE_RATE[pic_id-1]),'.2f'))[2:]+'%人选择）',font=('KaiTi', util.TEXT_FONT_SIZE)).pack()
        tk.Label(frame, text='下方地区（'+str(format(1-float(util.FAKE_RATE[pic_id-1]),'.2f'))[2:4]+'%人选择）',font=('KaiTi', util.TEXT_FONT_SIZE)).pack()
    util.T1 = time.time()


# 第三部分测试不通过
def testFailP3(window):
    frame = tk.Frame(window)
    frame.pack()
    tk.Label(frame, text=util.TITLE_PREFIX+'很抱歉，你没能通过测试'+util.TITLE_SUFFIX,
             font=('KaiTi', util.TITLE_FONT_SIZE)).pack()
    tk.Label(frame, text='请确保完全读懂题意后再进行测试',font=('KaiTi', util.TEXT_FONT_SIZE)).pack()
    def click():
        util.FLAG = 1
        frame.destroy()
        P3windowControl(window)
    tk.Button(frame, text="确定", command=click).pack()


def P3TestProb(window, true_ans, counter):
    if true_ans == 0:
        true_ans = '上'
    else:
        true_ans = '下'
    if util.DEBUG:
        print('【DEBUG】正在展示测试题。本题的标准答案为：',true_ans)
    part = '三'
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
        dispP3prob(window, counter)
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
    ans = tk.StringVar()
    tk.Label(frame, text='上方地区（50%人选择）',font=('KaiTi', util.TEXT_FONT_SIZE)).pack()
    tk.Label(frame, text='下方地区（50%人选择）',font=('KaiTi', util.TEXT_FONT_SIZE)).pack()
    


