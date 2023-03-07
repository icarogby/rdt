import socket
from threading import Thread

host = socket.gethostbyname(socket.gethostname())
port = 5000

# Client socket
clie = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def send():
    global clie
    
    while True:
        data = input("Enter data to send: ")
        clie.sendto(data.encode(), (host, port)) # send data to server

Thread(target=send).start()
