from socket import socket, AF_INET, SOCK_DGRAM, gethostbyname, gethostname
from time import sleep
from threading import Thread, Lock

core_ip = gethostbyname(gethostname()) # todo change to input("Enter ip of network: ")
my_ip = gethostbyname(gethostname()) # todo change to get a input 
addressee_ip = input("Enter ip of addressee: ")

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
        data = input("Enter data to send: ")
        make_segments(addressee_ip, skt, data)

def make_checksum(segment: str) -> int:
        sum = 0

        print("Creating Checksum...\n\n")

        segment = bin(int.from_bytes(segment.encode("utf-8"), "big"))[2:] # convert string to binary
        print(f"Segment in binary: {segment}")
        
        size = len(segment)

        for i in range(0, size, 16):
            print(f"parts of 16bits: {segment[i: i+16]} | this same part in integer: {int(segment[i: i+16], 2)}")
            sum += int(segment[i: i+16], 2)

        print(f"Sum of all parts: {sum}")
        print(f"Checksum of the segment: {~sum}")

        return ~sum

def make_segments(addressee_addr: str,  skt: socket, data: str) -> None:
    global serial_number, ack, listening

    for i in range(0, len(data), 1024):
        segment_data = data[i:i+1024]
        segment = f"{addressee_addr}|{serial_number}{segment_data}"

        check_sum = make_checksum(segment)

        segment = f"{check_sum}_{addressee_addr}|{serial_number}{segment_data}"

        print(f"Sending segment: {segment}")
        skt.sendto(segment.encode("utf-8"), (core_ip, 6000)) # todo change to 5000 port

        while True:
            listening = True #? Change here
            sleep(1)

            with critical:
                if ack:
                    ack = False
                    listening = False #? Change here
                    break
                else:
                    skt.sendto(segment.encode("utf-8"), (core_ip, 6000)) # todo change to 5000 port

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
                    print("Received rick ack(1)")
                    ack = True
            else:
                print("Received wrong ack. Ignoring...")

Thread(target=receive).start()
Thread(target=send).start()
