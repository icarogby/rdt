from socket import socket, AF_INET, SOCK_DGRAM, gethostbyname, gethostname
from time import time
from threading import Thread, Lock

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

def make_checksum(segment: str) -> int:
        sum = 0

        segment = bin(int.from_bytes(segment.encode("utf-8"), "big"))[2:] # convert string to binary
        size = len(segment)

        for i in range(0, size, 16):
            sum += int(segment[i: i+16], 2)

        return ~sum

def sendInSegments(addressee_ip: str,  skt: socket, dataInBits: str) -> None: # todo mudar para enviar bytes
    for i in range(0, len(dataInBits), 20):
        segmentData = dataInBits[i:i+20]

        # # Making Header
        # segment_without_checksum = f"{addressee_ip}|{serial_number}{segmentData}"

        # # Making checksum
        # check_sum = make_checksum(segment_without_checksum) #? Change here
        # segment = f"{check_sum}|{addressee_ip}|{serial_number}{segmentData}" #? Change here

        # # Making segment size
        # segment_size = len(segment) + 4 #? Change here
        # segment_size = str(segment_size).zfill(4)
        # segment = f"{segment_size}{check_sum}|{addressee_ip}|{serial_number}{segmentData}"

        # print(f"\nSending this segment:\n\tSeg size:{segment_size}\n\tChecksum: {check_sum}\n\tAddressee IP: {addressee_ip}\n\tSerial number: {serial_number}\n\tSegment data: {segment_data}\n")
        # print("Waiting for right ack...")

        skt.sendto(segment.encode("utf-8"), (core_ip, 6000)) # todo: change to 5000 port
        
        # start = time()
        # while True:
        #     listening = True #? Change here
            
        #     end = time()
        #     if end - start > 1:
        #         print("Timeout! Resending segment...")
        #         skt.sendto(segment.encode("utf-8"), (core_ip, 6000)) # todo: change to 5000 port
        #         start = time()
        #     else:
        #         if ack:
        #             ack = False
        #             listening = False #? Change here
        #             break

        # if serial_number == 0:
        #     serial_number = 1
        # else:
        #     serial_number = 0

class Sender():
    # Opening socket
    hostIP = gethostbyname(gethostname())
    hostPort = 9998 

    skt = socket(AF_INET, SOCK_DGRAM) # AF_INET = IPV4 | SOCK_DGRAM = UDP
    skt.bind((hostIP, hostPort))

    serialNumber = 0
    isListening = False

    # Initialize sender with recipient address
    def __init__(self, addresseeIP, addresseePort = 9998) -> None:
        ''' sddfsdfs ''' # todo fazer docstring
        self.addresseeIP = addresseeIP
        self.addresseePort = addresseePort

        Thread(target=receive).start()

    # critical = Lock() # todo ??
    # with critical:
    #     ack = False

    def send(self):
        while True:
            data = input("\nEnter data to send: ")
            sendInSegments(self.addresseeIP, self.skt, data)
