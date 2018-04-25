import socket





s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 8000))
while (1):
    text = raw_input()
    if text == 'q':
        break
    s.sendall(text)
socket.close()