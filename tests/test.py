#!/usr/bin/python
import sys,socket
print "\n Welcome to filedrop \n"

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
MAX = 65535
PORT = 1060

if sys.argv[1:] == ["server"]:
	s.bind(("127.0.0.1", PORT))
	print "Listening at", s.getsockname()
	while True:
		data, address = s.recvfrom(MAX)
		print '\n The client at', address, 'says', repr(data)
		s.sendto("Your data was %d bytes" % len(data), address)

elif sys.argv[1:] == ['client']:
	print "\n Address before sending:", s.getsockname()
	s.sendto("this is my message", ('127.0.0.1', PORT))
	print "\n Address after sending", s.getsockname()
	data, address = s.recvfrom(MAX)
	print "the server at", address, "says", repr(data)

else:
	print >>sys.stderr, 'usage: udp_local.py server|client'
