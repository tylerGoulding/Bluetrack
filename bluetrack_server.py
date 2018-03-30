#https://codeshare.io/2KPqzE

class Room(object):
  def __init__(self,corners):
    self.corners = corners
  def isValidPosition(x,y):
    #idk implement some check to see if its inside the room
    return True

class Location(object):
  def __init__(self,name,x = 0,y = 0):
    self.name = name;
    self.x = x;
    self.y = y;
  def getDist(x1,y1):
    return math.sqrt(((x1-self.x)**2) + ((y1-self.y)**2))
  
class beacon(Location):
  def __init__(self,name,x = 0,y = 0):
    self.name = name;
    self.x = x;
    self.y = y;

######################################################################################

import math
import socket
from cStringIO import StringIO

HOST = ''                 
PORT = 50009              # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

tx_power = -60 #find actual value -- rssi at 1 meter
N = 3 #number of beacons
M = 8 #number of locations (this should be more like 20)
#change these to actual values

possible_locations = [(1,1), (3,1), (3,2), (1,3), (2,5), (2,6), (3,7), (1,7)] 
beacons_locations = [(0,0), (0,4), (0,8)]#, (8,8), (4,4), (4,0)]
path = []

#fill in dictionary. key = location name
#value = list of distances from the key to each beacon location

# def recv_all(the_socket):
#     total_data=[]
#     while True:
#         data = the_socket.recv(1024)
#         if not data: break
#         total_data.append(data)
#     return ''.join(total_data)
  
#in csv format of timestamp,rssi_values  
def process_buffer(buffer):
  timestamp = []
  rssi_values = []
  f = StringIO(buffer)
  for line in f:
    data = (line.strip()).split(',')
    timestamp.append(data[0])
    rssi_values.append(map(int,data[1:]))
  return timestamp, rssi_values
  
def calculate_distances():  
  all_distances = {}
  #initialize dictionary with all distances between location and beacons
  #this will be NxM
  for i in xrange(M):
    key = "m" + str(i);
    all_distances[key] = [];
    x0,y0 = possible_locations[i]
    for x1,y1 in beacons_locations:
      distance = math.sqrt(((x1-x0)**2) + ((y1-y0)**2)) 
      all_distances[key].append(distance)
      
  return all_distances
    
#set up socket to connect to

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s.bind((HOST, PORT))
print "Listening... "
s.listen(1)
conn, addr = s.accept()
print "Accepted Connection:", addr


all_distances = calculate_distances()
rssi_values = []
estimated_distance = []
test_data = [("00:00,-60,-70,-74,-85,-78,-70\n"
    "00:02,-65,-71,-74,-82,-72,-69\n"
    "00:04,-60,-70,-74,-85,-78,-68\n"
    "00:06,-75,-78,-88,-85,-73,-70"), ("00:08,-70,-66,-85,-78,-62,-70\n"
    "00:10,-70,-65,-72,-85,-76,-79\n"
    "00:12,-60,-70,-74,-85,-78,-68\n"
    "00:14,-75,-78,-88,-85,-73,-70"), ("00:16,-73,-73,-77,-78,-67,-69\n"
    "00:18,-77,-63,-75,-75,-63,-77\n"
    "00:20,-76,-71,-66,-75,-67,-76\n"
    "00:22,-85,-68,-66,-65,-67,-86")]

print all_distances
count = 0
while (1):
  count += 1
  rssi_values = []
  data = conn.recv(1024)
  print data
  # data = recv_all(conn);
  time_stamp, rssi_values = process_buffer(data)
  for position in xrange(len(rssi_values)):
    min_error = 1000
    estimated_location = (0,0)
    estimated_distance = []
    for rssi in rssi_values[position]:
      d = 10**((int(rssi)-tx_power)/(-20.0))
      estimated_distance.append(d)
    print estimated_distance

    #now we filled the estimated distance d0-d5 from each beacon
    #compare with actual distance
    for i in xrange(M):
      mean_squared_error = 0
      key = "m" + str(i)

      for j,distance in enumerate(all_distances[key]):
        mean_squared_error += (estimated_distance[j] - distance)**2
      mean_squared_error /= float(N)
      if (mean_squared_error < min_error):
        min_error = mean_squared_error
        estimated_location = possible_locations[i]

    print (time_stamp[position] + " " + str(estimated_location))
    path.append((time_stamp[position],estimated_location))

print path
