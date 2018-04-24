
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
    clf = joblib.load('training.pkl') 
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
    pred = ["","",""]
    previous_room = "";
    i = 0
    while (1): 
        data = conn.recv(1024)
        timestamp,rssi_values = process_buffer(data)
        # check if one of the nodes is off, -150 for over 10 seconds?
        # choose the correct clf
        current_room = clf.predict(rssi_values)[0]
        if (previous_room == ""):
            previous_room = current_room;
        else:
            #include here a list of all non-possible paths
            #if prediction is not possible, ignore
            #but also set a timer, it is only possible if time < ~20 seconds/some arbitrary number
            if (((previous_room[0:4] == '5302') and  (current_room[0:4] == '5304')) or
              ((previous_room[0:4] == '5304') and  (current_room[0:4] == '5302'))):
                # print previous_room, testY[i]; 
                # do nothing
                continue;
            else:
                previous_room = current_room;

        pred[i] = (previous_room)
        i = (i+1)%3
        print pred
        print previous_room
        print max(pred, key=pred.count)


if __name__ == '__main__':
    main();