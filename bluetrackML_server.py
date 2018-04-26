
import math
import socket
from cStringIO import StringIO
import numpy as np
from sklearn.externals import joblib
import os
from sklearn.neighbors.nearest_centroid import NearestCentroid
from sklearn.externals import joblib

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def process_buffer(buffer):
  timestamp = []
  rssi_values = []
  f = StringIO(buffer)
  for line in f:
    data = (line.strip()).split(',')
    timestamp.append(data[0])
    rssi_values.append(map(float,data[1:]))
  return timestamp, rssi_values

def main():
    #load all training models with one node off as well
    clf_room = joblib.load('knn_room.pkl')
    clf5300 = joblib.load('knn_region_given_5300.pkl');
    clf5302 = joblib.load('knn_region_given_5302.pkl'); 
    clf5304 = joblib.load('knn_region_given_5304.pkl'); 
    clf_n0_off = joblib.load('knn_region_node_0_off.pkl')
    clf_n1_off = joblib.load('knn_region_node_1_off.pkl')
    clf_n2_off = joblib.load('knn_region_node_2_off.pkl')
    clf_n3_off = joblib.load('knn_region_node_3_off.pkl')
    clf_n4_off = joblib.load('knn_region_node_4_off.pkl')
    clf_n5_off = joblib.load('knn_region_node_5_off.pkl')
    
    HOST = ''
    PORT = 8000              # Arbitrary non-privileged port
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    s.bind((HOST, PORT))
    print "Listening... "
    s.listen(1)
    conn, addr = s.accept()
    print "Accepted Connection:", addr

    blacklist_dict = {};
    blacklist_dict['5302_upper_left_4'] = ('5304', '5300_middle','5300_upper', '5300_lower');
    blacklist_dict['5302_upper_right_4'] = ('5304', '5300_middle','5300_upper', '5300_lower');
    blacklist_dict['5302_lower_left_4'] = ('5304','5300_upper');
    blacklist_dict['5302_lower_right_4'] = ('5304','5300_upper');
    blacklist_dict['5302_middle_4'] = ('5304', '5300_middle','5300_upper');
    blacklist_dict['5304_upper_left_4'] = ('5302', '5300_middle','5300_upper', '5300_lower');
    blacklist_dict['5304_upper_right_4'] = ('5302', '5300_middle','5300_upper', '5300_lower');
    blacklist_dict['5304_lower_left_4'] = ('5302', '5300_lower');
    blacklist_dict['5304_lower_right_4'] = ('5302', '5300_lower');
    blacklist_dict['5300_lower_4'] = ('5300_upper', '5304', '5302_upper_right', '5302_upper_left');
    blacklist_dict['5300_middle_4'] = ('5304_upper_right', '5304_upper_left', '5302_upper_right', '5302_upper_left');
    blacklist_dict['5300_upper_4'] = ('5300_lower', '5302', '5304_upper_right', '5304_upper_left');

    pred = ["","",""]
    previous_room = "";
    i = 0
    blacklist_count = 0;
    node_off = -1;
    node_off_count = [0, 0, 0, 0, 0, 0];
    while (1): 
        data = conn.recv(1024)
        timestamp,rssi_values = process_buffer(data)
        current_room = "";

        for val in xrange((len(rssi_values)/2)):
            if (rssi_values[val*2] == -150):
                if (node_off_count[val] > 3):
                    node_off = val;
                    break;
                else:
                    node_off_count[val] += 1; 
            else:
                node_off_count[val] = 0;
                node_off = -1; 

        # check if one of the nodes is off, -150 for over 10 seconds?
        # choose the correct clf
        #current_room = clf_room.predict(rssi_values)[0]
        if (node_off == -1):
            room = clf_room.predict(rssi_values)[0];
            if room == "5300":
              current_room = clf5300.predict(rssi_values)[0];
            elif room == "5302":
              current_room =clf5302.predict(rssi_values)[0];
            elif room == "5304":
              current_room = clf5304.predict(rssi_values)[0];

        elif (node_off == 0):
            current_room = clf_n0_off.predict(rssi_values)[0];

        elif (node_off == 1):
            current_room = clf_n1_off.predict(rssi_values)[0];

        elif (node_off == 2):
            current_room = clf_n2_off.predict(rssi_values)[0];

        elif (node_off == 3):
            current_room = clf_n3_off.predict(rssi_values)[0];

        elif (node_off == 4):
            current_room = clf_n4_off.predict(rssi_values)[0];

        elif (node_off == 5):
            current_room = clf_n5_off.predict(rssi_values)[0];

        if (previous_room == ""):
            previous_room = current_room;
        else:
            if (current_room.startswith(blacklist_dict[previous_room]) and (blacklist_count < 4)):
                blacklist_count += 1; 
                print bcolors.FAIL +  "blacklisting: " + current_room + bcolors.ENDC
                # do nothing
                continue;
            else:
                previous_room = current_room;
                blacklist_count = 0;

        pred[i] = (previous_room)
        i = (i+1)%3
        print pred, previous_room
        print bcolors.WARNING + max(pred, key=pred.count) + bcolors.ENDC


if __name__ == '__main__':
    main();