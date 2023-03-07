import socket
from threading import Thread

# todo fazer somente socket servidor
host = socket.gethostbyname(socket.gethostname())
port = 5000

serv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # AF_INET = IPV4 | SOCK_DGRAM = UDP
serv.bind((host, port))

clie = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

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

def baguncinha(opc, data, addr):
    addr = (addr[0], 6000) #! Não mudar porta

    if opc == 1:
        clie.sendto(data, addr)
    elif opc == 2:
        pass
    elif opc == 3:
        clie.sendto(data, addr)
        print("dd1")
        clie.sendto(data, addr)
        print("dd2")
    elif opc == 4:
        clie.sendto(data, addr)
        # todo Fazer canal de volta
        # todo apagar
    elif opc == 5:
        #todo alterar numero de seguencia
        pass
    else:
        print("Opção inválida")
    
def gate():
    global serv, clie
    global opc

    while True:
        data, addr = serv.recvfrom(1024) # receive data and client address
        print(addr)

        baguncinha(opc, data, addr)

        print(f"Received data: {data.decode()}")

Thread(target=menu).start()
Thread(target=gate).start()
