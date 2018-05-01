#####################################################################
# we can break this into two files if needed it won't be hard
# I was not sure how we want to do it
# also there is some unhandled error that occurs randomly that I can't deal with/ignored
#####################################################################

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
import random
import time
from collections import deque
from colorutils import Color

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
positions = [None,None,None,None,None,None,None,None,None,None,None]
wean5300_names = ['5300_lower','5300_middle','5300_upper']
wean5302_names = ['5302_lower_right','5302_lower_left','5302_upper_right','5302_upper_left']
wean5304_names = ['5304_lower_right','5304_lower_left','5304_upper_right','5304_upper_left']
names = wean5300_names + wean5302_names + wean5304_names
#user_colors = [Color(255,42,26), Color(16,63,251)];

#wean5304_names = ['5304_lower_left','5304_lower_right', '5304_upper_left','5304_upper_right']

#load all training models with one node off as well
# clf_room_all = joblib.load('knn_room_all.pkl')
# clf5300_all = joblib.load('knn_region_given_5300_all.pkl');
# clf5302_all = joblib.load('knn_region_given_5302_all.pkl'); 
# clf5304_all = joblib.load('knn_region_given_5304_all.pkl'); 
# clf_n0_off_all = joblib.load('knn_region_node_0_off_all.pkl')
# clf_n1_off_all = joblib.load('knn_region_node_1_off_all.pkl')
# clf_n2_off_all = joblib.load('knn_region_node_2_off_all.pkl')
# clf_n3_off_all = joblib.load('knn_region_node_3_off_all.pkl')
# clf_n4_off_all = joblib.load('knn_region_node_4_off_all.pkl')
# clf_n5_off_all = joblib.load('knn_region_node_5_off_all.pkl')
# clf_room_distributed = joblib.load('knn_room_distributed.pkl')
# clf5300_distributed = joblib.load('knn_region_given_5300_distributed.pkl');
# clf5302_distributed = joblib.load('knn_region_given_5302_distributed.pkl'); 
# clf5304_distributed = joblib.load('knn_region_given_5304_distributed.pkl'); 
# clf_n0_off_distributed = joblib.load('knn_region_node_0_off_distributed.pkl')
# clf_n1_off_distributed = joblib.load('knn_region_node_1_off_distributed.pkl')
# clf_n2_off_distributed = joblib.load('knn_region_node_2_off_distributed.pkl')
# clf_n3_off_distributed = joblib.load('knn_region_node_3_off_distributed.pkl')
# clf_n4_off_distributed = joblib.load('knn_region_node_4_off_distributed.pkl')
# clf_n5_off_distributed = joblib.load('knn_region_node_5_off_distributed.pkl')
# clf_room_centralized = joblib.load('knn_room_centralized.pkl')
# clf5300_centralized = joblib.load('knn_region_given_5300_centralized.pkl');
# clf5302_centralized = joblib.load('knn_region_given_5302_centralized.pkl'); 
# clf5304_centralized = joblib.load('knn_region_given_5304_centralized.pkl'); 
# clf_n0_off_centralized = joblib.load('knn_region_node_0_off_centralized.pkl')
# clf_n1_off_centralized = joblib.load('knn_region_node_1_off_centralized.pkl')
# clf_n2_off_centralized = joblib.load('knn_region_node_2_off_centralized.pkl')
# clf_n3_off_centralized = joblib.load('knn_region_node_3_off_centralized.pkl')
# clf_n4_off_centralized = joblib.load('knn_region_node_4_off_centralized.pkl')
# clf_n5_off_centralized = joblib.load('knn_region_node_5_off_centralized.pkl')

