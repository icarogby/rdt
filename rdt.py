from socket import socket, AF_INET, SOCK_DGRAM
from threading import Thread
from time import time
import logging

logging.basicConfig(filename='rdt.log', filemode='w', level = 'DEBUG', format='%(name)s - %(levelname)s - %(message)s')

TIME_OUT = 2

class Sender():
    def __init__(self, senderAddress: tuple, log = False):
        self.serialNumber = 0
        self.isListening = False
        self.rightAck = False
        self.log = log

        self.skt = socket(AF_INET, SOCK_DGRAM) # AF_INET = IPV4 | SOCK_DGRAM = UDP
        self.skt.bind(senderAddress)

        self.thread = Thread(target=self.receive)
        self.thread.start()

    def receive(self):
        while True:
            receivedAck, _ = self.skt.recvfrom(1024)

            if self.isListening:
                if receivedAck == bytes([self.serialNumber]):
                    self.rightAck = True
                else:
                    if self.log: logging.debug("Received wrong ack. Ignoring...") # todo: take out

    def send(self, dataInBytes: bytes, receiverAddress: tuple):
        for i in range(0, len(dataInBytes), 16):
            segmentedData = dataInBytes[i:i+16]
            
            segmentedData = bytes([self.serialNumber]) + segmentedData

            segmentSize = len(segmentedData) + 2 + 1
            segmentedData = bytes([segmentSize]) + segmentedData

            # Calculating checksum.
            sum = 0

            for byteInInt in segmentedData:
                sum += byteInInt
            
            checkSum = ~sum

            checkSunInTwoBytes = bin(checkSum)[3:].zfill(16)

            checkSunByte1 = checkSunInTwoBytes[0:8]
            checkSunByte2 = checkSunInTwoBytes[8:16]
            
            segmentedData = bytes([int(checkSunByte1, 2), int(checkSunByte2, 2)]) + segmentedData

            # Sending segment.
            self.skt.sendto(segmentedData, receiverAddress)
            
            # Waiting for ack.
            self.isListening = True
            
            start = time()

            while True:
                end = time()

                if (end - start) > TIME_OUT:
                    if self.log: logging.debug("Timeout! Resending segment...")
                    
                    # Resending segment.
                    self.skt.sendto(segmentedData, receiverAddress)
                    
                    start = time()
                else:
                    if self.rightAck:
                        if self.log: logging.debug("Received ack. Moving on...")
                        
                        self.rightAck = False
                        self.isListening = False

                        break
            
            # Update serial number.
            self.serialNumber = 1 - self.serialNumber

class Receiver():
    def __init__(self, receiverAddress: tuple):
        self.ack = 0
        self.buffer = b""

        self.skt = socket(AF_INET, SOCK_DGRAM) # AF_INET = IPV4 | SOCK_DGRAM = UDP
        self.skt.bind(receiverAddress)

    def receive(self):
        receivedData, senderAddress = self.skt.recvfrom(1024)
        receivedData = self.buffer + receivedData

        for b in receivedData:
            print(f"{b} ")

        print("----------------")

        try:
            checkSumByte1 = receivedData[0]
            checkSumByte2 = receivedData[1]

            segmentSize = receivedData[2]

            serialNumber = receivedData[3]

            segmentData = receivedData[4:segmentSize]

            self.buffer = receivedData[segmentSize:]
        except:
            print("1. Data receive is corrupted. ignoring\n") # todo: to log
            return None
        
        try:
            checkSumByte1 = bin(checkSumByte1)[2:].zfill(8)
            checkSumByte2 = bin(checkSumByte2)[2:].zfill(8)
            checkSum = checkSumByte1 + checkSumByte2
            print(f"checkSum: {checkSum}") # todo: to log
            checkSum = int(checkSum, 2)

            sum = 0

            for byteInInt in receivedData[2:segmentSize]:
                sum += byteInInt

            print(sum)

            if (sum - checkSum) == -1:
                print(f"Received data: {segmentData}\n") # todo: to log

                if self.ack == serialNumber:
                    print("Sending ack...")
                    self.skt.sendto(bytes([self.ack]), senderAddress)
                    self.ack = 1 - self.ack
                else:
                    print("Received wrong segment. Ignoring...")
                    # todo: test self.skt.sendto(bytes([1 - self.ack]), senderAddress)
            else:
                print("Data receive is corrupted. ignoring\n")
        except:
            print("Data receive is corrupted. ignoring\n")
            return None

        return segmentData
