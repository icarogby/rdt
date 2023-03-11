from socket import socket, AF_INET, SOCK_DGRAM, gethostbyname, gethostname
from time import sleep
from threading import Thread, Lock

core_ip = gethostbyname(gethostname()) # todo change to input("Enter ip of network: ")
my_ip = gethostbyname(gethostname()) # todo change to get a input or gambiarra
addressee_ip = input("Enter ip of addressee: ")

serial_number = 0

critical = Lock()
with critical:
    ack = False

skt = socket(AF_INET, SOCK_DGRAM) # AF_INET = IPV4 | SOCK_DGRAM = UDP
skt.bind((my_ip, 5000))

def send():
    global skt
    
    while True:
        data = input("Enter data to send: ")
        make_segments(addressee_ip, skt, data)

def make_segments(addressee_addr: str,  skt: socket, data: str) -> None:
    global serial_number, ack

    for i in range(0, len(data), 1024):
        segment_data = data[i:i+1024]
        segment = f"{addressee_addr}|{serial_number}{segment_data}"

        skt.sendto(segment.encode("utf-8"), (core_ip, 6000)) # todo change to 5000 port

        while True:
            sleep(1)

            with critical:
                if ack:
                    print("Received ack")
                    ack = False
                    
                    break
                else:
                    skt.sendto(segment.encode("utf-8"), (core_ip, 6000)) # todo change to 5000 port

        if serial_number == 0:
            serial_number = 1
        else:
            serial_number = 0

def receive():
    global skt, ack

    while True:
        data, addr = skt.recvfrom(1024) # receive data and client address
        data = data.decode("utf-8")

        if data == "ack0":
            with critical:
                print("Received right ack")
                ack = True
        elif data == "ack1":
            with critical:
                print("Received rick ack")
                ack = True
        else:
            print("error")

Thread(target=receive).start()
Thread(target=send).start()
