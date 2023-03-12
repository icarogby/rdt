import socket
from threading import Thread
from time import sleep

host = socket.gethostbyname(socket.gethostname())
port = 6000 # todo change to 5000 port

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
        print("3 - Apagar ack")
        print("4 - Enviar ack com atraso")
        print("5 - trocar ack") #? change here
        print("6 - Enviar ack qd ñ estiver escutando")

        temp = int(input("O que deseja fazer com o pacote: "))

        if temp == 6:
            skt.sendto("ack0".encode("utf-8"), (host, 5000))
            opc = 1
        else:
            opc = temp
    
def core():
    global skt
    global opc

    while True:
        data, addr = skt.recvfrom(1024) # receive data and client address

        if data.decode("utf-8") == "ack0" or data.decode("utf-8") == "ack1":
            if opc == 1:
                skt.sendto(data, (host, 5000))
            elif opc == 2:
                skt.sendto(data, (host, 5000))
            elif opc == 3:
                pass
            elif opc == 4:
                sleep(2)
                skt.sendto(data, (host, 5000))
            elif opc == 5: #? change here
                if data.decode("utf-8") == "ack0":
                    skt.sendto("ack1".encode("utf-8"), (host, 5000))
                else:
                    skt.sendto("ack0".encode("utf-8"), (host, 5000))
            else:
                print("Opção inválida")
        else:
            if opc == 1:
                skt.sendto(data, (host, 7000))
            elif opc == 2:
                pass
            elif opc == 3:
                skt.sendto(data, (host, 7000))
            elif opc == 4:
                skt.sendto(data, (host, 7000))
            elif opc == 5:
                skt.sendto(data, (host, 7000))

        print(f": Received data: {data.decode()}")

Thread(target=menu).start()
Thread(target=core).start()
