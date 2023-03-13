from socket import socket, AF_INET, SOCK_DGRAM, gethostbyname, gethostname
from time import time
from threading import Thread, Lock

core_ip = gethostbyname(gethostname()) # todo: change to get a input
my_ip = gethostbyname(gethostname()) # todo: change to get a input
addressee_ip = input("\nEnter ip of addressee: ")

serial_number = 0
listening = False #? Change here

critical = Lock()
with critical:
    ack = False

skt = socket(AF_INET, SOCK_DGRAM) # AF_INET = IPV4 | SOCK_DGRAM = UDP
skt.bind((my_ip, 5000))

def send():
    global skt, listening
    
    while True:
        data = input("\nEnter data to send: ")
        make_segments(addressee_ip, skt, data)

def make_checksum(segment: str) -> int:
        sum = 0

        segment = bin(int.from_bytes(segment.encode("utf-8"), "big"))[2:] # convert string to binary
        size = len(segment)

        for i in range(0, size, 16):
            sum += int(segment[i: i+16], 2)

        return ~sum

def make_segments(addressee_ip: str,  skt: socket, data: str) -> None:
    global serial_number, ack, listening

    for i in range(0, len(data), 20):
        segment_data = data[i:i+20]

        # Making Header
        segment_without_checksum = f"{addressee_ip}|{serial_number}{segment_data}"

        # Making checksum
        check_sum = make_checksum(segment_without_checksum) #? Change here
        segment = f"{check_sum}|{addressee_ip}|{serial_number}{segment_data}" #? Change here

        # Making segment size
        segment_size = len(segment) + 4 #? Change here
        segment_size = str(segment_size).zfill(4)
        segment = f"{segment_size}{check_sum}|{addressee_ip}|{serial_number}{segment_data}"

        print(f"\nSending this segment:\n\tSeg size:{segment_size}\n\tChecksum: {check_sum}\n\tAddressee IP: {addressee_ip}\n\tSerial number: {serial_number}\n\tSegment data: {segment_data}\n")
        print("Waiting for right ack...")

        skt.sendto(segment.encode("utf-8"), (core_ip, 6000)) # todo: change to 5000 port
        
        start = time()
        while True:
            listening = True #? Change here
            
            end = time()
            if end - start > 1:
                print("Timeout! Resending segment...")
                skt.sendto(segment.encode("utf-8"), (core_ip, 6000)) # todo: change to 5000 port
                start = time()
            else:
                with critical:
                    if ack:
                        ack = False
                        listening = False #? Change here
                        break

        if serial_number == 0:
            serial_number = 1
        else:
            serial_number = 0

def receive():
    global skt, ack, listening

    while True:
        data, addr = skt.recvfrom(1024) # receive data and client address
        data = data.decode("utf-8")

        if not listening: #? Change here
            print("Received data. Ignoring...")
        else:
            if data == "ack0" and serial_number == 0: #? change here
                    print("Received right ack (0)")
                    ack = True
            elif data == "ack1" and serial_number == 1: #? change here
                with critical:
                    print("Received right ack (1)")
                    ack = True
            else:
                print("Received wrong ack. Ignoring...")

Thread(target=receive).start()
Thread(target=send).start()
