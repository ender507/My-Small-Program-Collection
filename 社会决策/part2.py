import tkinter as tk
from PIL import Image,ImageTk
import util

# 打印第二部分的说明  
def dispP2inst():
    window = util.createWindow()
    tk.Label(window, text=util.TITLE_PREFIX+'第一部分结束'+util.TITLE_SUFFIX,
            font=('Arial', util.TITLE_FONT_SIZE)).pack()
    tk.Label(window, text='恭喜你通过了第一部分的测试。\n\
点击下面的按钮开始第二部分的测试（之后的题目之后的题除了测试题，都没有标准答案）',
            font=('Arial', util.TEXT_FONT_SIZE),justify= 'left').pack()
    tk.Button(window, text="确定", command = window.destroy).pack()
    window.mainloop()


def dispP2prob(pic_id):
    if util.DEBUG:
        print('【DEBUG】现在是第二部分，正在展示编号为'+str(pic_id)+'的图片')
    window = util.createWindow()
    tk.Label(window, text=util.TITLE_PREFIX+'第二部分'+util.TITLE_SUFFIX,
            font=('Arial', util.TITLE_FONT_SIZE)).pack()
    tk.Label(window, text='请依据图片信息回答问题',
            font=('Arial', util.TEXT_FONT_SIZE),justify= 'left').pack()
    photo = Image.open("src\\"+str(pic_id)+".png")
    photo = photo.resize(util.PIC_SIZE) 
    photo = ImageTk.PhotoImage(photo)
    imgLabel = tk.Label(window,image=photo).pack()
    tk.Label(window, text='您打算将医疗物资运往哪个地区？请做出选择',
            font=('Arial', util.TEXT_FONT_SIZE),justify= 'left').pack()
    ans = tk.StringVar()
    tk.Radiobutton(window, text='上方地区',variable=ans, value='上',font=('Arial', util.TEXT_FONT_SIZE)).pack()
    tk.Radiobutton(window, text='下方地区',variable=ans, value='下',font=('Arial', util.TEXT_FONT_SIZE)).pack()
    def click():
        tmp = ans.get()
        if tmp == "":
            if util.DEBUG:
                print('【DEBUG】被试对象没有选择答案就提交，本题重新测试')
            return
        if util.DEBUG:
            print('【DEBUG】被试对象选择的答案是:' + tmp)
        util.P2ANS.append(tmp)
        window.destroy()
    tk.Button(window, text="确定", command = click,font=('Arial', util.TEXT_FONT_SIZE)).pack()
    window.mainloop()
