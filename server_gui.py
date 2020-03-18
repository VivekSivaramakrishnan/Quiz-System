import tkinter as tk
from PIL import ImageTk, Image
import qrcode
# Python program to implement server side of chat room.
import socket
import select
import sys
# import threading
from _thread import *
import time
import errno
from details import *
# from server import *
###############################


def clientthread(client):

    while True:
        try:
            message = get_message(client)

            if message:
                logger(f'<{client.addr[0]}> | Buzzed by {client.house}')
                client.broadcast()
                # For now its a sleep
                # Ideally the quiz master will control when the next wuestion is shown
                time.sleep(2)
                logger('Next question')
                client.broadcast()
                # Send name of buzzed house to master client

        except:
            logger(f'<{client.addr[0]} | {client.house}> has been removed.')
            remove(client)
            return 0


def get_message(client):

    message = client.socket.recv(64).decode('utf-8')
    if message:
        return message


def logger(text):
    tk.Label(log, text=text).pack()


houses = ['Master', 'Scott', 'Shakespeare', 'Newton', 'Nobel']


def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)
###############################


class Client:

    def __init__(self, socket, addr, house):
        self.socket = socket
        self.addr = addr
        self.house = house

    def broadcast(self):

        list_of_clients[0].socket.send(self.house.encode('utf-8'))

        for client in list_of_clients[1:]:
            client.socket.send(f'BUZZED by {self.house}'.encode('utf-8'))


root = tk.Tk()

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)


introframe = tk.Frame(root)
introframe.grid_rowconfigure(3, weight=1)
introframe.grid_columnconfigure(3, weight=1)

serverframe = tk.Frame(root)
serverframe.grid_rowconfigure(3, weight=1)
serverframe.grid_columnconfigure(3, weight=1)

list_of_clients = []


def start_server():

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    active_connections = 6

    color = {'Master': '111',
             'Scott': '100',
             'Shakespeare': '001',
             'Newton': '110',
             'Nobel': '011'}
    logger('Connecting')
    server.bind((ip, port))
    logger('Connected')
    server.listen(active_connections)

    serverframe.tkraise()

    def accept(bleh):
        for i in range(5):
            img = ImageTk.PhotoImage(qrcode.make(
                f'{ip} {port} {color[houses[i]]}'))
            label = tk.Label(serverframe, image=img)
            label.grid(row=1, column=3, rowspan=2, columnspan=3)

            # Accepting a client returns the socket of the client and its address
            soc, add = server.accept()
            client = Client(soc, add, houses[i])

            # Consists of all the conected clients
            list_of_clients.append(client)

            # loggers the address of the user that just connected
            tk.Label(
                log, text=f"Connection with <{client.addr[0]} | {client.house}> has been established!").pack()
            start_new_thread(clientthread, (client,))

        return 1

    start_new_thread(accept, ('bleh',))


button = tk.Button(introframe, text='Start Server', command=start_server)
button.grid(row=2, column=2)

introframe.grid(row=0, column=0, sticky="nsew")

log = tk.LabelFrame(serverframe, text='Server Log')
log.grid(row=1, column=1, rowspan=2, columnspan=2, sticky='nsew')

serverframe.grid(row=0, column=0, sticky="nsew")


introframe.tkraise()


root.mainloop()
