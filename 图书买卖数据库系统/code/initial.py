import tkinter as tk
import manager
import creator

def frame():#初始界面
    global root
    root=tk.Tk()
    root.geometry('900x700')
    root.title('416图书销售管理系统')
    lable0=tk.Label(root,text='欢迎回来, Admin!',bg='cyan',font=('微软雅黑',50)).pack()#上
	#canvas是个画布，想要插入图片的话首先要定义个canvas
    canvas=tk.Canvas(root,height=500,width=500)#中
    image_file=tk.PhotoImage(file='sysu.gif')
    #图片文件的后缀必须是.gif，且亲测不能自行鼠标右键重命名更改成.gif，要用win10里内置的画图功能，打开图片然后另存为的时候选择.gif
    #图片文件必须放到你的项目目录里边才有效
    image=canvas.create_image(250,100,image=image_file)
    canvas.place(x=200,y=200)

    #lable1=tk.Label(root,text='请选择用户类型:',font=('微软雅黑',20)).place(x=80,y=500)#下
    tk.Button(root, text='制作者名单',font=('微软雅黑',15),width=10, height=1,command=creator.frame).place(x=385, y=600)
    tk.Button(root, text='登录',font=('微软雅黑',15),width=10, height=2,command=exit_manager).place(x=385, y=450)

    root.mainloop()#必须要有这句话，你的页面才会动态刷新循环，否则页面不会显示 


def exit_manager():#跳转至管理员界面
    root.destroy()
    manager.frame()

if __name__ == '__main__':
    frame()


