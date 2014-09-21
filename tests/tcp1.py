#! /usr/bin/env python

import socket, sys
print "Welcome to filedrop \n"

PORT=1060
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)




if sys.argv[1:]==["server"]:
	print "Enter your IP address \n"
	HOST=raw_input()
	
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind((HOST, PORT))
	s.listen(1)
	while True:
		ClientName=s.getsockname()
		print "listening at ", ClientName
		client, sockname = s.accept()
		print "\n Accepted connection from", sockname
		print "\n Connected to ", client.getsockname(), "and", client.getpeername()
		message = client.recv(16)
		print "Client's 16 bit message is", repr(message)
		client.sendall("\nClosing Connection")
		client.close()
		print "Socket Closed"

elif sys.argv[1:]==["client"]:
	print "Enter Server's IP address \n"
	HOST=raw_input()

	s.connect((HOST,PORT))
	ClientName=s.getsockname()
	print "\nclient has been assigned the name ", ClientName
	s.sendall("Hi there server dfsfdsfsfdfsfsfds 11")
	reply = s.recv(16)
	print "\n The server said", repr(reply)
	s.close()


else:
	print 'usage: tcp.py server|client'


