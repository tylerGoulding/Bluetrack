import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 8001)
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)

# #### facilitate programming between Project Memebers
# dirname_tyler = "/Users/Tyler/Documents/GitHub/Bluetrack/"
# dirname_fatema = "C:\\Users\\Fatema Almeshqab\\Desktop\\Bluetrack\\"
# if platform.system() == 'Darwin':
#   dirname = dirname_tyler
# else:
#   dirname = dirname_fatema
#   for folder in data_folders:
#     new_dirname = dirname + folder;
#     for filename in os.listdir(new_dirname):
#       root, ext = os.path.splitext(filename)
#       # if "middle_5" in root:
#       #   continue;
#       root = root[:-2];
#       if root not in regions:
#         regions.append(root);

#       file = new_dirname + filename
#       features = [];
#       room_level_Y = [];
#       if root not in rawData:
#         rawData[root] = [];

# self.current_region



try:
    while(1):
        # Send data
        message = raw_input()
        print >>sys.stderr, 'sending "%s"' % message
        sock.sendall(message)

        # Look for the response
        # amount_received = 0
        # amount_expected = len(message)
        
        # while amount_received < amount_expected:
        # data = sock.recv(1024)
        # # amount_received += len(data)
        # if data != none:
        #     print >>sys.stderr, 'received "%s"' % data

finally:
    print >>sys.stderr, 'closing socket'
    sock.close()