from socket import socket, AF_INET, SOCK_DGRAM, gethostbyname, gethostname
from time import time

# def receive():
#     global skt, ack, listening

#     while True:
#         data, addr = skt.recvfrom(1024) # receive data and client address
#         data = data.decode("utf-8")

#         if not listening: #? Change here
#             print("Received data. Ignoring...")
#         else:
#             if data == "ack0" and serial_number == 0: #? change here
#                     print("Received right ack (0)")
#                     ack = True
#             elif data == "ack1" and serial_number == 1: #? change here
#                 with critical:
#                     print("Received right ack (1)")
#                     ack = True
#             else:
#                 print("Received wrong ack. Ignoring...")

class Sender():
    def __init__(self, senderAddress: tuple, receiverAddress: tuple) -> None:
        self.receiverAddress = receiverAddress

        self.serialNumber = 0
        self.isListening = False
        self.ack = False

        self.skt = socket(AF_INET, SOCK_DGRAM) # AF_INET = IPV4 | SOCK_DGRAM = UDP
        self.skt.bind(senderAddress)

    def send(self, dataInBytes: bytes):
        for i in range(0, len(dataInBytes), 16):
            segmentedData = dataInBytes[i:i+16]
            
            segmentedData = bytes([self.serialNumber]) + segmentedData

            segmentSize = len(segmentedData)
            segmentedData = bytes([segmentSize]) + segmentedData

            sum = 0

            for byteInInt in segmentedData:
                sum += byteInInt
            
            checkSum = ~sum

            checkSunIn2Bytes = bin(checkSum)[3:].zfill(16)
            byte1 = checkSunIn2Bytes[0:8]
            byte2 = checkSunIn2Bytes[8:16]
            
            segmentedData = bytes([int(byte1, 2), int(byte2, 2)]) + segmentedData

            self.skt.sendto(segmentedData, self.receiverAddress)
            
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

            # if (serial_number == 0):
            #     serial_number = 1
            # else:
            #     serial_number = 0