class RoomLocator(LineReceiver):
    delimiter = '\n'
    def __init__(self):
        self.pred = [["","",""], ["","",""]]
        self.pred_d = [["","",""], ["","",""]]
        self.pred_c = [["","",""], ["","",""]]
        self.count = 0;
        self.user_num = 0;
        self.clf_room_all = joblib.load('knn_room_all.pkl')
        self.clf5300_all = joblib.load('knn_region_given_5300_all.pkl');
        self.clf5302_all = joblib.load('knn_region_given_5302_all.pkl'); 
        self.clf5304_all = joblib.load('knn_region_given_5304_all.pkl'); 
        self.clf_n0_off_all = joblib.load('knn_region_node_0_off_all.pkl')
        self.clf_n1_off_all = joblib.load('knn_region_node_1_off_all.pkl')
        self.clf_n2_off_all = joblib.load('knn_region_node_2_off_all.pkl')
        self.clf_n3_off_all = joblib.load('knn_region_node_3_off_all.pkl')
        self.clf_n4_off_all = joblib.load('knn_region_node_4_off_all.pkl')
        self.clf_n5_off_all = joblib.load('knn_region_node_5_off_all.pkl')
        self.clf_room_distributed = joblib.load('knn_room_distributed.pkl')
        self.clf5300_distributed = joblib.load('knn_region_given_5300_distributed.pkl');
        self.clf5302_distributed = joblib.load('knn_region_given_5302_distributed.pkl'); 
        self.clf5304_distributed = joblib.load('knn_region_given_5304_distributed.pkl'); 
        self.clf_n0_off_distributed = joblib.load('knn_region_node_0_off_distributed.pkl')
        self.clf_n1_off_distributed = joblib.load('knn_region_node_1_off_distributed.pkl')
        self.clf_n2_off_distributed = joblib.load('knn_region_node_2_off_distributed.pkl')
        self.clf_n3_off_distributed = joblib.load('knn_region_node_3_off_distributed.pkl')
        self.clf_n4_off_distributed = joblib.load('knn_region_node_4_off_distributed.pkl')
        self.clf_n5_off_distributed = joblib.load('knn_region_node_5_off_distributed.pkl')
        self.clf_room_centralized = joblib.load('knn_room_centralized.pkl')
        self.clf5300_centralized = joblib.load('knn_region_given_5300_centralized.pkl');
        self.clf5302_centralized = joblib.load('knn_region_given_5302_centralized.pkl'); 
        self.clf5304_centralized = joblib.load('knn_region_given_5304_centralized.pkl'); 
        self.clf_n0_off_centralized = joblib.load('knn_region_node_0_off_centralized.pkl')
        self.clf_n1_off_centralized = joblib.load('knn_region_node_1_off_centralized.pkl')
        self.clf_n2_off_centralized = joblib.load('knn_region_node_2_off_centralized.pkl')
        self.clf_n3_off_centralized = joblib.load('knn_region_node_3_off_centralized.pkl')
        self.clf_n4_off_centralized = joblib.load('knn_region_node_4_off_centralized.pkl')
        self.clf_n5_off_centralized = joblib.load('knn_region_node_5_off_centralized.pkl')

        self.clf_node_off_all = [self.clf_n0_off_all, self.clf_n1_off_all, self.clf_n2_off_all,
                                 self.clf_n3_off_all, self.clf_n4_off_all, self.clf_n5_off_all]

        self.clf_node_off_distributed = [self.clf_n0_off_distributed, self.clf_n1_off_distributed,
                                        self.clf_n2_off_distributed, self.clf_n3_off_distributed,
                                        self.clf_n4_off_distributed, self.clf_n5_off_distributed]

        self.clf_node_off_centralized = [self.clf_n0_off_centralized, self.clf_n1_off_centralized,
                                        self.clf_n2_off_centralized, self.clf_n3_off_centralized,
                                        self.clf_n4_off_centralized, self.clf_n5_off_centralized]

        self.node_off = -1
        self.node_off_count = [0, 0, 0, 0, 0, 0];
        self.data = []
        self.user_id = -1
        self.timestamp = -1
        self.RSSIvalues = []
        # self.canvas = self.factory.canvas(root)
        # canvas.pack()
        self.blacklist_dict = create_blacklist();

    def process_buffer(self,buffer):
        timestamp = []
        rssi_values = []
        f = StringIO(buffer)
        for line in f:
            data = (line.strip()).split(',')
            user = data[0]
            timestamp.append(data[1])
            rssi_values.append(map(float,data[2:]))
        return int(user), timestamp, rssi_values

    def dataReceived(self, data):
        if data != '':
            self.data = self.process_buffer(str(data));
            self.user_id = self.data[0];
            user = self.factory.user_list[self.user_id]
            self.timestamp = self.data[1];
            self.RSSIvalues = self.data[2];
            # print self.RSSIvalues
            for val in xrange((len(self.RSSIvalues[0])/2)):
                if (self.RSSIvalues[0][val*2] == -150):
                    if (self.node_off_count[val] > 3):
                        self.node_off = val;
                        break;
                    else:
                        self.node_off_count[val] += 1; 
                else:
                    self.node_off_count[val] = 0;
                    self.node_off = -1; 

            room, current_region = user.predictRegion(self.RSSIvalues, self.blacklist_dict, self.node_off, self.clf_room_all, self.clf5300_all, 
                                               self.clf5302_all, self.clf5304_all, self.clf_node_off_all); 
            _,current_region_c = user.predictRegion(self.RSSIvalues, self.blacklist_dict, self.node_off, self.clf_room_centralized,
                                                 self.clf5300_centralized, self.clf5302_centralized, self.clf5304_centralized, 
                                                 self.clf_node_off_centralized, "center"); 
            _,current_region_d = user.predictRegion(self.RSSIvalues, self.blacklist_dict, self.node_off,
                                                self.clf_room_distributed, self.clf5300_distributed,
                                                self.clf5302_distributed, self.clf5304_distributed,
                                                self.clf_node_off_distributed, "dist"); 


            ########################################################
            # test tomorro
            # if (user.current_region == "5304_lower_right" and user.current_region_d == "5304_lower_right"):
            #    user.current_region = "5304_lower_right";
            # else:
            #    user.current_region = user.current_region_c

            self.pred[self.user_id][user.i] = (user.current_region)
            self.pred_d[self.user_id][user.i] = (user.current_region_d)
            self.pred_c[self.user_id][user.i] = (user.current_region_c)
            if room == "5302":
                total = self.pred[self.user_id] +self.pred_d[self.user_id] 
            if (self.user_id == 0):
                print "User Zero:"
                print "Pred Al:      ", max(self.pred[self.user_id], key=self.pred[self.user_id].count), self.pred[self.user_id]
                print "Pred Central: ", max(self.pred_c[self.user_id], key=self.pred_c[self.user_id].count), self.pred_c[self.user_id]
                print "Pred Distrib: ", max(self.pred_d[self.user_id], key=self.pred_d[self.user_id].count), self.pred_d[self.user_id]
                print "Most Commom:  ", max(total, key=total.count)
                if "5302_upper_left" in total:
                    print "Ignore most common: In 5302_upper_left"
                print "____________"


            user.i = (user.i+1)%3  
            ########################################################

            #pred_list = self.pred[self.user_id] + self.pred_d[self.user_id] + self.pred_c[self.user_id]
            user.current_region = max(total, key=total.count)
            if user.current_region != '':
                #user.clearPrevious(self.factory.canvas);
                #user.drawCurrent(self.factory.canvas);
                user.addPath();
                self.updateCanvas();
                user.previous_region = user.current_region;
                user.previous_region_d = user.current_region_d;
                user.previous_region_c = user.current_region_c; 

                # if (self.factory.user_list[0].current_region == self.factory.user_list[1].current_region):
                #     index = names.index(user.current_region);
                #     self.factory.canvas.itemconfig(positions[index], fill='DarkOrchid4');

    def connectionMade(self):
        print "hello"
        # self.factory was set by the factory's default buildProtocol:
        # self.transport.write("connected to Server" + '\r\n')
        # self.transport.loseConnection()

    def updateCanvas(self):
        user1 = self.factory.user_list[0];
        user2 = self.factory.user_list[1];

        for location in positions:
            index = names.index(location);
            if ((location in user1.deque) and (location in user2.deque)):
                user1_index = user1.deque.index(location);
                user2_index = user2.deque.index(location);
                user1_color = user1.colors[user1_index];
                user2_color = user2.colors[user2_index];
                new_color = self.colorBlend(user1_color, user2_color);
                w.itemconfig(location, fill=str(new_color.hex));
            elif (location in user1.deque):
                user1_index = user1.deque.index(location);
                user1_color = user1.colors[user1_index];
                w.itemconfig(location, fill=str(user1_color.hex));
            elif (location in user2.deque):
                user2_index = user2.deque.index(location);
                user2_color = user2.colors[user2_index];
                w.itemconfig(location, fill=str(user2_color.hex));
            else: 
                w.itemconfig(location, fill='cornsilk2');

