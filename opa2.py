from rdt import Reciever
from socket import gethostbyname, gethostname

receiver = Reciever((gethostbyname(gethostname()), 7000))

while True:
    msg = receiver.receive()

    if msg == None:
        continue
    else:
        print(msg)

