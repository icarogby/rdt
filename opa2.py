from rdt import Receiver
from socket import gethostbyname, gethostname

receiver = Receiver((gethostbyname(gethostname()), 7000))

while True:
    msg = receiver.receive()

    if msg == None:
        continue
    else:
        print(msg)

