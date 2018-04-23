
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
    i = 0
    while (1):
        
        data = conn.recv(1024)
        timestamp,rssi_values = process_buffer(data)
        # print   
        predict = clf.predict(rssi_values)
        pred[i] = (predict[0])
        i = (i+1)%3
        print pred
        print max(pred, key=pred.count)


if __name__ == '__main__':
    main();