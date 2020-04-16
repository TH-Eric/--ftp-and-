"""
chat room 客户端

功能：发送请求 返回结果

引用进程：
"""

from socket import *
from multiprocessing import Process
import sys

# 服务器地址

ADDR = ("127.0.0.1", 8001)


# 子进程接收消息(所有的客户端都在这里接收消息)
def recv_msg(s):
    while True:
        data, addr = s.recvfrom(4096)
        print(data.decode() + "\n发言:", end="")  # 打印接收内容


# 父进程发送消息（所有客户端都在这里发送消息）
def send_msg(s, name):
    while True:
        try:
            text = input("请您发言：")
        except KeyboardInterrupt:
            text = "quit"
        if text == "quit":
            msg = "Q" + name
            s.sendto(msg.encode(), ADDR)
            sys.exit("退出聊天室！")
        msg = "C %s %s" % (name, text)
        # 把姓名传过去后续方便区分
        s.sendto(msg.encode(), ADDR)


# 定义网络结构
def main():
    # 创建套接字
    s = socket(AF_INET, SOCK_DGRAM)

    # 进入聊天室
    while True:
        name = input("请输入你的姓名：")
        # 定协议
        msg = "L " + name

        # 发送服务端
        s.sendto(msg.encode(), ADDR)
        # 接收服务端请求
        data, addr = s.recvfrom(128)
        if data.decode() == "OK":  # 如果服务端能让我进入聊天室 就发送OK,表示可以进入聊天室
            print("您已经进入聊天室！")
            break
        else:
            print(data.decode())  # 如果服务端能让我进入聊天室,说明该用户已经存在
    # 创建一个新的进程
    p = Process(target=recv_msg, args=(s,))
    # 子进程接收消息（因为子进程不能输入）,参数需要套接字
    p.daemon = True
    p.start()
    # 父进程发送消息
    send_msg(s, name)


if __name__ == '__main__':
    main()
