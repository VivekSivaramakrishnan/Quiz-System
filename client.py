# Python program to implement client side of chat room.
import socket
import sys
import details

from _thread import start_new_thread

import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy_garden.zbarcam import ZBarCam
from kivy.uix.screenmanager import ScreenManager, Screen

from kivy.core.window import Window

Window.clearcolor = (1, 1, 1, 1)
HEAD = 'ProductSans-Light.ttf'
HEAD_size = 40

BUTTON = 'ProductSans-Bold.ttf'
BUTTON_size = 18

TEXT_input = 'CONSOLA.TTF'

BLUE = (0.298, 0.5451, 0.9608, 1)
BUTTON_BLUE = (0.1, 0.45, 0.91, 1)


def page_to_screen(page, name):
    screen = Screen(name=name)
    screen.add_widget(page)
    return screen


class Main(App):

    def build(self):
        return sm


class Client():

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ipp = details.ip
    portt = str(details.port)


class Intro(GridLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        # l, u, r, d
        self.padding = [50, 0, 50, 50]

        self.welcome_label = Label(text='Hi there',
                                   font_name=HEAD, color=[0, 0, 0, 1], font_size=HEAD_size)
        self.add_widget(self.welcome_label)
        self.add_widget(Label(
            text='Before proceeding make sure to be connected to the network of the server'))

        self.button_box = BoxLayout(orientation='horizontal')

        self.qr_button = Button(text='QR (beta)', on_press=self.qrproceed)
        self.qr_button.font_name = BUTTON
        self.qr_button.color = BLUE
        self.qr_button.font_size = BUTTON_size
        self.qr_button.background_normal = ''
        self.qr_button.background_color = (0, 0, 0, 0)
        self.qr_button.size_hint = None, None
        self.qr_button.size[1] = BUTTON_size + 20
        self.button_box.add_widget(self.qr_button)

        self.menu_button = Button(text='Continue', on_press=self.proceed)
        self.menu_button.font_name = BUTTON
        self.menu_button.color = (1, 1, 1, 1)
        self.menu_button.font_size = BUTTON_size
        self.menu_button.background_normal = ''
        self.menu_button.background_color = BUTTON_BLUE
        self.menu_button.size_hint = None, None
        self.menu_button.size[1] = BUTTON_size + 20
        self.button_box.add_widget(self.menu_button)

        self.button_box.spacing = Window.size[0]-100 - \
            self.qr_button.size[0]-self.menu_button.size[0]
        self.add_widget(self.button_box)

    def proceed(self, instance):
        sm.transition.direction = 'left'
        sm.current = 'menu'

    def qrproceed(self, instance):
        sm.transition.direction = 'right'
        sm.current = 'qrmenu'


class QrCodeScanner(GridLayout, Client):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.cols = 1
        self.padding = [50, 50, 50, 50]

        self.add_widget(Label(text='Point to QR code on quiz master',
                              font_name=HEAD, color=[0, 0, 0, 1], font_size=BUTTON_size))

        self.camera = ZBarCam()
        self.add_widget(self.camera)

        self.err = Label(text='', color=(1, 0, 0, 1))
        self.err.size_hint = None, None
        self.add_widget(self.err)

        start_new_thread(self.monitor_camera, (1,))

    def monitor_camera(self, rubb):

        while True:
            if self.camera.symbols:
                try:
                    self.ip, self.port, self.color = str(
                        self.camera.symbols[0].data).split(' ')
                    self.ip = self.ip[2:]
                    self.port = self.port
                    self.color = self.color[:-1]
                    break
                except Exception as e:
                    self.err.text = str(e)

        try:
            self.client.connect((self.ip, int(self.port)))
            self.connected = True
            # self.client.send('1'.encode('utf-8')))))
            sm.current = 'myapp'
        except Exception as e:
            self.err.text = '2'+str(e)
        color_change_qr()
        return


class Menu(GridLayout, Client):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.cols = 1
        self.padding = [50]*4

        self.add_widget(Label(
            text='Obtain IP and port the server is running on and enter the following details:', font_name=HEAD, color=[0, 0, 0, 1], font_size=BUTTON_size))

        self.sub_grid = GridLayout()

        self.sub_grid.cols = 2
        # self.sub_grid.padding = [10]*4

        self.sub_grid.add_widget(Label(text='IP Address: ', font_name=TEXT_input, color=[
                                 0, 0, 0, 1], font_size=BUTTON_size))
        self.ipin = TextInput(text=self.ipp)
        self.ipin.background_normal = ''
        self.ipin.background_color = (1, 1, 1, 1)
        self.ipin.font_name = TEXT_input
        self.sub_grid.add_widget(self.ipin)

        self.sub_grid.add_widget(Label(text='Port Number: ', font_name=TEXT_input, color=[
                                 0, 0, 0, 1], font_size=BUTTON_size))
        self.portin = TextInput(text=self.portt)
        self.portin.background_normal = ''
        self.portin.background_color = (1, 1, 1, 1)
        self.portin.font_name = TEXT_input
        self.sub_grid.add_widget(self.portin)

        self.sub_grid.add_widget(Label(text='Button Color: ', font_name=TEXT_input, color=[
                                 0, 0, 0, 1], font_size=BUTTON_size))
        self.colorin = TextInput(text='100')
        self.colorin.background_normal = ''
        self.colorin.background_color = (1, 1, 1, 1)
        self.colorin.font_name = TEXT_input
        self.sub_grid.add_widget(self.colorin)

        self.add_widget(self.sub_grid)

        self.connect_button = Button(text='Connect', on_press=self.connectt)
        self.connect_button.font_name = BUTTON
        self.connect_button.color = (1, 1, 1, 1)
        self.connect_button.font_size = BUTTON_size
        self.connect_button.background_normal = ''
        self.connect_button.background_color = BUTTON_BLUE
        self.connect_button.size_hint[1] = None
        self.connect_button.size[1] = BUTTON_size + 20
        self.add_widget(self.connect_button)

        self.err = Label(text='', color=(1, 0, 0, 1))
        self.err.size_hint = None, None
        self.add_widget(self.err)

    def connectt(self, instance):

        self.ip = self.ipin.text
        self.port = int(self.portin.text)
        try:
            self.client.connect((self.ip, self.port))
            self.connected = True
            # self.client.send('1'.encode('utf-8')))))
            sm.current = 'myapp'
        except Exception as e:
            self.err.text = str(e)
        color_change()


class MyApp(GridLayout, Client):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.cols = 1

        self.btn = Button()
        self.btn.text = 'Click  Me!'
        self.btn.background_normal = ''
        self.btn.background_color = ''
        self.btn.on_press = self.send
        self.connected = False

        self.add_widget(self.btn)
        start_new_thread(self.able_disable, ())

    def send(self):
        self.client.send('1'.encode('utf-8'))

    def able_disable(self):

        while True:
            if self.connected:
                msg = self.client.recv(64).decode('utf-8')
                self.btn.disabled = True
                self.btn.text = 'Wait...'
                msg = self.client.recv(64).decode('utf-8')
                self.btn.disabled = False
                self.btn.text = 'Click me!'


sm = ScreenManager()
sm.add_widget(page_to_screen(Intro(), 'intro'))
qrmenu = QrCodeScanner()
sm.add_widget(page_to_screen(qrmenu, 'qrmenu'))
menu = Menu()
sm.add_widget(page_to_screen(menu, 'menu'))
myapp = MyApp()
sm.add_widget(page_to_screen(myapp, 'myapp'))


def color_change():
    color = tuple(int(float(i)) for i in list(menu.colorin.text)) + (1,)

    myapp.btn.background_color = color
    myapp.connected = True


def color_change_qr():
    color = tuple(int(float(i)) for i in list(qrmenu.color)) + (1,)

    myapp.btn.background_color = color
    myapp.connected = True


if __name__ == '__main__':
    Main().run()
