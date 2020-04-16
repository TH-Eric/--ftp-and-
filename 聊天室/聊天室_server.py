"""
chat room
env:python3.6
socket udp and process

"""

# 创建连接地址(定义全局变量)
import socket
from multiprocessing import Process



HOST = "0.0.0.0"
PORT = 8001
ADDR = (HOST, PORT)

# 用于存储信息
user = {}


# 判断用户并且存储用户信息的函数
def do_login(s, name, address):
    # 判断用户是否存在
    if name in user or "管理" in name:
        s.sendto("该用户存在".encode(), address)
        return
    else:
        s.sendto(b"OK", address)
        msg = "\n欢迎 %s 进入聊天室" % name
        for i in user:  # 遍历字典得到字典中的建
            # 把该消息发送给所有人------>>>通过用户的地址
            s.sendto(msg.encode(), user[i])
        user[name] = address  # 在字典中增加一项



# 处理聊天
def do_chat(s, name, text):
    msg = "\n%s : %s"%(name,text)
    for i in user:
    # 发送消息（除去他本人）
        if i != name:
            s.sendto(msg.encode(), user[i])


# 处理退出
def do_quit(s,name):
    del user[name] # 删除用户
    msg = "\n%s 退出聊天室"%name
    for i in user:
        s.sendto(msg.encode(),user[i])


# 在这里建立 总>>>>>>分 的结构
def request(s):
    # 因为接收请求是源源不断的接收请求,所以在次就用while True
    while True:
        data, addr = s.recvfrom(1024)
        # 得到的temp就是一个列表 取的第一个就是列表的第一项
        temp = data.decode().split(" ", 2)
        # split(" ", 2)只能切割前面的两项

        if temp[0] == "L":
            # tmp -------->>>["L","name"]
            do_login(s,temp[1],addr)
            # 创建函数(需要套接字,用户姓名,地址)

        elif temp[0] == "C":
            # tmp -------->>>["C","name",text]
            do_chat(s,temp[1],temp[2])

        # 处理退出
        elif temp[0] == "Q":
            # tmp -------->>>["Q","name"]
            do_quit(s,temp[1])

# 发送管理员消息
def manager(s):
    while True:
        msg = input("管理员消息:")
        msg = "C 管理员 "+ msg
        s.sendto(msg.encode(), ADDR) #自己的地址

# 搭建基本架构
def main():
    # 创建一个udp的套接字
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(ADDR)
    # 创建一个接收请求的函数
    # 创建新的进程用于给客户端发送管理员消息
    p = Process(target=request, args=(s,))
    p.start()

    manager(s)  # 处理发来的请求(父进程)

    p.join()


if __name__ == '__main__':
    main()
