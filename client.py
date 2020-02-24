# Python program to implement client side of chat room.
import socket
import sys
import details

import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

Builder.load_string('''
<Intro>
    GridLayout:
        cols:1
        padding: [150, 150, 150, 150]

        Label:
            text: 'Welcome to the quiz program!'
            font_size: 18

        Label:
            text: 'Before moving on make sure to be connected to the same network as the server.'
            font_size: 14

        Label:
        Label:

        Button:
            text: 'Continue'
            font_size: 14
            on_press: root.proceed()

<Menu>
    GridLayout:
        cols:1
        padding: [120, 120, 120, 120]

        Label:
            text: 'Check server for IP and Port to connect to it.'
            font_size: 14

        GridLayout:
            cols: 2
            padding: [10, 10, 10, 10]


            Label:
                text: 'IP address: '

            TextInput:
                id: tip
                text: root.ip

            Label:
                text: 'Port: '

            TextInput:
                id: tport
                text: root.port

            Label:
                text: 'RGB: '

            TextInput:
                id: tcolor
                text: '1 0 0'

        Button:
            text: 'Connect'
            font_size: 14
            on_press: root.connectt()

<MyApp>

    GridLayout:
        cols: 1

        Button:
            text: 'Click Me!'
            background_normal: ''
            background_color: 1, 0, 0, 1
            font_size: 18
            on_press: root.send()

''')


class Main(App):

    def build(self):
        return sm


class Server():

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip = details.ip
    port = str(details.port)


class Intro(Screen):

    def proceed(self):
        sm.current = 'menu'


color = ''


class Menu(Screen, Server):
    def connectt(self):

        global color

        self.ip = self.ids.tip.text
        self.port = int(self.ids.tport.text)
        self.server.connect((self.ip, self.port))
        # self.server.send('1'.encode('utf-8'))
        sm.current = 'myapp'
        color = tuple([float(i) for i in self.ids.tcolor.text.split(' ')] + [1])


class MyApp(Screen, Server):

    def send(self):
        self.server.send('1'.encode('utf-8'))


sm = ScreenManager()
sm.add_widget(Intro(name='intro'))
sm.add_widget(Menu(name='menu'))
sm.add_widget(MyApp(name='myapp'))


if __name__ == '__main__':
    Main().run()
