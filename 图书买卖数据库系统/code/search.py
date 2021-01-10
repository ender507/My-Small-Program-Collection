import tkinter as tk
import tkinter.messagebox as msg
from tkinter import ttk
import pymysql
from BookSellDB import *
from pswd import *
def book_search(book_id,title):
    
    tree.delete(*tree.get_children()) 
    db = pymysql.connect("localhost", user_name, pass_word, "booksell")
    cursor = db.cursor()
    #print(book_id.get(),title.get())
    try:
        # 默认情况：查看所有图书
        if book_id.get() == '' and title.get() == '':
            cursor.execute('select * from book')
        # 按书的id进行索引
        elif book_id.get() != '' and title.get() == '':
            cursor.execute('select * from book where id = ' + book_id.get())
        elif book_id.get() == '' and title.get() != '':
            cursor.execute('select * from book where title ="' + title.get()+'"')
        # 按书名进行索引
        else:
            cursor.execute("select * from book where id ="+book_id.get()+'title = "' + title.get()+'"')
    except:
        msg._show(title='错误！',message='数据库查询出错！')
        return
    results=cursor.fetchall()
    if results:
        l= len(results)
        for i in range(0,l):#查询到的结果依次插入到表格中
            tree.insert('',i,values=(results[i]))
    else :
        tree.insert('', 0,values=('查询不到结果','查询不到结果','查询不到结果','查询不到结果','查询不到结果'))
    db.close()

def book():
    global window
    window = tk.Tk()
    window.title('图书查询')
    window.geometry('900x600')

    global book_id
    tk.Label(window, text='图书id：', font=('宋体', 18)).place(x=200, y=100)
    book_id = tk.Entry(window, font=('宋体', 18), width=5)
    book_id.place(x=300, y=100)

    global title
    tk.Label(window, text='书名：', font=('宋体', 18)).place(x=400, y=100)
    title = tk.Entry(window, font=('宋体', 18), width=15)
    title.place(x=500, y=100)
    

    global tree#建立树形图
    yscrollbar = ttk.Scrollbar(window, orient='vertical')#右边的滑动按钮
    tree = ttk.Treeview(window, columns=('1', '2', '3', '4', '5'), show="headings",yscrollcommand=yscrollbar.set)
    tree.column('1', width=150, anchor='center')
    tree.column('2', width=150, anchor='center')
    tree.column('3', width=150, anchor='center')
    tree.column('4', width=150, anchor='center')
    tree.column('5', width=150, anchor='center')
    tree.heading('1', text='id')
    tree.heading('2', text='书名')
    tree.heading('3', text='库存')
    tree.heading('4', text='进价')
    tree.heading('5', text='售价')
    tree.place(x=50, y=200)
    yscrollbar.place(x=955,y=150)

    db = BookSellDatabase(user_name,pass_word)
    
    tk.Button(window, text='确认', font=('宋体', 18), width=10, command=lambda:book_search(book_id,title)).place(x=700, y=95)
    window.mainloop()

def sell():
    global window2
    window2 = tk.Tk()
    window2.title('图书查询')
    window2.geometry('900x600')

    global book_id
    tk.Label(window2, text='图书id：', font=('宋体', 18)).place(x=200, y=100)
    book_id = tk.Entry(window2, font=('宋体', 18), width=5)
    book_id.place(x=300, y=100)

    global month
    tk.Label(window2, text='月份：', font=('宋体', 18)).place(x=400, y=100)
    month = tk.Entry(window2, font=('宋体', 18), width=5)
    month.place(x=500, y=100)
    

    global tree2#建立树形图
    yscrollbar = ttk.Scrollbar(window2, orient='vertical')#右边的滑动按钮
    tree2 = ttk.Treeview(window2, columns=('1', '2', '3', '4', '5','6'), show="headings",yscrollcommand=yscrollbar.set)
    tree2.column('1', width=120, anchor='center')
    tree2.column('2', width=120, anchor='center')
    tree2.column('3', width=120, anchor='center')
    tree2.column('4', width=120, anchor='center')
    tree2.column('5', width=120, anchor='center')
    tree2.column('6', width=120, anchor='center')
    tree2.heading('1', text='月份')
    tree2.heading('2', text='书名')
    tree2.heading('3', text='销售数')
    tree2.heading('4', text='进价')
    tree2.heading('5', text='售价')
    tree2.heading('6', text='销售额')
    tree2.place(x=60, y=200)
    yscrollbar.place(x=800,y=500)

    db = BookSellDatabase(user_name,pass_word)
    
    tk.Button(window2, text='确认', font=('宋体', 18), width=10, command=lambda:sell_search(book_id,month)).place(x=700, y=95)
    window2.mainloop()

def sell_search(book_id,month):

    tree2.delete(*tree2.get_children()) 
    db = pymysql.connect("localhost", user_name, pass_word, "booksell")
    cursor = db.cursor()
    #print(book_id.get(),title.get())
    try:
        # 默认情况：查看所有图书
        if book_id.get() == '' and month.get() == '':
            cursor.execute('select month,title,sum(num),price_in,price_out,sum(num)*(price_out-price_in) from book,sold where book.id=sold.id group by month,book.id order by month,book.id')
        # 按书的id进行索引
        elif book_id.get() != '' and month.get() == '':
            cursor.execute('select month,title,sum(num),price_in,price_out,sum(num)*(price_out-price_in) from book,sold where book.id=sold.id and book.id = '+book_id.get()+ ' group by month,book.id order by month,book.id' )
        # 按月份进行索引
        elif book_id.get() == '' and month.get() != '':
            cursor.execute('select month,title,sum(num),price_in,price_out,num*(price_out-price_in) from book,sold where book.id=sold.id and month = '+month.get()+' group by month,book.id order by month,book.id' )
        else:
            cursor.execute("select month,title,sum(num),price_in,price_out,num*(price_out-price_in) from book,sold where book.id=sold.id and book.id= "+book_id.get()+ " and month= "+month.get()+" group by month,book.id order by month,book.id")
    except:
        msg._show(title='错误！',message='数据库查询出错！')
        return
    results=cursor.fetchall()
    if results:
        l= len(results)
        for i in range(0,l):#查询到的结果依次插入到表格中
            tree2.insert('',i,values=(results[i]))
    else :
        tree2.insert('', 0,values=('查询不到结果','查询不到结果','查询不到结果','查询不到结果','查询不到结果','查询不到结果'))
    db.close()