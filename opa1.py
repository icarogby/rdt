from rdt import Sender
from socket import gethostbyname, gethostname

sender = Sender((gethostbyname(gethostname()), 5000))

while True:
    msg = input("Type a message: ")
    sender.send(msg.encode("utf-8"), (gethostbyname(gethostname()), 7000))
