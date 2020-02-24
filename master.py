import socket
import sys
from details import *

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


server.connect((ip, port))


def master_client():
    try:
        h = server.recv(64).decode('utf-8')
        print(f'{h} buzzed')
    except:
        print('Closing...')
        sys.exit()
