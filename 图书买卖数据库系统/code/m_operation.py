import tkinter as tk
import tkinter.messagebox as msg
import search
from tkinter import ttk
import pymysql
import ID
import BookSellDB as db
from pswd import *

def frame():
    window=tk.Tk()
    window.title('管理员')
    window.geometry('900x700')
    lable0 = tk.Label(window, text='图书管理界面', bg='cyan', font=('微软雅黑', 50)).pack()  # 上

    lable1 = tk.Label(window, text='请选择操作:', font=('微软雅黑', 20)).place(x=80, y=400)  # 下
    tk.Button(window, text='进购', font=('微软雅黑', 15), width=10, height=2,command=purchase).place(x=350, y=200)
    tk.Button(window, text='卖书', font=('微软雅黑', 15), width=10, height=2,command=sell).place(x=350, y=300)
    tk.Button(window, text='退书', font=('微软雅黑', 15), width=10, height=2,command=refund).place(x=350, y=400)
    tk.Button(window, text='信息查询', font=('微软雅黑', 15), width=10, height=2,command=search_what).place(x=350, y=500)

    window.mainloop()

def purchase():#进货
    global win
    win = tk.Tk()
    win.title('图书销售管理')
    win.geometry('900x600')
    win.wm_attributes('-topmost', 1)
    lable1 = tk.Label(win, text='请填写进购图书的信息:', font=('微软雅黑', 20)).place(x=200, y=30)

    global tree#建立树形图
    yscrollbar = ttk.Scrollbar(win, orient='vertical')#右边的滑动按钮
    tree = ttk.Treeview(win, columns=('1', '2', '3', '4', '5', '6'), show="headings",yscrollcommand=yscrollbar.set)
    tree.column('1', width=100, anchor='center')
    tree.column('2', width=100, anchor='center')
    tree.column('3', width=100, anchor='center')
    tree.column('4', width=100, anchor='center')
    tree.column('5', width=100, anchor='center')
    tree.column('6', width=100, anchor='center')
    tree.heading('1', text='图书id')
    tree.heading('2', text='书名')
    tree.heading('3', text='供应商id')
    tree.heading('4', text='供应商')
    tree.heading('5', text='进价')
    tree.heading('6', text='库存')
    tree.place(x=120, y=100)
    yscrollbar.place(x=800,y=150)
    db = pymysql.connect("localhost", user_name, pass_word, "booksell") 
    cursor = db.cursor()
    try:
        cursor.execute("select book_id,title,supplier.id,name,price,count from supplier,book where book_id = book.id group by supplier.id,book_id order by book_id,price")
    except:
        msg._show(title='错误！',message='数据库查询出错！')
        return
    results=cursor.fetchall()
    if results:
        l= len(results)
        for i in range(0,l):#查询到的结果依次插入到表格中
            tree.insert('',i,values=(results[i]))
    else :
        tree.insert('', 0,values=('查询不到结果','查询不到结果','查询不到结果','查询不到结果','查询不到结果','查询不到结果'))
    db.close()

    global b_id
    tk.Label(win, text='图书id：', font=('宋体', 12)).place(x=100, y=400)
    b_id = tk.Entry(win, font=('宋体', 12), width=5)
    b_id.place(x=170, y=400)

    global p_id
    tk.Label(win, text='供货商id：', font=('宋体', 12)).place(x=250, y=400)
    p_id = tk.Entry(win, font=('宋体', 12), width=5)
    p_id.place(x=350, y=400)

    global amount
    tk.Label(win, text='数量：', font=('宋体', 12)).place(x=430, y=400)
    amount = tk.Entry(win, font=('宋体', 12), width=5)
    amount.place(x=500, y=400)

    global month
    tk.Label(win, text='月：', font=('宋体', 12)).place(x=250, y=500)
    month = tk.Entry(win, font=('宋体', 12), width=5)
    month.place(x=300, y=500)

    global day
    tk.Label(win, text='日：', font=('宋体', 12)).place(x=400, y=500)
    day = tk.Entry(win, font=('宋体', 12), width=5)
    day.place(x=450, y=500)

    tk.Button(win, text='确认', font=('宋体', 12), width=10, command=lambda:add(b_id,p_id,amount,month,day)).place(x=600, y=400)
    
