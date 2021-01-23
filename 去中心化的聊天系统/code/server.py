from rpyc import Service
from rpyc.utils.server import ThreadedServer
import time

# "exposed_"开头的方法能被客户端调用
class ChatService(Service):

    # 客户端登录，服务器记录在线状态        
    def exposed_login(self, user_name):
        global client_num
        if user_name in client_name:
            return False
        else:
            client_num += 1
            client_name.add(user_name)
            print('连入用户：', user_name)
            return True


    # 查看所有的在线用户
    def exposed_getOnlineUserList(self, user_name):
        mes = ""
        for each_user in client_name:
            if each_user != user_name:
                mes += each_user
                mes += "\n"
        mes = "当前在线用户共" + str(client_num-1) + "人:\n"+ mes
        return mes

    """
    客户端将本地聊天记录推送到服务器，客户端整合聊天记录并返回
    从而维护客户端本地聊天记录的一致性
    最终客户端保存整合后的聊天记录，服务器不保存聊天记录
    """
    # 收集、整合、推送私聊记录
    def exposed_pushPrivateMes(self, old_mes, user1, user2):
        res = ""
        # 将use1的本地聊天记录暂存在服务器
        if old_mes != "":
            private_channel[(user1, user2)] = old_mes
        # 若服务器保存了user2的本地聊天记录，则与user1的本地记录整合后
        # 返回给user1，从而维护消息的一致性
        if (user2, user1) in private_channel.keys():
            mes1 = old_mes.split('\n')
            mes2 = private_channel[(user2, user1)].split('\n')
            i = 0
            j = 0
            # 最后一行消息为空字符故要-1
            while i < len(mes1)-1 and j < len(mes2)-1:
                t1, m1 = mes1[i].split(' ', 1)
                t2, m2 = mes2[j].split(' ', 1)
                # 比较时间戳，较小的排在前
                t1 = float(t1)
                t2 = float(t2)
                if t1 > t2:
                    res = res + mes2[j] + '\n'
                    j += 1
                elif t1 < t2:
                    res = res + mes1[i] + '\n'
                    i += 1
                else:
                    res = res + mes1[i] + '\n'
                    i += 1
                    j += 1
            while i < len(mes1)-1:
                res = res + mes1[i] + '\n'
                i+= 1
            while j < len(mes2)-1:
                res = res + mes2[j] + '\n'
                j+= 1
            # 删掉服务器的聊天记录缓存
            del private_channel[(user2, user1)]
        else:
            res = old_mes
        return res

    # 推送群聊记录
    def exposed_pushGroupMes(self, old_mes, user, group):
        global group_num
        # 若群聊不存在则新建群聊
        if group not in group_name.keys():
            group_name[group] = set({})
            group_num += 1
            group_channel[group] = ""
        # 将当前用户加入群聊
        group_name[group].add(user)
        print(user, '加入群聊', group)
        # 对用户本地群聊记录进行整合
        res = ""
        mes1 = old_mes.split('\n')
        mes2 = group_channel[group].split('\n')
        i = 0
        j = 0
        while i < len(mes1)-1 and j < len(mes2)-1:
            t1, m1 = mes1[i].split(' ', 1)
            t2, m2 = mes2[j].split(' ', 1)
            # 比较时间戳，较小的排在前
            t1 = float(t1)
            t2 = float(t2)
            if t1 > t2:
                res = res + mes2[j] + '\n'
                j += 1
            elif t1 < t2:
                res = res + mes1[i] + '\n'
                i += 1
            else:
                res = res + mes1[i] + '\n'
                i += 1
                j += 1
        while i < len(mes1)-1:
            res = res + mes1[i] + '\n'
            i+= 1
        while j < len(mes2)-1:
            res = res + mes2[j] + '\n'
            j+= 1
        # 保存整合的消息
        group_channel[group] = res
        return res
    

    # 退出群聊
    def exposed_exitGroup(self, user_name, group):
        print(user_name, '退出群聊', group)
        group_name[group].remove(user_name)
        
    
    # 私聊消息处理
    def exposed_sendPrivateMes(self, user1, user2, mes):
        message[user2] = mes

    # 群聊消息处理
    def exposed_sendGroupMes(self, group, mes):
        group_channel[group] += mes
        for each in group_name[group]:
            message[each] = mes
        
    # 接收消息
    def exposed_getMes(self, user_name):
        if user_name not in message.keys():
            return ""
        else:
            mes =  message[user_name]
            del message[user_name]
            return mes

    
    # 用户注销
    def exposed_logout(self, user_name):
        print('登出用户：', user_name)
        client_name.remove(user_name)
        global client_num
        client_num -= 1

    # 查看聊天群
    def exposed_getGroupList(self):
        mes = "当前共有" + str(group_num) + "个群聊:\n"
        for each in group_name:
            mes = mes + each + '\n'
        return mes

    
client_num  = 0             # 在线用户数
client_name = set({})       # 在线用户集合
private_channel = dict({})  # 暂存的私聊消息：private_channel[(A,B)]=M表示A的本地与B的聊天记录为M
message = dict({})          # 立即发送的消息：message[A]=M表示马上要将M发送给A
group_num = 0               # 聊天群个数
group_name = dict({})       # 聊天群：group_name[A]={B,C}表示B和C正在群聊A中
group_channel = dict({})    # 暂存的群聊消息：group_channel[A]=M表示群聊A的聊天记录为M


# 创建线程开启服务
rpcServer = ThreadedServer(ChatService, port=9999, auto_register=False)  
rpcServer.start()
    
    
