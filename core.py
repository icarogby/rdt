import socket
from threading import Thread

host = socket.gethostbyname(socket.gethostname())
port = 5000

skt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # AF_INET = IPV4 | SOCK_DGRAM = UDP
skt.bind((host, port))

print(f"Host: {host} | Port: {port}")

opc = 1

def menu():
    global opc

    while True:
        print("Estado atual:")
        print("1 - Reenviar normalmente")
        print("2 - Descartar pacote")
        print("3 - Enviar duplicado")
        print("4 - Apagar ack")
        print("5 - Reenviar com reordenação\n\n")

        opc = int(input("O que deseja fazer com o pacote: "))

def sim(opc, data, addr):
    global skt

    if opc == 1:
        skt.sendto(data, addr)
    elif opc == 2:
        pass
    elif opc == 3:
        skt.sendto(data, addr)
        skt.sendto(data, addr)
    elif opc == 4:
        skt.sendto(data, addr)
        # todo Fazer canal de volta
        # todo apagar
    elif opc == 5:
        #todo alterar numero de seguencia
        pass
    else:
        print("Opção inválida")
    
def gate():
    global skt
    global opc

    while True:
        data, addr = skt.recvfrom(1024) # receive data and client address
        print(addr)

        sim(opc, data, addr)

        print(f": Received data: {data.decode()}")

Thread(target=menu).start()
Thread(target=gate).start()
