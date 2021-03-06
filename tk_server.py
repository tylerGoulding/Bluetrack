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
from colorutils import Color
import time

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
wean5302_names = ['5302_lower_right','5302_lower_left', '5302_upper_right','5302_upper_left']
wean5304_names = ['5304_lower_right','5304_lower_left', '5304_upper_right','5304_upper_left']
names = wean5300_names + wean5302_names + wean5304_names

#wean5304_names = ['5304_lower_left','5304_lower_right', '5304_upper_left','5304_upper_right']

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

class User():
    def __init__(self, number):
        self.number = number;
        self.path = []
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

    def predictRegion(self, rssi_values, blacklist_dict, node_off, clf_room, clf5300, clf5302, 
                      clf5304, clf_node_off, region="all"):

        room = ""
        predicted_region = ""
        if (node_off == -1):
            room = clf_room.predict(rssi_values)[0];
            if room == "5300":
              predicted_region = clf5300.predict(rssi_values)[0];
            elif room == "5302":
              predicted_region = clf5302.predict(rssi_values)[0];
            elif room == "5304":
              predicted_region = clf5304.predict(rssi_values)[0];

        else:
            print "node {} off".format(node_off)
            rssi_values = [rssi_values[0][:node_off*2] + rssi_values[0][node_off*2+2:]]
            predicted_region = clf_node_off[node_off].predict(rssi_values)[0];

        if (region=="all"):
            if (self.current_region == ""):
                self.current_region = predicted_region;
            else:
                if (predicted_region.startswith(blacklist_dict[self.current_region]) and (self.blacklist_count < 3)):
                    self.blacklist_count += 1; 
                    print "blacklisting: " + predicted_region;
                    # do nothing
                else:
                    self.current_region = predicted_region;
                    self.blacklist_count = 0;

            return self.current_region;

        elif (region=="dist"):
            if (self.current_region_d == ""):
                self.current_region_d = predicted_region;
            else:
                if (predicted_region.startswith(blacklist_dict[self.current_region_d]) and (self.blacklist_count_d < 3)):
                    self.blacklist_count_d += 1; 
                    print "blacklisting: " + predicted_region;
                    # do nothing
                else:
                    self.current_region_d = predicted_region;
                    self.blacklist_count_d = 0;

            return self.current_region_d;

        elif (region=="center"):
            if (self.current_region_c == ""):
                self.current_region_c = predicted_region;

            else:
                if (predicted_region.startswith(blacklist_dict[self.current_region_c]) and (self.blacklist_count_c < 3)):
                    self.blacklist_count_c += 1; 
                    print "blacklisting: " + predicted_region;
                    # do nothing
                else:
                    self.current_region_c = predicted_region;
                    self.blacklist_count_c = 0;

            return self.current_region_c;

    def addPath(self):
        self.path.append(self.current_region);

    def clearPrevious(self, w):
        if ((len(self.path) > 0)):
            index = names.index(self.path[-1]);
            w.itemconfig(positions[index], fill='cornsilk2');

    def drawCurrent(self, w, user_colors):
        index = names.index(self.current_region);
        c1_index = 0
        c2_index = 4
        new_color = color_blend(user_colors, c1_index, c2_index);
        w.itemconfig(positions[index], fill=str(new_color.hex));

# endpoint = TCP4ServerEndpoint(reactor, 8007)
# en/dpoint.listen(QOTDFactory("configurable quote"))
# reactor.run()



def color_blend_2(c1,c2):
    r = (c1.red+c2.red)/2;
    g = (c1.green+c2.green)/2;
    b = (c1.blue+c2.blue)/2;
    print r
    print g
    print b

    return Color((r, g, b))

def color_blend(user_colors, c1_index, c2_index):
    c1 = user_colors[0][c1_index];
    c2 = user_colors[1][c2_index];
    difference = abs(c1_index - c2_index) + 2.5; 
    total = 5
    if (c1_index > c2_index):
        r = min(255, c1.red*difference/total+ c2.red*(total-difference)/total);
        g = min(255, c1.green*difference/total+ c2.green*(total-difference)/total);
        b = min(255, c1.blue*difference/total+ c2.blue*(total-difference)/total);
    else:
        r = min(255, c2.red*difference/total+ c1.red*(total-difference)/total);
        g = min(255, c2.green*difference/total+ c1.green*(total-difference)/total);
        b = min(255, c2.blue*difference/total+ c1.blue*(total-difference)/total);
    return Color((r, g, b))


