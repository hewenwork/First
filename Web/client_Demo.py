from socket import *

Host = "192.168.2.208"
Port = 8000
Address = (Host, Port)
client = socket(AF_INET, SOCK_STREAM)
client.connect(Address)
while True:
    client.send(b"aa")
    a = client.recv(1024)
    print(a.decode("utf-8"))
