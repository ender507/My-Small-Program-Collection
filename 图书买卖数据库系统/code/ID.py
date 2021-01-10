import tkinter as tk
import tkinter.messagebox as msg
import pymysql
import initial
import manager
import reader
import m_operation
import r_operation
def id_check():#检查账号
    global id
    id = manager.entry_name.get()
    password = manager.entry_key.get()
    getid()#最后得到id
    try:
        db = pymysql.connect("localhost", id, password, "booksell")
    except:
        msg._show(title='错误！',message='账号或密码输入错误！')
        return 
    success_login()#密码对上了，进入对应的读者/管理员操作界面
    db.close()#查询完一定要关闭数据库啊

def success_login():#成功登录
    manager.root1.destroy()
    m_operation.frame()#销毁登录注册界面，跳转到管理员的操作界面

def getid():
    return id

