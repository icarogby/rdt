import socket
from threading import Thread
from time import sleep
from rdt import Sender

x = Sender((23132, 12))

x.send("oi")

host = socket.gethostbyname(socket.gethostname())
port = 6000 # todo change to 5000 port

skt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # AF_INET = IPV4 | SOCK_DGRAM = UDP
skt.bind((host, port))

print(f"Host: {host} | Port: {port}")

opc = 1

def menu():
    global opc

    while True:
        print(f"\nCurrent state: {opc}\n")
        print("1 - Reenviar seguimento normalmente")
        print("2 - Descartar sequimento")
        print("3 - Apagar ack")
        print("4 - Enviar ack com atraso")
        print("5 - trocar ack")
        print("6 - Enviar ack qd ñ estiver escutando")
        print("7 - Mudar checksum")
        print("8 - Send not a segment")

        temp = int(input("\nO que deseja fazer com o sequimento? "))

        if temp == 6:
            skt.sendto("ack0".encode("utf-8"), (host, 5000)) # todo: change to 5000 port
            opc = 1
        elif temp == 8:
            skt.sendto("not a segment".encode("utf-8"), (host, 7000)) # todo: change to 5000 port
            opc = 1
        else:
            opc = temp
    
def core():
    global skt
    global opc

    while True:
        data, addr = skt.recvfrom(1024) # receive data and client address

        print(f"Received data: {data.decode()}")

        if data.decode("utf-8") == "ack0" or data.decode("utf-8") == "ack1":
            if opc == 1:
                skt.sendto(data, (host, 5000))
            elif opc == 2:
                skt.sendto(data, (host, 5000))
            elif opc == 3:
                pass
            elif opc == 4:
                sleep(1.5)
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
            elif opc == 7:
                data = data.decode("utf-8")

                check_sum, addressee_ip, serial_number_with_data = data.split("|")
                check_sum = int(check_sum[4:]) - 10
                data = f"{check_sum}|{addressee_ip}|{serial_number_with_data}"
                
                print(f"New data: {data}")

                skt.sendto(data.encode("utf-8"), (host, 7000))

Thread(target=menu).start()
Thread(target=core).start()
