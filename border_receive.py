from socket import socket, AF_INET, SOCK_DGRAM, gethostbyname, gethostname
from time import sleep
from threading import Thread, Lock

my_ip = gethostbyname(gethostname()) # todo change to get a input or gambiarra

skt = socket(AF_INET, SOCK_DGRAM) # AF_INET = IPV4 | SOCK_DGRAM = UDP
skt.bind((my_ip, 7000)) # todo change to 5000 port

ack_number = 0

def make_sum(segment: str) -> int:
    sum = 0

    segment = bin(int.from_bytes(segment.encode("utf-8"), "big"))[2:] # convert string to binary string
    size = len(segment)

    for i in range(0, size, 16):
        print(f"See word: {segment[i: i+16]}")
        sum += int(segment[i: i+16], 2)

    return sum

def receive():
    global skt, ack_number

    while True:
        data, addr = skt.recvfrom(1024) # receive data and client address
        data = data.decode("utf-8")
        
        print(data) #* debug

        check_sum, data_no_cs = data.split("\\")
        check_sum = int(check_sum)
        ip, serial_number = data_no_cs.split("|")

        if int(serial_number[0]) == ack_number:
            skt.sendto(f"ack{ack_number}".encode("utf-8"), (my_ip, 6000))

            sum = make_sum(data_no_cs)
            print(f"sum: {sum} | check_sum: {check_sum} | sum + check_sum: {sum + check_sum}")

            if (check_sum + sum) == -1:
                print("no loose")

            if ack_number == 0:
                ack_number = 1
            else:
                ack_number = 0
        else:
            skt.sendto(f"ack{int(serial_number[0])}".encode("utf-8"), (my_ip, 6000))
            print("Received wrong ack. Pkg deleted")

Thread(target=receive).start()
