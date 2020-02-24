# Python program to implement server side of chat room.
import socket
import select
import sys
# import threading
from _thread import *
import time
import errno
from details import *

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


active_connections = 6

# Binding server to ip and port
server.bind((ip, port))

# Listens for 6 connections
server.listen(active_connections)

list_of_clients = []


def clientthread(client):

    while True:
        message = get_message(client)

        if message:
            message_to_send = f'<{client.addr[0]}> | Buzzed by {client.house}'
            print(message_to_send)
            # Send name of buzzed house to master client
            client.broadcast_to_master()
        else:
            break
    return 0


def get_message(client):

    try:
        message = client.socket.recv(64).decode('utf-8')
        if message:
            return message

    except Exception as e:
        print(f'<{client.addr[0]} | {client.house}> is  removed.')
        remove(client)
        return 0


def house_gen():
    for i in ['Master', 'Scott', 'Shakespeare', 'Newton', 'Nobel']:
        yield i


house = house_gen()


def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)


class Client:

    def __init__(self, socket, addr, house):
        self.socket = socket
        self.addr = addr
        self.house = house

    def broadcast_to_master(self):
        list_of_clients[0].socket.send(self.house.encode('utf-8'))


while True:

    # Accepting a client returns the socket of the client and its address
    soc, add = server.accept()
    client = Client(soc, add, next(house))

    # Consists of all the conected clients
    list_of_clients.append(client)

    # prints the address of the user that just connected
    print(
        f"Connection with <{client.addr[0]} | {client.house}> has been established!")

    # A thread for this user is then created
    # This function is from the threading module
    # threading.Thread(target=clientthread, args=client)
    start_new_thread(clientthread, (client,))
client_socket.close()
server.close()
