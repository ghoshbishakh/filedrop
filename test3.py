#!/usr/bin/python
import sys,socket
print "\n Welcome to filedrop \n"

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
MAX = 65535
PORT = 1060

if sys.argv[1:] == ["server"]:
	ip = raw_input("\n enter ip of your PC:\n")
	s.bind((ip, PORT))
	print "Listening at", s.getsockname()
	while True:
		data, address = s.recvfrom(MAX)
		print '\n The client at', address, 'says', repr(data)
		s.sendto("Your data was %d bytes" % len(data), address)

elif sys.argv[1:] == ['client']:
	ip = raw_input("\n enter ip of other PC:\n")
	print "\n Address before sending:", s.getsockname()
	text = "yo yo! time for action"
	s.sendto(text, (ip, PORT))
	print "\n Address after sending", s.getsockname()
	data, address = s.recvfrom(MAX)
	print "the server at", address, "says", repr(data)
	

	while text!="exit":
		text = raw_input("\n type message and press enter to send \n \t \t or \n type 'exit' to quit \t \t:")
		s.sendto(text, (ip, PORT))

else:
	print >>sys.stderr, 'usage: udp_local.py server|client'
