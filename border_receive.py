from socket import socket, AF_INET, SOCK_DGRAM, gethostbyname, gethostname
from threading import Thread

my_ip = gethostbyname(gethostname()) # todo: change to get a input

skt = socket(AF_INET, SOCK_DGRAM) # AF_INET = IPV4 | SOCK_DGRAM = UDP
skt.bind((my_ip, 7000)) # todo: change to 5000 port

ack_number = 0

def make_sum(segment: str) -> int:
    sum = 0

    segment = bin(int.from_bytes(segment.encode("utf-8"), "big"))[2:] # convert string to binary string
    size = len(segment)

    for i in range(0, size, 16):
        sum += int(segment[i: i+16], 2)

    return sum

def receive():
    global skt, ack_number

    while True:
        print("Waiting for data...")
        data, addr = skt.recvfrom(1024) # receive data and client address
        data = data.decode("utf-8")

        print(f"Data receive: {data}\n") #* debug

        check_sum, addressee_ip, serial_number_with_data = data.split("|") #? Change here
        check_sum = int(check_sum)

        serial_number = int(serial_number_with_data[0])

        sum = make_sum(f"{addressee_ip}|{serial_number_with_data}") #? Change here
        print(f"sum: {sum} | check_sum: {check_sum} | sum + check_sum: {sum + check_sum}") #* debug
    
        if (check_sum + sum) == -1: #? Change here
            print("Checksum ok. No loose.\n")

            if int(serial_number) == ack_number:
                print("Received pkg with right serial number. Sending ack.")
                print(f"Message: {serial_number_with_data[1:]}\n")
                skt.sendto(f"ack{ack_number}".encode("utf-8"), (my_ip, 6000)) # todo: change to 5000 port

                if ack_number == 0:
                    ack_number = 1
                else:
                    ack_number = 0
            else:
                print("Received pkg with wrong ack and deleting this pkg. Resending previous ack.")
                skt.sendto(f"ack{serial_number}".encode("utf-8"), (my_ip, 6000))
        else:
            print("Checksum fail! Not sending ack\n")

Thread(target=receive).start()
