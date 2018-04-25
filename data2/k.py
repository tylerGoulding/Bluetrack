import kivy
from kivy.config import Config

from kivy.support import install_twisted_reactor

Config.set('graphics', 'width', '1200')
Config.set('graphics', 'height', '700')


from kivy.core.window import Window


from kivy.uix.widget import Widget

install_twisted_reactor()

from twisted.internet import reactor
from twisted.internet import protocol
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty

from kivy.uix.floatlayout import FloatLayout
from kivy.properties import NumericProperty
from kivy.properties import StringProperty


class EchoServer(protocol.Protocol):
    def dataReceived(self, data):
        response = self.factory.app.handle_message(data)
        if response:
            self.transport.write(response)


class EchoServerFactory(protocol.Factory):
    protocol = EchoServer

    def __init__(self, app):
        self.app = app


from kivy.app import App
from kivy.uix.label import Label


class floor(Widget):
    wall_width = 8.00

    window_height = Window.height
    window_width = Window.width
    increment = Window.height/700.
    offset5300 = 150, window_height - 150
    height5300 = increment*96
    width5300 = increment*900

    width5302 = increment*230
    height5302  = increment*325
    offset5302 = offset5300[0], offset5300[1] - height5302

    
    width5304 = increment*251
    height5304  = increment*300
    offset5304 = (offset5300[0] + width5302 + wall_width), offset5300[1] - height5304

    name = StringProperty('')


class layout5300(Widget):
    pass





    # pass

class TwistedServerApp(App):
    root = None
    flor = None

    def build(self):
        root = FloatLayout(padding=10)
        reactor.listenTCP(8000, EchoServerFactory(self))
        flor = floor()
        root.add_widget(flor);
        return root

    def handle_message(self, msg):
        # print self.root.children[0].

        msg = msg.decode('utf-8')
        # self.label.name = "size = {}x{} received:  {}\n".format( msg)
        self.root.children[0].name.text = "responded: {}\n".format(msg)
        print msg
        return msg.encode('utf-8')


if __name__ == '__main__':
    # Window.fullscreen = True


    TwistedServerApp().run()