import tkinter as tk
from PIL import Image,ImageTk
import util


def dispP3inst():
    window = util.createWindow()
    tk.Label(window, text='\n\n\n第二部分结束',
            font=('Arial', 30)).pack()
    tk.Label(window, text='\n你完成了第二部分的测试。\n\
接下来各个情境，其他信息类型不变，但是你将额外得知多数人选择的选项，请做出你的选择\n\
点击下面的按钮开始第三部分的测试。\n\n',
            font=('Arial', 15),justify= 'left').pack()
    def click():
        window.destroy()
    tk.Button(window, text="确定", command = window.destroy).pack()
    window.mainloop()


def dispP3prob(pic_id, up_is_major):
    if util.DEBUG:
        print('【DEBUG】现在是第三部分，正在展示编号为'+str(pic_id)+'的图片')
    window = util.createWindow()
    tk.Label(window, text='第三部分',
            font=('Arial', 30)).pack()
    tk.Label(window, text='请依据图片信息回答问题',
            font=('Arial', 20),justify= 'left').pack()
    photo = Image.open("src\\"+str(pic_id)+".png")
    photo = photo.resize((1000,340)) 
    photo = ImageTk.PhotoImage(photo)
    imgLabel = tk.Label(window,image=photo).pack()
    tk.Label(window, text='您打算将医疗物资运往哪个地区？请做出选择',
            font=('Arial', 15),justify= 'left').pack()
    ans = tk.StringVar()
    if up_is_major:
        tk.Radiobutton(window, text='上方地区（大多数人选择了该选项）',variable=ans, value='上',font=('Arial', 20)).pack()
        tk.Radiobutton(window, text='下方地区（小部分人选择了该选项）',variable=ans, value='下',font=('Arial', 20)).pack()
    else:
        tk.Radiobutton(window, text='上方地区（小部分人选择了该选项）',variable=ans, value='上',font=('Arial', 20)).pack()
        tk.Radiobutton(window, text='下方地区（大多数人选择了该选项）',variable=ans, value='下',font=('Arial', 20)).pack()
    def click():
        tmp = ans.get()
        if tmp == "":
            if util.DEBUG:
                print('【DEBUG】被试对象没有选择答案就提交，本题重新测试')
            return
        if util.DEBUG:
            print('【DEBUG】被试对象选择的答案是:' + tmp)
        util.P3ANS.append(tmp)
        window.destroy()
    tk.Button(window, text="确定", command = click).pack()
    window.mainloop()
