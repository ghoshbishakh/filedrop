from twisted.internet import reactor,protocol

print "Starting Connection"

class echoClientProtocol(protocol.Protocol):
	def connectionMade(self):
		print "Sending Data \n"
		self.transport.write("Hello, World!")
		print "Data SENT \n"

	def dataReceived(self, data):
		print "Server said", data
		self.transport.loseConnection()

class echoFactory(protocol.ClientFactory):
	def buildProtocol(self, addr):
		return echoClientProtocol()

	def clientConnectionFailed(self, connector, reason):
		print "Connection Failed"
		reactor.stop()

	def clientConnectionLost(self, connector, reason):
		print "Connection Lost"
		reactor.stop()

reactor.connectTCP("localhost", 55667, echoFactory())
reactor.run()