from socket import gethostbyname, gethostname, socket, AF_INET, SOCK_DGRAM

skt = socket(AF_INET, SOCK_DGRAM)
skt.bind((gethostbyname(gethostname()), 5001))

while True:
    data, addr = skt.recvfrom(1024)
    
    data = data[4:]
    print(data.decode("utf-8"))
