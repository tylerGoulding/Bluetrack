from Tkinter import *
from twisted.internet import tksupport, reactor
from twisted.internet.protocol import Factory, Protocol
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.protocols.basic import LineReceiver
import math
import socket
from cStringIO import StringIO
import numpy as np
from sklearn.externals import joblib
import os

H_5300 = 96
H_5302 = 325
W_5302 = 230
H_5304 = 300
W_5304 = 251
WALL_WIDTH = 16.00
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 550
wean5300_positions = [None,None,None]
wean5302_positions = [None,None,None,None]
wean5304_positions = [None,None,None,None]

 #load all training models with one node off as well
clf_room_all = joblib.load('knn_room_all.pkl')
clf5300_all = joblib.load('knn_region_given_5300_all.pkl');
clf5302_all = joblib.load('knn_region_given_5302_all.pkl'); 
clf5304_all = joblib.load('knn_region_given_5304_all.pkl'); 
clf_n0_off_all = joblib.load('knn_region_node_0_off_all.pkl')
clf_n1_off_all = joblib.load('knn_region_node_1_off_all.pkl')
clf_n2_off_all = joblib.load('knn_region_node_2_off_all.pkl')
clf_n3_off_all = joblib.load('knn_region_node_3_off_all.pkl')
clf_n4_off_all = joblib.load('knn_region_node_4_off_all.pkl')
clf_n5_off_all = joblib.load('knn_region_node_5_off_all.pkl')
clf_room_distributed = joblib.load('knn_room_distributed.pkl')
clf5300_distributed = joblib.load('knn_region_given_5300_distributed.pkl');
clf5302_distributed = joblib.load('knn_region_given_5302_distributed.pkl'); 
clf5304_distributed = joblib.load('knn_region_given_5304_distributed.pkl'); 
clf_n0_off_distributed = joblib.load('knn_region_node_0_off_distributed.pkl')
clf_n1_off_distributed = joblib.load('knn_region_node_1_off_distributed.pkl')
clf_n2_off_distributed = joblib.load('knn_region_node_2_off_distributed.pkl')
clf_n3_off_distributed = joblib.load('knn_region_node_3_off_distributed.pkl')
clf_n4_off_distributed = joblib.load('knn_region_node_4_off_distributed.pkl')
clf_n5_off_distributed = joblib.load('knn_region_node_5_off_distributed.pkl')
clf_room_centralized = joblib.load('knn_room_centralized.pkl')
clf5300_centralized = joblib.load('knn_region_given_5300_centralized.pkl');
clf5302_centralized = joblib.load('knn_region_given_5302_centralized.pkl'); 
clf5304_centralized = joblib.load('knn_region_given_5304_centralized.pkl'); 
clf_n0_off_centralized = joblib.load('knn_region_node_0_off_centralized.pkl')
clf_n1_off_centralized = joblib.load('knn_region_node_1_off_centralized.pkl')
clf_n2_off_centralized = joblib.load('knn_region_node_2_off_centralized.pkl')
clf_n3_off_centralized = joblib.load('knn_region_node_3_off_centralized.pkl')
clf_n4_off_centralized = joblib.load('knn_region_node_4_off_centralized.pkl')
clf_n5_off_centralized = joblib.load('knn_region_node_5_off_centralized.pkl')


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

        data = process_buffer(line);
        self.user = self.data[0];
        self.timestamp = self.data[1];
        self.RSSIvalues = self.data[2:];


    def connectionMade(self):
        # self.factory was set by the factory's default buildProtocol:
        self.transport.write(self.factory.quote + '\r\n')
        self.transport.loseConnection()


class RoomLocatorFactory(Factory):

    # This will be used by the default buildProtocol to create new protocols:
    protocol = RoomLocator
    def __init__(self, numUsers = None):
        self.numUsers = numUsers or 1;

