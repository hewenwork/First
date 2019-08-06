from socket import *

# Address
Host = gethostbyname(gethostname())
Port = 8000

# Config socket
# socket.socket()创建一个socket对象，并说明socket使用的是IPv4(AF_INET，IP version 4)和TCP协议(SOCK_STREAM)
sock = socket(AF_INET, SOCK_STREAM)
# 绑定服务器host和端口
sock.bind((Host, Port))
# 最多监听3个链接
sock.listen(3)
while True:

    # 接收建立连接
    con, addr = sock.accept()
    # 接受信息
    request = con.recv(1024)

    # 发送信息
    con.send(b"Hello")
    print(request)