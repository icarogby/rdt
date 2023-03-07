import socket
from threading import Thread

chost = input("Enter ip of network: ")
host = input("Enter your ip: ")
send_ip = input("Enter ip to send: ")
port = 5000

# Server socket
skt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # AF_INET = IPV4 | SOCK_DGRAM = UDP
skt.bind((host, port))

def make_segment(ip,  data):
    return f"{ip}|{data}"

def receive():
    global skt

    while True:
        data, addr = skt.recvfrom(1024) # receive data and client address
        print(f"Received data: {data.decode()}")

def send():
    global skt
    
    while True:
        data = input("Enter data to send: ")
        make_segment(send_ip, data)
        skt.sendto(data.encode(), (chost, port)) # send data to server

Thread(target=receive).start()
Thread(target=send).start()