def add(b_id,p_id,num,month,day):#添加图书信息到数据库中
    #sql="INSERT INTO book VALUES('%s','%s','%s','%s','%s')"% (list.get(),b_name.get(),author.get(),price.get(),amount.get())
    db = pymysql.connect("localhost", user_name, pass_word, "booksell")
    cursor = db.cursor()
    #cursor.execute(sql)
    


    cursor.execute('select count,price from book,supplier where book_id = book.id and book.id = ' + b_id.get() + ' and supplier.id = ' + p_id.get())
    res = cursor.fetchone()
    rest_num = res[0]
    price_in = res[1]
    #print(rest_num+int(num.get()),price_in)

    
    try:
        cursor.execute("start transaction")
        
        cursor.execute("update book set count = " + str(rest_num+int(num.get())) + ', price_in = ' +
                       str(price_in) + ', price_out=' + str(format(1.2 * float(price_in), '.2f')) + 'where id = ' + b_id.get())
        
        # 添加进货记录
        cursor.execute('select num from purchase where id =' + b_id.get() + ' and month=' + month.get() + ' and day=' +
                       day.get() + ' and supplier_id=' + p_id.get())
        record_num = cursor.fetchone()
        #print(record_num)
        # 如果没有当天的进货记录则创建新的进货记录
        if record_num == ():
            #print(1)
            cursor.execute("insert into purchase values(" + b_id.get() + ',' + month.get() + ',' + day.get() + ',' +
                                num.get() + ',' + p_id.get() + ")")
            
        # 否则直接修改当天的进货记录
        else:
            if record_num[0] + int(num.get()) == 0:
                #print(2) 
                cursor.execute("delete from purchase where id=" + b_id.get() +
                               " and month=" + month.get() + " and day=" + day.get() + " and supplier_id=" + p_id.get())
                           
            else:
                #print(3)
                cursor.execute(
                    "update purchase set num=" + str(record_num[0] + int(num.get())) + " where id=" + b_id.get() +
                    " and month=" + month.get() + " and day=" + day.get() + " and supplier_id=" + p_id.get())
                
    except:
        msg._show(title='错误！',message='数据库查询出错！')
        cursor.execute("rollback")                 # 出错时需要回滚

    db.commit()#这句不可或缺，当我们修改数据完成后必须要确认才能真正作用到数据库里

    db.close()
    msg.showinfo(title='成功！', message='新书已入库！')

def sell():#卖书
    global win
    win = tk.Tk()
    win.title('图书销售管理')
    win.geometry('900x300')
    win.wm_attributes('-topmost', 1)
    lable1 = tk.Label(win, text='请填写购买信息：', bg='cyan',font=('微软雅黑', 20)).place(x=30, y=100)

    global b_id2
    tk.Label(win, text='图书id：', font=('宋体', 12)).place(x=50, y=200)
    b_id2 = tk.Entry(win, font=('宋体', 12), width=5)
    b_id2.place(x=120, y=200)

    global amount2
    tk.Label(win, text='数量：', font=('宋体', 12)).place(x=190, y=200)
    amount2 = tk.Entry(win, font=('宋体', 12), width=5)
    amount2.place(x=260, y=200)

    global month2
    tk.Label(win, text='月：', font=('宋体', 12)).place(x=330, y=200)
    month2 = tk.Entry(win, font=('宋体', 12), width=5)
    month2.place(x=400, y=200)

    global day2
    tk.Label(win, text='日：', font=('宋体', 12)).place(x=470, y=200)
    day2 = tk.Entry(win, font=('宋体', 12), width=5)
    day2.place(x=540, y=200)

    global customer2
    tk.Label(win, text='顾客id：', font=('宋体', 12)).place(x=610, y=200)
    customer2 = tk.Entry(win, font=('宋体', 12), width=5)
    customer2.place(x=680, y=200)

    tk.Button(win, text='确认购买', font=('宋体', 12), width=10, command=lambda:confirm_sell(b_id2,amount2,month2,day2,customer2)).place(x=750, y=195)

