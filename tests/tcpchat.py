#! /usr/bin/python

import sys,socket
from threading import Thread

PORT=50607
USAGE="\n \t usage: tcpchat.py server|client <ip address of server>"

if len(sys.argv)==1:
	print USAGE
else:
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	def ClientRecv(sock):
		while True:
			data = sock.recv(1024)
			if not data: sys.exit(0)
			if str(data)=="stop":
				sys.exit(0)
			print data, "\n"
	def ClientSend(sock):
		while 1:
			message = raw_input(">>>")
			str(message)
			sock.sendall(message)



	print "\n \t Welcome to TCP chat"

	if sys.argv[1]=="server":
		if len(sys.argv)<3:
			print "\n \t Please specify your IP address"
			print USAGE
		else:
			HOST=sys.argv[2]


			s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			s.bind((HOST, PORT))
			s.listen(1)
			while True:
				SocketAddr=s.getsockname()
				print "listening at ", SocketAddr
				client, ClientAddr = s.accept()
				print "\n Accepted connection from", ClientAddr
				print "\n Connected is establishde between ", client.getsockname(), "and", client.getpeername()
				message = client.recv(16)
				print "Client's 16 bit message is", repr(message)
				client.sendall("\nClosing Connection")
				message = client.recv(16)
				print "Client's 16 bit message is", repr(message)
				client.close()
				print "Socket Closed"


	elif sys.argv[1]=="client":
		if len(sys.argv)<3:
			print "\n \t Please specify your IP address"
			print USAGE
		else:
			HOST=sys.argv[2]
			s.connect((HOST,PORT))
			print "\n Connected"
			ClientAddr=s.getsockname()
			print "\nclient has been assigned the address ", ClientAddr
			Thread(target=ClientRecv,args=(s,)).start()
			ClientSend(s)
			Thread(target=ClientRecv,args=(s,)).stop()
	else:
		print USAGE