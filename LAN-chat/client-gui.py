#import and install gtk3reactor
from twisted.internet import gtk3reactor
gtk3reactor.install()

# Import protocol, reactor and LineReceiver
from twisted.internet import protocol,reactor
from twisted.protocols.basic import LineReceiver

#import PyGobject
from gi.repository import Gtk


#------------------CORE--------------------------

class chatClient(LineReceiver):
	def __init__(self):
		global thisClient
		thisClient=self

	def connectionMade(self):
		print "Connected! \n"

	def lineReceived(self, line):
		print line
		

	def sendChat(self, chat):
		self.sendLine(chat)




class clientFactory(protocol.ClientFactory):
	def buildProtocol(self, addr):
		return chatClient()



#GUI ------------

#loading XML from glade file
GUIbuilder = Gtk.Builder()
GUIbuilder.add_from_file("client-gui-layout.glade")

window = GUIbuilder.get_object("chatWindow")
chatTextBuffer = GUIbuilder.get_object("chatTextBuffer")
chatEntry= GUIbuilder.get_object("chatEntry")



class Handler:
	"""Contains the signal handlers"""
	def onDeleteWindow(self, *args):
		reactor.stop()

	def onSendButtonClick(self, *args):
		sendChatRequest()

def sendChatRequest():
	endIter= chatTextBuffer.get_end_iter()
	text = chatEntry.get_text()
	chatTextBuffer.insert(endIter, text, length=len(text))
	thisClient.sendChat(text)


GUIbuilder.connect_signals(Handler())

window.show_all()





#-------------run reactor loop-----------------------

reactor.connectTCP("localhost", 55667, clientFactory())
print "running reactor \n"
reactor.run()





