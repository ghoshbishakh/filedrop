from twisted.internet import protocol,reactor

class echoProtocol(protocol.Protocol):
	def dataReceived(self, data):
		print data;
		self.transport.write(data)
		print "data sent back \n"

class echoFactory(protocol.Factory):
	def buildProtocol(self, addr):
		print "recieved connection \n"
		return echoProtocol()


reactor.listenTCP(55667, echoFactory())
print "run reactor \n"
reactor.run()
print "reactor running \n"