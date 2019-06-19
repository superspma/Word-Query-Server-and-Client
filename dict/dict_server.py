"""
dict_server服务端
功能 业务逻辑处理
模型 多进程 tcp 并发

"""
from socket import *
from multiprocessing import Process
import signal, sys
from operation_db import *

# 全局变量
HOST = "0.0.0.0"
PORT = 8991
ADDR = (HOST, PORT)

# 数据库对象
db = Database()


# 注册请求
def do_register(c, data):
    tmp = data.split(" ")
    name = tmp[1]
    passwd = tmp[2]
    if db.register(name, passwd):
        c.send(b"OK")
    else:
        c.send(b"Fail")


# 登录处理
def do_login(c, data):
    tmp = data.split(" ")
    name = tmp[1]
    passwd = tmp[2]
    if db.do_login(name, passwd):
        c.send(b"OK")
    else:
        c.send(b"Fail")


# 接收客户端请求,分配处理函数
def request(c):
    db.create_cursor()  # 生成游标
    while True:
        data = c.recv(1024).decode()
        if not data or data[0]=="E":
            sys.exit()
        elif data[0] == "R":
            do_register(c, data)
        elif data[0] == "L":
            do_login(c, data)

        print(c.getpeername(), ":", data)


# 搭建网络
def main():
    s = socket()
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind(ADDR)
    s.listen(5)

    # 处理僵尸进程
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)

    # 循环等待客户端连接
    print("Listen the port", PORT)
    while True:
        try:
            c, addr = s.accept()
            print("Connect from", addr)
        except KeyboardInterrupt:
            s.close()
            db.close()
            sys.exit("服务端退出")
        except Exception as e:
            print(e)
            continue

        # 为客户端创建子进程
        p = Process(target=request, args=(c,))
        p.daemon = True
        p.start()


if __name__ == '__main__':
    main()
