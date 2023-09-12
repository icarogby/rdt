from rdt import Sender
from socket import gethostbyname, gethostname

x = Sender((gethostbyname(gethostname()), 5000), (gethostbyname(gethostname()), 5001))

while True:
    x.send(input("Enter data: ").encode("utf-8"))