def refund():#退货
    global win
    win = tk.Tk()
    win.title('图书销售管理')
    win.geometry('900x300')
    win.wm_attributes('-topmost', 1)
    lable1 = tk.Label(win, text='请填写退货信息：', bg='cyan',font=('微软雅黑', 20)).place(x=30, y=100)

    global b_id3
    tk.Label(win, text='图书id：', font=('宋体', 12)).place(x=50, y=200)
    b_id3 = tk.Entry(win, font=('宋体', 12), width=5)
    b_id3.place(x=120, y=200)

    global amount3
    tk.Label(win, text='数量：', font=('宋体', 12)).place(x=190, y=200)
    amount3 = tk.Entry(win, font=('宋体', 12), width=5)
    amount3.place(x=260, y=200)

    global month3
    tk.Label(win, text='月：', font=('宋体', 12)).place(x=330, y=200)
    month3 = tk.Entry(win, font=('宋体', 12), width=5)
    month3.place(x=400, y=200)

    global day3
    tk.Label(win, text='日：', font=('宋体', 12)).place(x=470, y=200)
    day3 = tk.Entry(win, font=('宋体', 12), width=5)
    day3.place(x=540, y=200)

    global month4
    tk.Label(win, text='售出月：', font=('宋体', 12)).place(x=330, y=250)
    month4 = tk.Entry(win, font=('宋体', 12), width=5)
    month4.place(x=400, y=250)

    global day4
    tk.Label(win, text='售出日：', font=('宋体', 12)).place(x=470, y=250)
    day4 = tk.Entry(win, font=('宋体', 12), width=5)
    day4.place(x=540, y=250)

    global customer3
    tk.Label(win, text='顾客id：', font=('宋体', 12)).place(x=610, y=200)
    customer3 = tk.Entry(win, font=('宋体', 12), width=5)
    customer3.place(x=680, y=200)

    tk.Button(win, text='确认退货', font=('宋体', 12), width=10, command=lambda:confirm_refund(b_id3,amount3,month3,day3,month4,day4,customer3)).place(x=750, y=195)

def confirm_sell(b_id,num,month,day,c_id):
    db = pymysql.connect("localhost", user_name, pass_word, "booksell")
    cursor = db.cursor()
    if (not validNum(int(num.get()))) or (not validDate(int(month.get()),int(day.get()))) or (not validCustomer(int(c_id.get()))):
        return
    # 输入合法则从数据库获取数据
    try:
        
        cursor.execute("start transaction")
        # 如果使用书名查询，则先获取id
        cursor.execute("select id from book where id = " + b_id.get())
        book = cursor.fetchone()
        if book == ():
            msg._show(title='错误！',message='查询错误：查询不到该书数据')
            db.commit()
            return
        # 获取该书的库存数量
        cursor.execute('select count from book where id = ' + b_id.get())
        rest_num = cursor.fetchone()
        if rest_num == ():
            msg._show(title='错误！',message='查询错误：查询不到该书数据')
            db.commit()
            return
        rest_num = rest_num[0]
        # 库存不足则出错
        if int(num.get()) > rest_num:
            msg._show(title='错误！',message='库存不足：该书库存只剩余' + str(rest_num) + '本')
            db.commit()
            return
        # 否则可以出售
        else:
            # 修改库存
            cursor.execute("update book set count = " + str(rest_num - int(num.get())) + ' where id = ' + b_id.get())
            cursor.execute('select num from sold where id = ' + b_id.get() + ' and month=' + month.get() + ' and day=' +
                           day.get() + ' and customer_id=' + c_id.get())
            record_num = cursor.fetchone()
            # 如果没有当天的销售记录则创建新的销售记录
            if record_num == None:
                cursor.execute("insert into sold values(" + b_id.get() + ',' + month.get() + ',' +  day.get() + ',' +
                                    num.get() + ',' + c_id.get() + ")")
            # 否则直接修改当天的销售记录
            else:
                if record_num[0]+int(num.get()) == 0:
                    cursor.execute("delete from sold where id=" + b_id.get() +
                                   " and month=" + month.get() +" and day=" + day.get() + " and customer_id=" + c_id.get())
                else:
                    cursor.execute("update sold set num=" + str(record_num[0]+int(num.get())) + " where id=" + b_id.get() +
                                   " and month=" + month.get() +" and day=" + day.get() + " and customer_id=" + c_id.get())
    except:
        msg._show(title='错误！',message='数据库查询或修改出错')
        cursor.execute("rollback")                 # 出错时需要回滚
    db.commit()
    db.close()
    msg.showinfo(title='购买成功', message='购买成功！')
    win.destroy()

