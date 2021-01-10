import tkinter as tk

def frame():#初始界面
    global root
    root=tk.Tk()
    root.geometry('900x700')
    root.title('416图书销售管理系统')
    lable0=tk.Label(root,text='制作者名单',bg='cyan',font=('微软雅黑',50)).pack()
    lable1=tk.Label(root,text='方维远',bg='cyan',font=('微软雅黑',50)).place(x=80, y=200) 
    lable1=tk.Label(root,text='侯少森',bg='cyan',font=('微软雅黑',50)).place(x=80, y=300) 
    lable1=tk.Label(root,text='胡霆熙',bg='cyan',font=('微软雅黑',50)).place(x=80, y=400) 
   
    tk.Button(root, text='退出',font=('微软雅黑',15),width=10, height=2,command=exit_creator).place(x=385, y=550)

    root.mainloop()#必须要有这句话，你的页面才会动态刷新循环，否则页面不会显示 

def exit_creator():#跳转至管理员界面
    root.destroy()
