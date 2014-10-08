#! /usr/bin/python

import socket
from time import sleep

discoveredNodes = {}


def handleBroadcast(ip, message):
    discoveredNodes[ip] = str(message)
    print discoveredNodes


class udpBroadcaster(object):

    """broadcast UDP packets"""

    def __init__(self, PORT, address='<broadcast>'):
        self.address = address
        self.PORT = PORT

    def start(self):
        broadcastSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        broadcastSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        while True:
            broadcastSocket.sendto('Broadcast message!',
                                   (self.address, self.PORT))
            print "broadcasting \n"
            sleep(2)


class udpListner(object):
    """listen UDP broadcasts"""
    def __init__(self, PORT, address=''):
        self.PORT = PORT
        self.address = address

    def start(self):
        listnerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        listnerSocket.bind((self.address, self.PORT))
        while True:
            data, address = listnerSocket.recvfrom(1024)
            print 'The client at', address, 'says', repr(data)
#listnerSocket.sendto('Your data was %d bytes' % len(data), address)
            handleBroadcast(address, data)
