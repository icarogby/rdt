import socket
from threading import Thread

host = socket.gethostbyname(socket.gethostname())
port = 6000 #! Mudar para 5000

# Server socket
serv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # AF_INET = IPV4 | SOCK_DGRAM = UDP
serv.bind((host, port))

def gate():
    global serv

    while True:
        data, addr = serv.recvfrom(1024) # receive data and client address
        print(f"Received data: {data.decode()}")

Thread(target=gate).start()