class User():
    def __init__(self, number):
        self.name = name;
        self.path = []
        self.current_room = ""
        self.previous_room = ""
        self.current_room_c = ""
        self.previous_room_c = "" 
        self.current_room_d = ""
        self.previous_room_d = "" 
        self.room = ""
        self.room_c = ""
        self.room_d = ""
        self.blacklist_count = 0;
        self.blacklist_count_d = 0;
        self.blacklist_count_c = 0;
        self.i = 0;

    def predictRegion(rssi_values, node_off, clf_room, clf5300, clf5302, clf5304, clf_node_off, region="all"):
        room = ""
        current_room = ""
        if (node_off == -1):
            room = clf_room.predict(rssi_values)[0];
            if room == "5300":
              current_room = clf5300.predict(rssi_values)[0];
            elif room == "5302":
              current_room = clf5302.predict(rssi_values)[0];
            elif room == "5304":
              current_room = clf5304.predict(rssi_values)[0];

        else:
            print "node {} off".format(node_off)
            rssi_values = [rssi_values[0][:node_off*2] + rssi_values[0][node_off*2+2:]]
            current_room = clf_node_off[node_off].predict(rssi_values)[0];

        if (region=="all"):
            if (user.previous_room == ""):
                user.previous_room = current_room;
            else:
                if (current_room.startswith(blacklist_dict[user.previous_room]) and (user.blacklist_count < 3)):
                    user.blacklist_count += 1; 
                    print "blacklisting: " + current_room;
                    # do nothing
                else:
                    user.previous_room = current_room;
                    user.blacklist_count = 0;

            return user.previous_room;

        elif (region=="dist"):
            if (user.previous_room_d == ""):
                user.previous_room_d = current_room;
            else:
                if (current_room.startswith(blacklist_dict[user.previous_room_d]) and (user.blacklist_count_d < 3)):
                    user.blacklist_count_d += 1; 
                    print "blacklisting: " + current_room;
                    # do nothing
                else:
                    user.previous_room_d = current_room;
                    user.blacklist_count_d = 0;

            return user.previous_room_d;

        elif (region=="cent"):
            if (user.previous_room_c == ""):
                user.previous_room_c = current_room;

            else:
                if (current_room.startswith(blacklist_dict[user.previous_room_c]) and (user.blacklist_count_c < 3)):
                    user.blacklist_count_c += 1; 
                    print "blacklisting: " + current_room;
                    # do nothing
                else:
                    user.previous_room_c = current_room;
                    user.blacklist_count_c = 0;

            return user.previous_room_c;

# endpoint = TCP4ServerEndpoint(reactor, 8007)
# en/dpoint.listen(QOTDFactory("configurable quote"))
# reactor.run()

def drawSpace():
    increment = 1 #WINDOW_HEIGHT/700
    offset5300 = WINDOW_WIDTH/8, WINDOW_HEIGHT/8
    height5300 = increment*H_5300
    width5302 = increment*W_5302
    height5302  = increment*H_5302
    offset5302 = offset5300[0] + WALL_WIDTH , offset5300[1] + height5300 + WALL_WIDTH
    width5304 = increment*W_5304
    height5304  = increment*H_5304
    offset5304 = (offset5302[0] + width5302 + WALL_WIDTH), offset5300[1] + height5300 +WALL_WIDTH
    width5300 = increment*(1.5*width5302+width5304+4*WALL_WIDTH)

    corridor = w.create_rectangle(offset5300[0], offset5300[1],  offset5300[0]+width5300,
                                  offset5300[1]+height5300,fill='ivory2')
    wean5302 = w.create_rectangle(offset5302[0], offset5302[1],  offset5302[0]+width5302,
                                  offset5302[1]+height5302,fill='light blue')
    wean5304 = w.create_rectangle(offset5304[0], offset5304[1],  offset5304[0]+width5304,
                                  offset5304[1]+height5304,fill='LightCyan2')

    wean5300_positions[0] = w.create_rectangle(offset5300[0], offset5300[1], (offset5300[0]+(width5300/3)),
                                              (offset5300[1]+(height5300)) , fill='ivory2', outline='black')
    wean5300_positions[1] = w.create_rectangle((offset5300[0]+width5300/3), offset5300[1],  (offset5300[0]+(2*width5300/3)),
                                              (offset5300[1]+(height5300)) , fill='ivory2', outline='black')
    wean5300_positions[2] = w.create_rectangle((offset5300[0]+2*width5300/3), offset5300[1],  (offset5300[0]+(width5300)),
                                              (offset5300[1]+(height5300)) , fill='ivory2',outline='black')

    wean5302_positions[0] = w.create_rectangle(offset5302[0], offset5302[1],  (offset5302[0]+(width5302)/2),
                                              (offset5302[1]+(height5302)/2) , fill='light blue', outline='black')
    wean5302_positions[1] = w.create_rectangle((offset5302[0]+width5302/2), offset5302[1],  (offset5302[0]+(width5302)),
                                              (offset5302[1]+(height5302)/2) , fill='light blue',outline='black')
    wean5302_positions[2] = w.create_rectangle(offset5302[0], (offset5302[1]+(height5302)/2), (offset5302[0]+(width5302)/2),
                                              (offset5302[1]+(height5302)) , fill='light blue',outline='black')
    wean5302_positions[3] = w.create_rectangle(offset5302[0]+width5302/2, offset5302[1]+(height5302)/2, (offset5302[0]+(width5302)),
                                              (offset5302[1]+(height5302)) , fill='light blue',outline='black')

    wean5304_positions[0] = w.create_rectangle(offset5304[0], offset5304[1],  (offset5304[0]+(width5304)/2),
                                              (offset5304[1]+(height5304)/2) , fill='LightCyan2',outline='black')
    wean5304_positions[1] = w.create_rectangle((offset5304[0]+width5304/2), offset5304[1],  (offset5304[0]+(width5304)),
                                              (offset5304[1]+(height5304)/2) , fill='LightCyan2',outline='black')
    wean5304_positions[2] = w.create_rectangle(offset5304[0], (offset5304[1]+(height5304)/2), (offset5304[0]+(width5304)/2),
                                              (offset5304[1]+(height5304)) , fill='LightCyan2',outline='black')
    wean5304_positions[3] = w.create_rectangle(offset5304[0]+width5304/2, offset5304[1]+(height5304)/2, (offset5304[0]+(width5304)),
                                              (offset5304[1]+(height5304)) , fill='LightCyan2',outline='black')


