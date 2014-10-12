#! /usr/bin/python

import socket
from time import sleep
import threading


class udpBroadcasterThread(threading.Thread):

    """broadcast UDP sockets (process runs in a separate thread of control)"""

    def __init__(self, PORT, address='<broadcast>', threadName=None):
        threading.Thread.__init__(self)
        self.name = threadName
        self.PORT = PORT
        self.address = address
        self.exitFlag = 0

    def run(self):
        broadcastSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        broadcastSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        while(self.exitFlag == 0):
            broadcastSocket.sendto('filedrop_ping',
                                   (self.address, self.PORT))
            # print "broadcasting \n"
            sleep(2)

    def startBroadcast(self):
        self.exitFlag = 0
        self.start()

    def stopBroadcast(self):
        self.exitFlag = 1


class udpListenerThread(threading.Thread):

    """listen UDP broadcasts (process runs in a separate thread of control)"""

    def __init__(self, PORT, address='', threadName=None):
        threading.Thread.__init__(self)
        self.name = threadName
        self.PORT = PORT
        self.address = address
        self.nodes = {}
        self.exitFlag = 0

    def run(self):
        listenerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        listenerSocket.bind((self.address, self.PORT))
        while(self.exitFlag == 0):
            data, address = listenerSocket.recvfrom(1024)
            # print 'The client at', address, 'says', repr(data)
        #listenerSocket.sendto('Your data was %d bytes' % len(data), address)
            if(str(data) == 'filedrop_ping'):
                self.nodes[address] = 0
        listenerSocket.close()

    def getNodes(self):
        return self.nodes

    def increaseTime(self, key):
        self.nodes[key] += 2

    def expireNode(self, key):
        del self.nodes[key]

    def startListener(self):
        self.exitFlag = 0
        self.start()

    def stopListener(self):
        self.exitFlag = 1


class nodeCheckerThread(threading.Thread):

    """calculates time after last ping and timeouts nodes after s second.
    (runs in a separate thread of control)"""

    def __init__(self, listener, timeout=6, threadName=None):
        threading.Thread.__init__(self)
        self.listener = listener
        self.timeout = timeout
        self.exitFlag = 0

    def run(self):
        while(self.exitFlag == 0):
            nodes = self.listener.getNodes()
            print nodes
            for key in nodes.keys():
                if ((nodes[key]+2) >= self.timeout):
                    self.listener.expireNode(key)
                else:
                    self.listener.increaseTime(key)
            sleep(2)

    def startCheck(self):
        self.exitFlag = 0
        self.start()

    def stopCheck(self):
        self.exitFlag = 1


broadcaster = udpBroadcasterThread(45678)
listener = udpListenerThread(45678)
checker = nodeCheckerThread(listener)
