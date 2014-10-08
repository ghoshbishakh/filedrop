#! /usr/bin/python

import socket
PORT = 45678
listnerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
listnerSocket.bind(('', PORT))
print 'Listening at', listnerSocket.getsockname()

while True:
    data, address = listnerSocket.recvfrom(1024)
    print 'The client at', address, 'says', repr(data)
    listnerSocket.sendto('Your data was %d bytes' % len(data), address)
