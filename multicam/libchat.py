import threading

import socket
import struct


class listenerThread(threading.Thread):

    """listens multicasts (process runs in a separate thread of control)"""

    def __init__(self, displayFunc, PORT=5678, address='224.1.1.1', threadName=None, ):
        threading.Thread.__init__(self)
        self.name = threadName
        self.PORT = PORT
        self.GROUP = address
        self.exitFlag = 0
        self.displayFunc = displayFunc

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.GROUP, self.PORT))
        mreq = struct.pack("4sl", socket.inet_aton(self.GROUP), socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        print "listening..."
        while(self.exitFlag == 0):
            text = sock.recv(10240)
            if(text == "0000"):
                break
            self.displayFunc(text)
            print text
        sock.close()
        print "stopped"

    def startListener(self):
        self.exitFlag = 0
        self.start()

    def stopListener(self):
        self.exitFlag = 1


GROUP = '224.1.1.1'
PORT = 5678

sendsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sendsock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
def sendSock(text):
    sendsock.sendto(text, (GROUP, PORT))