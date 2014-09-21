
# Import protocol, reactor and LineReceiver
from twisted.internet import protocol,reactor
from twisted.protocols.basic import LineReceiver


#Chat Protocol
class chatProtocol(LineReceiver):
	def __init__(self, factory):
		self.factory=factory
		self.name=None
		self.state = "NOT_REGISTERED"

	def connectionMade(self):
		self.sendLine("What's your name?")

	def lineReceived(self, line):
		if self.state == "NOT_REGISTERED":
			self.registerUser(line)
		else:
			self.handleChat(line)

	def registerUser(self, name):
		if name in self.factory.users:
			self.sendLine("Name already taken, please choose another.")
			return
		else:
			self.factory.users[name]= self
			self.state= "REGISTERED"
			self.name= name
			self.sendLine("Welcome, %s!"%(name)) #######
			self.broadcastLine("%s has joined the chat room"%(name))
			print "%s has joined the chat room \n"%(name)

	def handleChat(self, message):
		message = "<%s>: %s "%(self.name, message)
		self.broadcastLine(message)

	def broadcastLine(self, line):
		for name, protocol in self.factory.users.iteritems():
			protocol.sendLine(line)


	def connectionLost(self, reason):
		if self.name in self.factory.users:
			del self.factory.users[self.name]
			self.broadcastLine("%s has left the chat room."%(self.name))
			print "%s has left the chat room. \n reason:"%(self.name, reason)

#Chat Factory
class chatFactory(protocol.Factory):
	def __init__(self):
		self.users= {}

	def buildProtocol(self, addr):
		print "recieved an new connection \n"
		return chatProtocol(self)



#Assign PORT and Start reactor

reactor.listenTCP(55667, chatFactory())
print "attempting to run reactor \n"
reactor.run()