def confirm_refund(b_id,num,month,day,sell_month,sell_day,c_id):
    db = pymysql.connect("localhost", user_name, pass_word, "booksell")
    cursor = db.cursor()
    if (not validNum(int(num.get()))) or (not validDate(int(month.get()), int(day.get()))) or (not validCustomer(int(c_id.get()))) or\
            (not validDate(int(sell_month.get()), int(sell_day.get()))):
        return
        # 输入合法则从数据库获取数据
    try:
        cursor.execute("start transaction")
        # 如果使用书名查询，则先获取id
        cursor.execute("select id from book where id = " + b_id.get())
        book = cursor.fetchone()
        if book == ():
            msg._show(title='错误！',message='查询错误：查询不到该书数据')
            db.commit()
            return
        # 获取该书的销售记录
        cursor.execute('select * from sold where id = ' + b_id.get() + ' and month=' + sell_month.get() + ' and day=' + sell_day.get()
                       + ' and customer_id=' + c_id.get())
        sell_log = cursor.fetchone()
        
        if sell_log == ():
            msg._show(title='错误！',message='查询错误：查询不到该日期下该顾客对该书的购买信息')
            db.commit()
            return
        sell_log = sell_log[3]
        # 退货数超出购买数则报错
        if int(num.get()) > sell_log:
            msg._show(title='错误！',message='数目错误：退货数大于购买数')
            db.commit()
            return
        # 否则可以退货
        else:
            # 修改库存
            #print(0)
            cursor.execute("select count from book where id = " + b_id.get())
            rest_num = cursor.fetchone()[0]
            cursor.execute("update book set count = " + str(rest_num + int(num.get())) + ' where id = ' + b_id.get())
            cursor.execute('select num from sold where id = ' + b_id.get() + ' and month=' + month.get() + ' and day=' +
                           day.get() + ' and customer_id=' + c_id.get())
            record_num = cursor.fetchone()
            # 如果没有当天的退货记录则创建新的退货记录
            if record_num == None:
                cursor.execute("insert into sold values(" + b_id.get() + ',' + month.get() + ',' + day.get() + ',' +
                    str(-int(num.get())) + ',' + c_id.get() + ")")
            # 否则直接修改退货记录
            else:
                if record_num[0]-int(num.get()) == 0:
                    cursor.execute("delete from sold where id=" + b_id.get() +
                                   " and month=" + month.get() +" and day=" + day.get() + " and customer_id=" + c_id.get())
                else:
                    cursor.execute("update sold set num=" + str(record_num[0]-int(num.get())) + " where id=" + b_id.get() +
                                   " and month=" + month.get() +" and day=" + day.get() + " and customer_id=" + c_id.get())
    except:
        msg._show(title='错误！',message='Error:数据库查询或修改出错')
        cursor.execute("rollback")  # 出错时需要回滚
    db.commit()
    msg.showinfo(title='退书成功', message='退书成功！')
    win.destroy()

def search_what():
    window=tk.Tk()
    window.title('图书管理系统')
    window.geometry('900x700')
    lable0 = tk.Label(window, text='查询界面', bg='cyan', font=('微软雅黑', 50)).pack()  # 上

    lable1 = tk.Label(window, text='请选择操作:', font=('微软雅黑', 20)).place(x=80, y=400)  # 下
    tk.Button(window, text='书本库存', font=('微软雅黑', 15), width=10, height=2,command=search.book).place(x=350, y=250)
    tk.Button(window, text='销售数据', font=('微软雅黑', 15), width=10, height=2,command=search.sell).place(x=350, y=400)

    window.mainloop()

def validDate(month, day):
    if type(month) != type(1) or type(day) != type(1):
        return False
    if month < 1 or month > 13:
        return False
    if month in (1,3,5,7,8,10,12) and day > 0 and day < 32:
        return True
    elif month in (4,6,9,11) and day > 0 and day < 31:
        return True
    elif month == 2 and day > 0 and day <30:
        return True
    else:
        return False

# 判断输入数目合法性
def validNum(num):
    if type(num) != type(1) or num <= 0:
        msg._show(title='错误！',message='输入错误：书的数目输入不合法，应为正整数')
        return False
    return True

# 判断输入顾客编号合法性
def validCustomer(customer):
    if type(customer) != type(1):
        msg._show(title='错误！',message='输入错误：顾客编号输入不合法，应为整数')
        return False
    return True