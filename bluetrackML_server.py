
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

    HOST = ''
    PORT = 8001              # Arbitrary non-privileged port
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

    pred = ["","",""]
    pred_d = ["","",""]
    pred_c = ["","",""]

    previous_room = "";
    previous_room_d = "";
    previous_room_c = "";

    i = 0
    blacklist_count = 0;
    blacklist_count_c = 0;
    blacklist_count_d = 0;
    node_off = -1;
    node_off_count = [0, 0, 0, 0, 0, 0];
    while (1): 
        print "waiting for data"
        data = conn.recv(1024)
        print "data received: ", data
        try:
            timestamp,rssi_values = process_buffer(data)
            # print rssi_values;
        except:
            print "BAAAAAAAAAADDDDDDDDDD DATA"
            print data
        print "node off count:", node_off_count;
        print "lenght:", str((len(rssi_values[0])/2))

        current_room = "";
        current_room_d = "";
        current_room_c = "";

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

        # check if one of the nodes is off, -150 for over 10 seconds?
        # choose the correct clf
        #current_room = clf_room.predict(rssi_values)[0]
        if (node_off == -1):
            room = clf_room_all.predict(rssi_values)[0];
            room_d = clf_room_distributed.predict(rssi_values)[0];
            room_c = clf_room_centralized.predict(rssi_values)[0];
            if room == "5300":
              current_room = clf5300_all.predict(rssi_values)[0];
              current_room_d = clf5300_distributed.predict(rssi_values)[0];
              current_room_c = clf5300_centralized.predict(rssi_values)[0];

            elif room == "5302":
              current_room = clf5302_all.predict(rssi_values)[0];
              current_room_d = clf5302_distributed.predict(rssi_values)[0];
              current_room_c = clf5302_centralized.predict(rssi_values)[0];

            elif room == "5304":
              current_room = clf5304_all.predict(rssi_values)[0];
              current_room_d = clf5304_distributed.predict(rssi_values)[0];
              current_room_c = clf5304_centralized.predict(rssi_values)[0];

        elif (node_off == 0):
            print "node {} off".format(node_off)
            rssi_values = [rssi_values[0][:node_off*2] + rssi_values[0][node_off*2+2:]]
            current_room = clf_n0_off_all.predict(rssi_values)[0];
            current_room_d = clf_n0_off_distributed.predict(rssi_values)[0];
            current_room_c = clf_n0_off_centralized.predict(rssi_values)[0];

        elif (node_off == 1):
            print "node {} off".format(node_off)
            rssi_values = [rssi_values[0][:node_off*2] + rssi_values[0][node_off*2+2:]]
            print len(rssi_values)
            current_room = clf_n1_off_all.predict(rssi_values)[0];
            current_room_d = clf_n1_off_distributed.predict(rssi_values)[0];
            current_room_c = clf_n1_off_centralized.predict(rssi_values)[0];

        elif (node_off == 2):
            print "node {} off".format(node_off)
            rssi_values = [rssi_values[0][:node_off*2] + rssi_values[0][node_off*2+2:]]
            current_room = clf_n2_off_all.predict(rssi_values)[0];
            current_room_d = clf_n2_off_distributed.predict(rssi_values)[0];
            current_room_c = clf_n2_off_centralized.predict(rssi_values)[0];

        elif (node_off == 3):
            print "node {} off".format(node_off)
            rssi_values = [rssi_values[0][:node_off*2] + rssi_values[0][node_off*2+2:]]
            current_room = clf_n3_off_all.predict(rssi_values)[0];
            current_room_d = clf_n3_off_distributed.predict(rssi_values)[0];
            current_room_c = clf_n3_off_centralized.predict(rssi_values)[0];

        elif (node_off == 4):
            print "node {} off".format(node_off)
            rssi_values = [rssi_values[0][:node_off*2] + rssi_values[0][node_off*2+2:]]
            print len(rssi_values)
            current_room = clf_n4_off_all.predict(rssi_values)[0];
            current_room_d = clf_n4_off_distributed.predict(rssi_values)[0];
            current_room_c = clf_n4_off_centralized.predict(rssi_values)[0];

        elif (node_off == 5):
            print "node {} off".format(node_off)
            rssi_values = [rssi_values[0][:node_off*2] + rssi_values[0][node_off*2+2:]]
            current_room = clf_n5_off_all.predict(rssi_values)[0];
            current_room_d = clf_n5_off_distributed.predict(rssi_values)[0];
            current_room_c = clf_n5_off_centralized.predict(rssi_values)[0];
        if (previous_room == ""):
            previous_room = current_room;
        else:
            if (current_room.startswith(blacklist_dict[previous_room]) and (blacklist_count < 3)):
                blacklist_count += 1; 
                print bcolors.FAIL +  "blacklisting: " + current_room + bcolors.ENDC
                # do nothing
                continue;
            else:
                previous_room = current_room;
                blacklist_count = 0;

        if (previous_room_d == ""):
            previous_room_d = current_room_d;
        else:
            if (current_room_d.startswith(blacklist_dict[previous_room_d]) and (blacklist_count_d < 3)):
                blacklist_count_d += 1; 
                print bcolors.FAIL +  "blacklisting: " + current_room_d + bcolors.ENDC
                # do nothing
                continue;
            else:
                previous_room_d = current_room_d;
                blacklist_count_d = 0;

        if (previous_room_c == ""):
            previous_room_c = current_room_c;
        else:
            if (current_room_c.startswith(blacklist_dict[previous_room_c]) and (blacklist_count_c < 3)):
                blacklist_count_c += 1; 
                print bcolors.FAIL +  "blacklisting: " + current_room_c + bcolors.ENDC
                # do nothing
                continue;
            else:
                previous_room_c = current_room_c;
                blacklist_count_c = 0;

        pred[i] = (previous_room)
        pred_d[i] = (previous_room_d)
        pred_c[i] = (previous_room_c)


        i = (i+1)%3
        print "###################################################"
        print "_____ ALL ______"
        print pred, previous_room
        print bcolors.WARNING + max(pred, key=pred.count) + bcolors.ENDC

        print "_____ DIST ______"
        print pred_d, previous_room_d
        print bcolors.OKBLUE + max(pred_d, key=pred_d.count) + bcolors.ENDC

        print "_____ CENT ______"
        print pred_c, previous_room_c
        print bcolors.OKGREEN + max(pred_c, key=pred_c.count) + bcolors.ENDC


if __name__ == '__main__':
    main();