# Python program to implement client side of chat room.
import socket
import sys
import details

from server import get_message

import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen


def page_to_screen(page, name):
    screen = Screen(name=name)
    screen.add_widget(page)
    return screen


class Main(App):

    def build(self):
        return sm


class Server():

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip = details.ip
    port = str(details.port)


class Intro(GridLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.padding = [150, 150, 150, 150]

        self.add_widget(Label(text='Welcome to the quiz program!'))
        self.add_widget(Label(
            text='Before proceeding make sure to be connected to the network of the server'))
        self.add_widget(Button(text='Continue', on_press=self.proceed))

    def proceed(self, instance):
        sm.current = 'menu'


class Menu(GridLayout, Server):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.cols = 1
        self.padding = [120]*4

        self.add_widget(Label(
            text='Obtain IP and port the srver is running on and enter the following details:'))

        self.sub_grid = GridLayout()

        self.sub_grid.cols = 2
        self.sub_grid.padding = [10]*4

        self.sub_grid.add_widget(Label(text='IP Address: '))
        self.ipin = TextInput(text=self.ip)
        self.sub_grid.add_widget(self.ipin)

        self.sub_grid.add_widget(Label(text='Port Number: '))
        self.portin = TextInput(text=self.port)
        self.sub_grid.add_widget(self.portin)

        self.sub_grid.add_widget(Label(text='Button Color: '))
        self.colorin = TextInput(text='1 0 0')
        self.sub_grid.add_widget(self.colorin)

        self.add_widget(self.sub_grid)
        self.add_widget(Button(text='Connect', on_press=self.connectt))

        self.err = Label(text='', color=(1, 0, 0, 1))
        self.add_widget(self.err)

    def connectt(self, instance):

        self.ip = self.ipin.text
        self.port = int(self.portin.text)
        try:
            self.server.connect((self.ip, self.port))
            # self.server.send('1'.encode('utf-8')))))
            sm.current = 'myapp'
        except Exception as e:
            self.err.text = str(e)
        color_change()


class MyApp(GridLayout, Server):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.cols = 1

        self.btn = Button()
        self.btn.text = 'Click  Me!'
        self.btn.background_normal = ''
        self.btn.background_color = ''
        self.btn.on_press = self.send

        self.add_widget(self.btn)

    def send(self):
        self.server.send('1'.encode('utf-8'))


sm = ScreenManager()
sm.add_widget(page_to_screen(Intro(), 'intro'))
menu = Menu()
sm.add_widget(page_to_screen(menu, 'menu'))
myapp = MyApp()
sm.add_widget(page_to_screen(myapp, 'myapp'))


def color_change():
    color = tuple(int(float(i)) for i in menu.colorin.text.split(' ')) + (1,)

    myapp.btn.background_color = color


if __name__ == '__main__':
    Main().run()
