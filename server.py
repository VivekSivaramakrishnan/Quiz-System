# Python program to implement server side of chat room.
import socket
import select
import sys
# import threading
from _thread import *
import time
import errno
from details import *


def clientthread(client):

    while True:
        try:
            message = get_message(client)

            if message:
                message_to_send = f'<{client.addr[0]}> | Buzzed by {client.house}'
                print(message_to_send)
                # Send name of buzzed house to master client
                client.broadcast()
        except:
            print(f'<{client.addr[0]} | {client.house}> has been removed.')
            remove(client)
            return 0


def get_message(client):

    message = client.socket.recv(64).decode('utf-8')
    if message:
        return message


def house_gen():
    for i in ['Master', 'Scott', 'Shakespeare', 'Newton', 'Nobel']:
        yield i


def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)


class Client:

    def __init__(self, socket, addr, house):
        self.socket = socket
        self.addr = addr
        self.house = house

    def broadcast(self):

        list_of_clients[0].socket.send(self.house.encode('utf-8'))

        for client in list_of_clients[1:]:
            client.socket.send(f'BUZZED by {self.house}'.encode('utf-8'))


if __name__ == '__main__':
    house = house_gen()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    active_connections = 6

    # Binding server to ip and port
    server.bind((ip, port))

    # Listens for 6 connections
    server.listen(active_connections)

    list_of_clients = []

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
