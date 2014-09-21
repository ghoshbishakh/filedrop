
# Import protocol, reactor and LineReceiver
from twisted.internet import protocol,reactor
from twisted.protocols.basic import LineReceiver

class chatClient(LineReceiver):
	def connectionMade(self):
		print "Connected! \n"

	def lineReceived(self, line):
		print line
		message = str(raw_input())
		self.sendChat(message)

	def sendChat(self, chat):
		self.sendLine(chat)




class clientFactory(protocol.ClientFactory):
	def buildProtocol(self, addr):
		return chatClient()

#Assign IP PORT and Start reciever
reactor.connectTCP("localhost", 55667, clientFactory())
print "running reactor \n"
reactor.run()