class RoomLocatorFactory(Factory):
    # This will be used by the default buildProtocol to create new protocols:
    protocol = RoomLocator
    def __init__(self,canvas, numUsers = None, verbose = False):
        self.canvas = canvas;
        self.numUsers = numUsers or 1;
        self.verbose = verbose;
        self.user_color_list = [[], []];
        self.user_list = [User(0, self.user_color_list[0]), User(1, self.user_color_list[1])];

class User():
    def __init__(self, number, colors):
        self.path_q = deque(maxlen=5)
        self.number = number;
        # self.path = []
        self.previous_region = ""
        self.current_region = ""
        self.previous_region_c = ""
        self.current_region_c = "" 
        self.previous_region_d = ""
        self.current_region_d = "" 
        self.blacklist_count = 0;
        self.blacklist_count_d = 0;
        self.blacklist_count_c = 0;
        self.i = 0;
        self.colors = colors;

    def predictRegion(self, rssi_values, blacklist_dict, node_off, clf_room, clf5300, clf5302, 
                      clf5304, clf_node_off, region="all"):

        room = ""
        predicted_region = ""
        if (node_off == -1):
            room = clf_room.predict(rssi_values)[0];
            if (room == "5300"):
              predicted_region = clf5300.predict(rssi_values)[0];
            elif (room == "5302"):
              predicted_region = clf5302.predict(rssi_values)[0];
            elif (room == "5304"):
              predicted_region = clf5304.predict(rssi_values)[0];

        else:
            print "node {} off".format(node_off)
            rssi_values = [rssi_values[0][:node_off*2] + rssi_values[0][node_off*2+2:]]
            predicted_region = clf_node_off[node_off].predict(rssi_values)[0];

        if (region=="all"):
            if (self.current_region == ""):
                self.current_region = predicted_region;
            else:
                if (predicted_region.startswith(blacklist_dict[self.current_region]) and (self.blacklist_count<3)):
                    self.blacklist_count += 1; 
                    print "blacklisting: " + predicted_region;
                    # do nothing
                else:
                    self.current_region = predicted_region;
                    self.blacklist_count = 0;

            return room, self.current_region;

        elif (region=="dist"):
            if (self.current_region_d == ""):
                self.current_region_d = predicted_region;
            else:
                if (predicted_region.startswith(blacklist_dict[self.current_region_d]) and (self.blacklist_count_d<3)):
                    self.blacklist_count_d += 1; 
                    print "blacklisting: " + predicted_region;
                    # do nothing
                else:
                    self.current_region_d = predicted_region;
                    self.blacklist_count_d = 0;

            return room, self.current_region_d;

        elif (region=="center"):
            if (self.current_region_c == ""):
                self.current_region_c = predicted_region;

            else:
                if (predicted_region.startswith(blacklist_dict[self.current_region_c]) and (self.blacklist_count_c<3)):
                    self.blacklist_count_c += 1; 
                    print "blacklisting: " + predicted_region;
                    # do nothing
                else:
                    self.current_region_c = predicted_region;
                    self.blacklist_count_c = 0;

            return room, self.current_region_c;

    def addPath(self):
        path_q.append(self.current_region);
        # if (self.current_region != self.previous_region):
            # self.path.append(self.current_region);


    def clearPrevious(self, w):
        if ((len(self.path) > 0)):
            index = names.index(self.path[-1]);
            print w.itemcget(positions[index], "fill")
            if (self.number == 1) and (w.itemcget(positions[index], "fill") == 'DarkOrchid4'):
                w.itemconfig(positions[index], fill='blue');
            if (self.number == 0) and (w.itemcget(positions[index], "fill") == 'DarkOrchid4'):
                w.itemconfig(positions[index], fill='red');

            w.itemconfig(positions[index], fill='cornsilk2');

    def drawCurrent(self,w):
        index = names.index(self.current_region);
        w.itemconfig(positions[index], fill=self.colors[0]);

