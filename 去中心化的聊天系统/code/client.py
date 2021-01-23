import rpyc
import threading
import time

# 第二个线程持续监听信道，返回新消息
def getMes(conn2, user_name):
    while 1:
        mes = None
        mes = conn2.root.getMes(user_name)
        if mes != None and mes != "":
            t, s, u, m = mes.split(' ', 3)
            # 在私聊状态下收到对方消息
            if status == 1 and user2 == u:
                appendMes(user_name, u, mes, True)
                mes2disp(mes)
                #print('收到消息时间戳：', time.time())
            # 收到其他人的私聊消息
            elif status != 2:
                appendMes(user_name, u, mes, True)
                print('----提示：收到来自【'+u+'】的私聊消息----')
            # 收到群聊消息
            elif status == 2:
                appendMes(user_name, group, mes, False)
                mes2disp(mes)


# 读取本地聊天记录
def loadMes(user1, user2, private):
    if private:
        slt = '_'
    else:
        slt = '__'
    file_name = 'chatting log\\' + user1 + slt + user2 +'.txt'
    mes = ""
    # 打开本地聊天记录文件
    try:
        f = open(file_name, 'r')
        for eachLine in f:
            mes = mes + eachLine
        f.close()
    # 若不存在聊天记录则新建
    except:
        f = open(file_name, 'w')
        f.close()
    return mes

# 以覆盖的方式写入本地聊天记录
def saveMes(user1, user2, mes, private):
    if private:
        slt = '_'
    else:
        slt = '__'
    file_name = 'chatting log\\' + user1 + slt + user2 +'.txt'
    with open(file_name, 'w') as f:
        f.write(mes)

# 以添加的方式写入本地聊天记录
def appendMes(user1, user2, mes, private):
    if private:
        slt = '_'
    else:
        slt = '__'
    file_name = 'chatting log\\' + user1 + slt + user2 +'.txt'
    with open(file_name, 'a') as f:
        f.write(mes)
    
# 将记录转换成聊天消息并打印
def mes2disp(mes):
    if mes != "":
        t, s, u, m = mes.split(' ', 3)
        print('【'+u+'】'+ m)
        #print('发送消息时间戳：',t)
    
# 连接服务器节点
conn = rpyc.connect('localhost',9999)
login_status = False
while 1:
        user_name = input('请输入用户名:')
        print(user_name)
        login_status = conn.root.login(user_name)
        if login_status == False:
                print('用户名重复，请重新输入!')
        else:
                print('登录成功')
                break



status = 0      # 状态，为0表示接收消息但不显示，为1则显示私聊消息，2为群聊消息
user2 = None    # 私聊对象
group = None    # 群聊的群
# 开始监听信道，接收消息
conn2 = rpyc.connect('localhost',9999)
t1 = threading.Thread(target = getMes, args = (conn2, user_name,))
t1.start()
# 主页面指令
while 1:
    print('请输入数字下达指令：')
    print('【1】查看所有在线用户')
    print('【2】发起私聊')
    print('【3】查看所有聊天群')
    print('【4】进入群聊（群组不存在则会新建）')
    print('【5】退出程序')
    cmd = input()

    
    # 查看所有在线用户
    if cmd == '1':
        print(conn.root.getOnlineUserList(user_name))

        
    # 发起私聊
    elif cmd == '2':
        # 确立私聊对象
        user2 = input('请输入私聊对象的用户名：')
        if user_name == user2:
            print('不能建立与自己的私聊！')
            continue
        # 拉取本地聊天记录并推送到服务器
        old_mes = loadMes(user_name, user2, True)
        res = conn.root.pushPrivateMes(old_mes, user_name, user2)
        saveMes(user_name, user2, res, True)
        status = 1
        print('进入与', user2, '的私聊状态，输入exit退出私聊')
        # 打印消息记录
        mes = res.split('\n')
        for each in mes:
            mes2disp(each)
        while 1:
            mes = input()
            # 退出私聊
            if mes == 'exit':
                status = 0
                user2 = None
                break
            else:
            # 消息 = 时间戳 + 状态 + 发送者 +发送内容
                print('【'+user_name+'】'+mes)
                mes = str(time.time()) + ' 1 ' + user_name + ' ' + mes +'\n'
                appendMes(user_name, user2, mes, True)# 写入本地聊天记录
                conn.root.sendPrivateMes(user_name, user2, mes)# 发给服务器


    # 查看所有群组
    elif cmd == '3':
        print(conn.root.getGroupList())

    # 进入群聊
    elif cmd == '4':
        group = input('请输入群聊名称：')
        # 拉取本地聊天记录并推送到服务器
        old_mes = loadMes(user_name, group, False)
        res = conn.root.pushGroupMes(old_mes, user_name, group)
        saveMes(user_name, group, res, False)
        status = 2
        print('进入在', group, '的群聊状态，输入exit退出群聊')
        # 打印历史聊天记录
        mes = res.split('\n')
        for each in mes:
            mes2disp(each)
        while 1:
            mes = input()
            # 退出群聊
            if mes == 'exit':
                conn.root.exitGroup(user_name, group)
                status = 0
                group = None
                break
            else:
            # 消息 = 时间戳 + 状态 + 发送者 +发送内容
                mes = str(time.time()) + ' 2 ' + user_name + ' ' + mes +'\n'
                conn.root.sendGroupMes(group, mes)# 发给服务器
        
    
    # 退出程序
    elif cmd == '5':
        conn.root.logout(user_name)
        print('退出程序...')
        exit()

    # 其他输入    
    else:
        print('输入有误，请重新输入')