def create_blacklist():
    blacklist_dict = {};
    blacklist_dict['5302_upper_left'] = ('5304', '5300_middle','5300_upper', '5300_lower');
    blacklist_dict['5302_upper_right'] = ('5304', '5300_middle','5300_upper', '5300_lower');
    blacklist_dict['5302_lower_left'] = ('5304','5300_upper');
    blacklist_dict['5302_lower_right'] = ('5304','5300_upper');
    blacklist_dict['5302_middle'] = ('5304', '5300_middle','5300_upper');
    blacklist_dict['5304_upper_left'] = ('5302', '5300_middle','5300_upper', '5300_lower');
    blacklist_dict['5304_upper_right'] = ('5302', '5300_middle','5300_upper', '5300_lower');
    blacklist_dict['5304_lower_left'] = ('5302', '5300_lower');
    blacklist_dict['5304_lower_right'] = ('5302', '5300_lower');
    blacklist_dict['5300_lower'] = ('5300_upper', '5304', '5302_upper_right', '5302_upper_left');
    blacklist_dict['5300_middle'] = ('5304_upper_right', '5304_upper_left', '5302_upper_right', '5302_upper_left');
    blacklist_dict['5300_upper'] = ('5300_lower', '5302', '5304_upper_right', '5304_upper_left');

def main():
    root = Tk()
    # Install the Reactor support
    tksupport.install(root)
    w = Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT,background='black')
    w.pack()
    drawSpace();
    reactor.run();

    blacklist_dict = create_blacklist();
    clf_node_off_all = [clf_n0_off_all, clf_n1_off_all, clf_n2_off_all, clf_n3_off_all,
                        clf_n4_off_all, clf_n5_off_all]

    clf_node_off_distributed = [clf_n0_off_distributed, clf_n1_off_distributed, clf_n2_off_distributed,
                                clf_n3_off_distributed, clf_n4_off_distributed, clf_n5_off_distributed]

    clf_node_off_centralized = [clf_n0_off_centralized, clf_n1_off_centralized, clf_n2_off_centralized,
                                clf_n3_off_centralized, clf_n4_off_centralized, clf_n5_off_centralized]

    pred = ["","",""]
    pred_d = ["","",""]
    pred_c = ["","",""]

    user_list = [User(0), User(1)];
    node_off = -1;
    node_off_count = [0, 0, 0, 0, 0, 0];
    while (1): 
        #receive data from server
        #call roomLocator instance
        #find line received for rssi values 
        #user 1 or user 2? roomLocator.user; 
        rssi_values = [[0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5]];
        user_num = 1; #roomLocator.user; 
        user = user_list[user_num]; 
        #node off depends on values received from either user
        for val in xrange((len(rssi_values[0])/2)):
            print val
            print rssi_values[0][val*2]
            if (rssi_values[0][val*2] == -150):
                if (node_off_count[val] > 3):
                    node_off = val;
                    break;
                else:
                    node_off_count[val] += 1; 
            else:
                node_off_count[val] = 0;
                node_off = -1; 

        # check if one of the nodes is off
        # choose the correct clf

        previous_room = user.predictRegion(rssi_values, blacklist_dict, node_off, clf_room_all, clf5300_all, 
                                           clf5302_all, clf5304_all, clf_node_off_all); 
        previous_room_c = user.predictRegion(rssi_values, blacklist_dict, node_off, clf_room_centralized,
                                             clf5300_centralized, clf5302_centralized, clf5304_centralized, 
                                             clf_node_off_centralized, "center"); 
        previous_room_d = user.predictRegion(rssi_values, blacklist_dict, node_off, clf_room_distributed, 
                                             clf5300_distributed, clf5302_distributed, clf5304_distributed,
                                             clf_node_off_distributed, "dist"); 

        pred[user_num][user.i] = (previous_room)
        pred_d[user_num][user.i] = (previous_room_d)
        pred_c[user_num][user.i] = (previous_room_c)
        user.i = (user.i+1)%3
        print user.num, previous_room, previous_room_c, previous_room_d

#########################################################################3

#reactor.listenTCP(8125, RoomLocatorFactory())
# at this point build Tk app as usual using the root object,
# and start the program with "reactor.run()", and stop it
# with "reactor.stop()".

# <<<<<<< HEAD
# reactor.listenTCP(8001, RoomLocatorFactory())

# reactor.run()
# =======
if __name__ == '__main__':
    main();
# >>>>>>> cb69b3007c64ed975e3ddb893e06d41d7f9e2d88
