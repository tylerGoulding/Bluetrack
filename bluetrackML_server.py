
import math
import socket
from cStringIO import StringIO
import numpy as np
from sklearn.externals import joblib
import os
from sklearn.neighbors.nearest_centroid import NearestCentroid
from sklearn.externals import joblib

def process_buffer(buffer):
  timestamp = []
  rssi_values = []
  f = StringIO(buffer)
  for line in f:
    data = (line.strip()).split(',')
    timestamp.append(data[0])
    rssi_values.append(map(int,data[1:]))
  return timestamp, rssi_values

def main():
    #load all training models with one node off as well
    clf_room = joblib.load('knn_room.pkl')
    clf5300 = joblib.load('knn_region_given_5300.pkl');
    clf5302 = joblib.load('knn_region_given_5302.pkl'); 
    clf5304 = joblib.load('knn_region_given_5304.pkl'); 
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
    blacklist_dict['5302_upper_left_3'] = ('5304', '5300_middle','5300_upper', '5300_lower');
    blacklist_dict['5302_upper_right_3'] = ('5304', '5300_middle','5300_upper', '5300_lower');
    blacklist_dict['5302_lower_left_3'] = ('5304','5300_upper');
    blacklist_dict['5302_lower_right_3'] = ('5304','5300_upper');
    blacklist_dict['5302_middle_3'] = ('5304', '5300_middle','5300_upper');
    blacklist_dict['5304_upper_left_3'] = ('5302', '5300_middle','5300_upper', '5300_lower');
    blacklist_dict['5304_upper_right_3'] = ('5302', '5300_middle','5300_upper', '5300_lower');
    blacklist_dict['5304_lower_left_3'] = ('5302', '5300_lower');
    blacklist_dict['5304_lower_right_3'] = ('5302', '5300_lower');
    blacklist_dict['5300_lower_3'] = ('5300_upper', '5304', '5302_upper_right', '5302_upper_left');
    blacklist_dict['5300_middle_3'] = ('5304_upper_right', '5304_upper_left', '5302_upper_right', '5302_upper_left');
    blacklist_dict['5300_upper_3'] = ('5300_lower', '5302', '5304_upper_right', '5304_upper_left');

    pred = ["","",""]
    previous_room = "";
    i = 0
    blacklist_count = 0;
    while (1): 
        data = conn.recv(1024)
        timestamp,rssi_values = process_buffer(data)
        # check if one of the nodes is off, -150 for over 10 seconds?
        # choose the correct clf
        #current_room = clf_room.predict(rssi_values)[0]
        room = clf_room.predict(rssi_values)[0];
        if room == "5300":
          current_room = clf5300.predict(rssi_values)[0];
        elif room == "5302":
          current_room =clf5302.predict(rssi_values)[0];
        elif room == "5304":
          current_room = clf5304.predict(rssi_values)[0];

        if (previous_room == ""):
            previous_room = current_room;
        else:
            if (current_room.startswith(blacklist_dict[previous_room]) and (blacklist_count < 4)):
                blacklist_count += 1; 
                # do nothing
                continue;
            else:
                previous_room = current_room;
                blacklist_count = 0;

        pred[i] = (previous_room)
        i = (i+1)%3
        print pred
        print previous_room
        print max(pred, key=pred.count)


if __name__ == '__main__':
    main();