from Tkinter import *
from twisted.internet import tksupport, reactor
from twisted.internet.protocol import Factory, Protocol
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.protocols.basic import LineReceiver

class RoomLocator(LineReceiver):
    def process_buffer(buffer):
        timestamp = []
        rssi_values = []
        f = StringIO(buffer)
        for line in f:
            data = (line.strip()).split(',')
            user = data[0]
            timestamp.append(data[1])
            rssi_values.append(map(float,data[2:]))
        return user, timestamp, rssi_values

    def lineReceived(self, line):
        print line
        self.user, self.timestamp, self.rssi_values = process_buffer(line);
        self.user = self.data[0];
        self.timestamp = self.data[1];
        self.RSSIvalues = self.data[2:];

        # if response:
        #     self.transport.write(response)


    def connectionMade(self):
        # self.factory was set by the factory's default buildProtocol:

        self.transport.write(self.factory.quote + '\r\n')
        self.transport.loseConnection()


class RoomLocatorFactory(Factory):

    # This will be used by the default buildProtocol to create new protocols:
    protocol = RoomLocator

    def __init__(self, numUsers = None):
        self.numUsers = numUsers or 1;

# endpoint = TCP4ServerEndpoint(reactor, 8007)
# en/dpoint.listen(QOTDFactory("configurable quote"))
# reactor.run()
wall_width = 8.00

window_height = 700
window_width = 1200
increment = window_height/700.
offset5300 = 150, 150
height5300 = increment*96
width5300 = increment*900

width5302 = increment*230
height5302  = increment*325
offset5302 = offset5300[0] + wall_width , offset5300[1] + height5300 + wall_width


width5304 = increment*251
height5304  = increment*300
offset5304 = (offset5302[0] + width5302 + wall_width), offset5300[1] + height5300 +wall_width
print offset5302
print offset5304


root = Tk()

# Install the Reactor support
tksupport.install(root)
w = Canvas(root, width=1200, height=700,background='black')
w.pack()

colors = ["blue","red"]

corridor = w.create_rectangle(offset5300[0], offset5300[1],  offset5300[0]+width5300, offset5300[1]+height5300,fill='white')
wean5302 = w.create_rectangle(offset5302[0], offset5302[1],  offset5302[0]+width5302, offset5302[1]+height5302,fill='white')
wean5304 = w.create_rectangle(offset5304[0], offset5304[1],  offset5304[0]+width5304, offset5304[1]+height5304,fill='white')
wean5302_positions = [None,None,None,None]
wean5302_positions[0] = w.create_rectangle(offset5302[0], offset5302[1],  (offset5302[0]+(width5302)/2), (offset5302[1]+(height5302)/2) , fill='white')
wean5302_positions[1] = w.create_rectangle((offset5302[0]+width5302/2), offset5302[1],  (offset5302[0]+(width5302)), (offset5302[1]+(height5302)/2) , fill='white')
wean5302_positions[2] = w.create_rectangle(offset5302[0], (offset5302[1]+(height5302)/2),  (offset5302[0]+(width5302)/2), (offset5302[1]+(height5302)) , fill='white')
wean5302_positions[3] = w.create_rectangle(offset5302[0]+width5302/2, offset5302[1]+(height5302)/2,  (offset5302[0]+(width5302)), (offset5302[1]+(height5302)) , fill='white')

wean5304_positions = [None,None,None,None]
wean5304_positions[0] = w.create_rectangle(offset5304[0], offset5304[1],  (offset5304[0]+(width5304)/2), (offset5304[1]+(height5304)/2) , fill='white')
wean5304_positions[1] = w.create_rectangle((offset5304[0]+width5304/2), offset5304[1],  (offset5304[0]+(width5304)), (offset5304[1]+(height5304)/2) , fill='white')
wean5304_positions[2] = w.create_rectangle(offset5304[0], (offset5304[1]+(height5304)/2),  (offset5304[0]+(width5304)/2), (offset5304[1]+(height5304)) , fill='white')
wean5304_positions[3] = w.create_rectangle(offset5304[0]+width5304/2, offset5304[1]+(height5304)/2,  (offset5304[0]+(width5304)), (offset5304[1]+(height5304)) , fill='white')

# wean5304 = w.create_rectangle(offset5302[0], offset5302[1],  offset5302[0]+width5300,offset5302[1]+height5300)

# at this point build Tk app as usual using the root object,
# and start the program with "reactor.run()", and stop it
# with "reactor.stop()".

reactor.listenTCP(8001, RoomLocatorFactory())

reactor.run()