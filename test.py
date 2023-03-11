from socket import socket, AF_INET, SOCK_DGRAM, gethostbyname, gethostname

my_ip = gethostbyname(gethostname()) 
port = 7000

skt = socket(AF_INET, SOCK_DGRAM) # AF_INET = IPV4 | SOCK_DGRAM = UDP

while True:
    msg = input("Enter msg: ")
    skt.sendto(msg.encode("utf-8"), (my_ip, 5000))
