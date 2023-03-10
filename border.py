import socket
from threading import Thread, Lock
from time import sleep

net_ip = socket.gethostbyname(socket.gethostname()) # todo change to input("Enter ip of network: ")
my_ip = socket.gethostbyname(socket.gethostname()) # todo change to get a input or gambiarra
addressee_ip = input("Enter ip of addressee: ")

serial_number = 0

critical = Lock()

with critical:
    ack = False

skt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # AF_INET = IPV4 | SOCK_DGRAM = UDP
skt.bind((my_ip, 6000)) # todo change to 5000 port

def send_in_segments(addressee_addr: str,  skt: socket.socket, data: str) -> None:
    global serial_number, ack

    for i in range(0, len(data), 1024):
        segment_data = data[i:i+1024]
        segment = f"{addressee_addr}|{serial_number}{segment_data}"

        if serial_number == 0:
            serial_number = 1
        else:
            serial_number = 0

        skt.sendto(segment.encode("utf-8"), (net_ip, 5000))

        while True:
            sleep(1)

            with critical:
                if ack:
                    print("Received ack")
                    ack = False
                    
                    break
                else:
                    skt.sendto(segment.encode("utf-8"), (net_ip, 5000))

def receive():
    global skt, ack

    while True:
        data, addr = skt.recvfrom(1024) # receive data and client address
        
        if data == "ack":          
            with critical:
                print("Received ack")
                ack = True
        
        print(f"Received data: {data.decode()}")

def send():
    global skt
    
    while True:
        data = input("Enter data to send: ")
        send_in_segments(addressee_ip, skt, data)

Thread(target=receive).start()
Thread(target=send).start()
