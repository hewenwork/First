import socket
import pyperclip
result = socket.gethostbyname(socket.getfqdn(socket.gethostname()))
result = "IP地址:%s\n端口: 5900\nVNC密码:123" % result
print(result)
pyperclip.copy(result)