def drawSpace(w, user_colors, blend_color_list):
    global positions
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
                                  offset5300[1]+height5300,fill='cornsilk2')
    wean5302 = w.create_rectangle(offset5302[0], offset5302[1],  offset5302[0]+width5302,
                                  offset5302[1]+height5302,fill='cornsilk2')
    wean5304 = w.create_rectangle(offset5304[0], offset5304[1],  offset5304[0]+width5304,
                                  offset5304[1]+height5304,fill='cornsilk2')

    c1_index = 0
    c2_index = 0
    new_color = color_blend_2(user_colors[0][c1_index],user_colors[1][c2_index]);

    wean5300_positions[0] = w.create_rectangle(offset5300[0], offset5300[1], (offset5300[0]+(width5300/3)),
                                              (offset5300[1]+(height5300)) ,fill=str(user_colors[1][0].hex), outline='black')

    c1_index = 1
    c2_index = 1
    new_color = color_blend_2(user_colors[0][c1_index],user_colors[1][c2_index]);

    wean5300_positions[1] = w.create_rectangle((offset5300[0]+width5300/3), offset5300[1],  (offset5300[0]+(2*width5300/3)),
                                              (offset5300[1]+(height5300)) ,fill=str(user_colors[1][1].hex), outline='black')

    c1_index = 2
    c2_index = 2
    new_color = color_blend_2(user_colors[0][c1_index],user_colors[1][c2_index]);

    wean5300_positions[2] = w.create_rectangle((offset5300[0]+2*width5300/3), offset5300[1],  (offset5300[0]+(width5300)),
                                              (offset5300[1]+(height5300)) ,fill=str(user_colors[1][2].hex),outline='black')

    c1_index = 3
    c2_index = 3
    new_color = color_blend_2(user_colors[0][c1_index],user_colors[1][c2_index]);

    wean5302_positions[0] = w.create_rectangle(offset5302[0], offset5302[1],  (offset5302[0]+(width5302)/2),
                                              (offset5302[1]+(height5302)/2) ,fill=str(user_colors[1][3].hex), outline='black')

    c1_index = 4
    c2_index = 4
    new_color = color_blend_2(user_colors[0][c1_index],user_colors[1][c2_index]);

    wean5302_positions[1] = w.create_rectangle((offset5302[0]+width5302/2), offset5302[1],  (offset5302[0]+(width5302)),
                                              (offset5302[1]+(height5302)/2) ,fill=str(user_colors[1][4].hex),outline='black')
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

    legend_width = 220
    legend_height = 160
    legend_offset = 50
    legend_box = w.create_rectangle(WINDOW_WIDTH-legend_width, WINDOW_HEIGHT-legend_height,
                                    WINDOW_WIDTH-legend_offset, WINDOW_HEIGHT-50, fill='cornsilk2');

    legend_offset_h = 30
    legend_offset_w = 45
    margin = 10;
    user1_legend = w.create_rectangle(WINDOW_WIDTH-legend_width+margin, WINDOW_HEIGHT-legend_height+margin,
                                      WINDOW_WIDTH-legend_width+legend_offset_w,  WINDOW_HEIGHT-legend_height+legend_offset_h, fill='red');

    user1_txt = w.create_text(WINDOW_WIDTH-legend_height+margin,  WINDOW_HEIGHT-140, text="User 1")
    
    user2_legend = w.create_rectangle(WINDOW_WIDTH-legend_width+margin, WINDOW_HEIGHT-legend_height+margin+legend_offset_h,
                                      WINDOW_WIDTH-legend_width+legend_offset_w,  WINDOW_HEIGHT-legend_height+2*legend_offset_h, fill='blue');
    
    user2_txt = w.create_text(WINDOW_WIDTH-legend_height+margin,  WINDOW_HEIGHT-110, text="User 2")

    both_legend = w.create_rectangle(WINDOW_WIDTH-legend_width+margin, WINDOW_HEIGHT-legend_height+margin+2*legend_offset_h,
                                    WINDOW_WIDTH-legend_width+legend_offset_w, WINDOW_HEIGHT-legend_height+3*legend_offset_h, fill='DarkOrchid4');

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


