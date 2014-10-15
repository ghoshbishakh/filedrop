#! /use/bin/python

import socket
from time import sleep
PORT = 45678
broadcastSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
broadcastSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
while True:
    broadcastSocket.sendto('Broadcast message!', ('<broadcast>', PORT))
    sleep(2)