# endpoint = TCP4ServerEndpoint(reactor, 8007)
# en/dpoint.listen(QOTDFactory("configurable quote"))
# reactor.run()

def drawSpace(w):
    global positions
    increment = 1 #WINDOW_HEIGHT/700
    offset5300 = WINDOW_WIDTH/16, WINDOW_HEIGHT/16
    height5300 = increment*H_5300
    width5302 = increment*W_5302
    height5302  = increment*H_5302
    offset5302 = offset5300[0] + WALL_WIDTH , offset5300[1] + height5300 + WALL_WIDTH
    width5304 = increment*W_5304
    height5304  = increment*H_5304
    offset5304 = (offset5302[0] + width5302 + WALL_WIDTH), offset5300[1] + height5300 +WALL_WIDTH
    width5300 = increment*(2*width5302+width5304+4*WALL_WIDTH)

    corridor = w.create_rectangle(offset5300[0], offset5300[1],  offset5300[0]+width5300,
                                  offset5300[1]+height5300,fill='cornsilk2')
    wean5302 = w.create_rectangle(offset5302[0], offset5302[1],  offset5302[0]+width5302,
                                  offset5302[1]+height5302,fill='cornsilk2')

    wean5304 = w.create_rectangle(offset5304[0], offset5304[1],  offset5304[0]+width5304,
                                  offset5304[1]+height5304,fill='cornsilk2')

    wean5310 = w.create_rectangle(offset5304[0]+WALL_WIDTH+width5304, offset5302[1],
                                  WINDOW_WIDTH-60, offset5302[1]+height5302, fill="grey30")

    wean5310_txt = w.create_text((offset5304[0]+WALL_WIDTH+width5304+WINDOW_WIDTH-50)/2, 
                                (offset5302[1]*2 + height5302)/2, text="5310", font="Helvetica 20 italic")

    wean5300_positions[0] = w.create_rectangle(offset5300[0], offset5300[1], (offset5300[0]+(width5300/3)),
                                              (offset5300[1]+(height5300)) , fill='cornsilk2', outline='black')
    wean5300_positions[1] = w.create_rectangle((offset5300[0]+width5300/3), offset5300[1], (offset5300[0]+(2*width5300/3)),
                                              (offset5300[1]+(height5300)) , fill='cornsilk2', outline='black')
    wean5300_positions[2] = w.create_rectangle((offset5300[0]+2*width5300/3), offset5300[1],  (offset5300[0]+(width5300)),
                                              (offset5300[1]+(height5300)) , fill='cornsilk2',outline='black')
    wean5302_positions[0] = w.create_rectangle(offset5302[0], offset5302[1],  (offset5302[0]+(width5302)/2),
                                              (offset5302[1]+(height5302)/2) , fill='cornsilk2', outline='black')
    wean5302_positions[1] = w.create_rectangle((offset5302[0]+width5302/2), offset5302[1],  (offset5302[0]+(width5302)),
                                              (offset5302[1]+(height5302)/2) , fill='cornsilk2',outline='black')
    wean5302_positions[2] = w.create_rectangle(offset5302[0], (offset5302[1]+(height5302)/2), (offset5302[0]+(width5302)/2),
                                              (offset5302[1]+(height5302)) , fill='cornsilk2',outline='black')
    wean5302_positions[3] = w.create_rectangle(offset5302[0]+width5302/2, offset5302[1]+(height5302)/2, (offset5302[0]+(width5302)),
                                              (offset5302[1]+(height5302)) , fill='cornsilk2',outline='black')
    wean5304_positions[0] = w.create_rectangle(offset5304[0], offset5304[1],  (offset5304[0]+(width5304)/2),
                                              (offset5304[1]+(height5304)/2) , fill='cornsilk2',outline='black')
    wean5304_positions[1] = w.create_rectangle((offset5304[0]+width5304/2), offset5304[1],  (offset5304[0]+(width5304)),
                                              (offset5304[1]+(height5304)/2) , fill='cornsilk2',outline='black')
    wean5304_positions[2] = w.create_rectangle(offset5304[0], (offset5304[1]+(height5304)/2), (offset5304[0]+(width5304)/2),
                                              (offset5304[1]+(height5304)) , fill='cornsilk2',outline='black')
    wean5304_positions[3] = w.create_rectangle(offset5304[0]+width5304/2, offset5304[1]+(height5304)/2, (offset5304[0]+(width5304)),
                                              (offset5304[1]+(height5304)) , fill='cornsilk2',outline='black')


    # wean5302_txt = w.create_text((offset5302[0]*2+width5302)/2, 
    #                             (offset5302[1]*2 + height5302)/2, text="5302",
    #                             font="Helvetica 20")

    # wean5300_txt = w.create_text((offset5300[0]*2+width5300)/2, 
    #                             (offset5300[1]*2 + height5300)/2, text="Corridor 5300",
    #                             font="Helvetica 20")
    # wean5304_txt = w.create_text((offset5304[0]*2+width5304)/2, 
    #                             (offset5304[1]*2 + height5304)/2, text="5304",
    #                             font="Helvetica 20")

    legend_width = 220
    legend_height = 160
    legend_offset = 50
    legend_offset_h = 30
    legend_offset_w = 45
    margin = 10;

    legend_box = w.create_rectangle(WINDOW_WIDTH-legend_width, WINDOW_HEIGHT-legend_height,
                                    WINDOW_WIDTH-legend_offset, WINDOW_HEIGHT-50, fill='cornsilk2');

    user1_legend = w.create_rectangle(WINDOW_WIDTH-legend_width+margin, WINDOW_HEIGHT-legend_height+margin,
                                      WINDOW_WIDTH-legend_width+legend_offset_w, 
                                      WINDOW_HEIGHT-legend_height+legend_offset_h, fill='red');

    user1_txt = w.create_text(WINDOW_WIDTH-legend_height+margin,  WINDOW_HEIGHT-140, text="User 1")
    
    user2_legend = w.create_rectangle(WINDOW_WIDTH-legend_width+margin,
                                      WINDOW_HEIGHT-legend_height+margin+legend_offset_h,
                                      WINDOW_WIDTH-legend_width+legend_offset_w, 
                                      WINDOW_HEIGHT-legend_height+2*legend_offset_h, fill='blue');
    
    user2_txt = w.create_text(WINDOW_WIDTH-legend_height+margin,  WINDOW_HEIGHT-110, text="User 2")

    both_legend = w.create_rectangle(WINDOW_WIDTH-legend_width+margin,
                                    WINDOW_HEIGHT-legend_height+margin+2*legend_offset_h,
                                    WINDOW_WIDTH-legend_width+legend_offset_w,
                                    WINDOW_HEIGHT-legend_height+3*legend_offset_h, fill='DarkOrchid4');

    user2_txt = w.create_text(WINDOW_WIDTH-legend_height+margin,  WINDOW_HEIGHT-80, text="Both")

    positions = wean5300_positions + wean5302_positions + wean5304_positions;

         
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

    return blacklist_dict;

def main():
    root = Tk()
    root.title("BlueTrack")
    # Install the Reactor support
    w = Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT,background='SkyBlue4')
    root.resizable(width=False, height=False)
    w.pack()
    drawSpace(w);
    # blacklist_dict = create_blacklist();
    # clf_node_off_all = [clf_n0_off_all, clf_n1_off_all, clf_n2_off_all, clf_n3_off_all,
                        # clf_n4_off_all, clf_n5_off_all]

    # clf_node_off_distributed = [clf_n0_off_distributed, clf_n1_off_distributed, clf_n2_off_distributed,
                                # clf_n3_off_distributed, clf_n4_off_distributed, clf_n5_off_distributed]

    # clf_node_off_centralized = [clf_n0_off_centralized, clf_n1_off_centralized, clf_n2_off_centralized,
                                # clf_n3_off_centralized, clf_n4_off_centralized, clf_n5_off_centralized]

    tksupport.install(root)
    reactor.listenTCP(8050, RoomLocatorFactory(w))
    reactor.run()

if __name__ == '__main__':
    main();