def trackPerson(root):
    w = Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT,background='SkyBlue4')
    w.pack()
    user_colors = [ [Color(hex='#ff2a1a'),Color(hex='#f66340'),Color(hex='#f09063'),Color(hex='#edb284'),Color(hex='#eccba2')],
                                 [Color(hex='#021e97'), Color(hex='#032bc9'),Color(hex='#0435fb'),Color(hex='#365efc'),Color(hex='#6886fd')]]
    user_colors = [user_colors[0][::-1], user_colors[1][::-1]]
    blend_color_list = [Color((236, 198, 236)), Color((210, 121, 210)), Color((153, 51, 153)), Color((128, 0, 128)), Color((102, 0, 102))]

    # for i in xrange(len(user_colors[0])):
    #     blend_color_list.append(color_blend_2(user_colors[0][i], user_colors[1][i]));

    # print blend_color_list                   
    drawSpace(w, user_colors, blend_color_list);

    blacklist_dict = create_blacklist();
    clf_node_off_all = [clf_n0_off_all, clf_n1_off_all, clf_n2_off_all, clf_n3_off_all,
                        clf_n4_off_all, clf_n5_off_all]

    clf_node_off_distributed = [clf_n0_off_distributed, clf_n1_off_distributed, clf_n2_off_distributed,
                                clf_n3_off_distributed, clf_n4_off_distributed, clf_n5_off_distributed]

    clf_node_off_centralized = [clf_n0_off_centralized, clf_n1_off_centralized, clf_n2_off_centralized,
                                clf_n3_off_centralized, clf_n4_off_centralized, clf_n5_off_centralized]

    pred = [["","",""], ["","",""]]
    pred_d = [["","",""], ["","",""]]
    pred_c = [["","",""], ["","",""]]

    user_list = [User(0), User(1)];
    node_off = -1;
    node_off_count = [0, 0, 0, 0, 0, 0];
    count = 0;
    user_num = 0;
    #while (1): 
    time.sleep(0.25);
    count +=1;
    #receive data from server
    #call roomLocator instance
    #find line received for rssi values 
    #user 1 or user 2? roomLocator.user; 
    if (user_num == 1): 
        user_num = 0; #roomLocator.user; 
        rssi_values = [[-50, -60, -50, -59, -48, -41, -49, -89, -88, -90, -95, -96]];
    else:
        user_num = 1;
        rssi_values = [[-90, -90, -80, -89, -78, -71, -69, -79, -78, -70, -65, -60]];

    user = user_list[user_num]; 
    #node off depends on values received from either user
    for val in xrange((len(rssi_values[0])/2)):
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

    current_region = user.predictRegion(rssi_values, blacklist_dict, node_off, clf_room_all, clf5300_all, 
                                       clf5302_all, clf5304_all, clf_node_off_all); 
    current_region_c = user.predictRegion(rssi_values, blacklist_dict, node_off, clf_room_centralized,
                                         clf5300_centralized, clf5302_centralized, clf5304_centralized, 
                                         clf_node_off_centralized, "center"); 
    current_region_d = user.predictRegion(rssi_values, blacklist_dict, node_off, clf_room_distributed, 
                                         clf5300_distributed, clf5302_distributed, clf5304_distributed,
                                         clf_node_off_distributed, "dist"); 

    pred[user_num][user.i] = (current_region)
    pred_d[user_num][user.i] = (current_region_d)
    pred_c[user_num][user.i] = (current_region_c)
    user.i = (user.i+1)%3
    # I am overwriting the room in this block just for testing 
    if (user_num == 1): 
        user.current_region = random.choice(wean5304_names);

    else: 
        user.current_region = random.choice(wean5302_names);

    #print user.number, user.current_region;
    #user.clearPrevious(w);
    #user.drawCurrent(w, user_colors);

    user.addPath();
    user.previous_region = user.current_region;
    user.previous_region_d = user.current_region_d;
    user.previous_region_c = user.current_region_c;

    # if (user_list[0].current_region == user_list[1].current_region):
    #     index = names.index(user.current_region);
    #     w.itemconfig(positions[index], fill='DarkOrchid4');

#########################################################################3

#reactor.listenTCP(8125, RoomLocatorFactory())
# at this point build Tk app as usual using the root object,
# and start the program with "reactor.run()", and stop it
# with "reactor.stop()".

def main():
    root = Tk()
    root.title("BlueTrack")
    # Install the Reactor support
    tksupport.install(root)
    reactor.callInThread(trackPerson, root);
    reactor.run()

if __name__ == '__main__':
    main();