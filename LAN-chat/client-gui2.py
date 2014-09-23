#import and install gtk3reactor
from twisted.internet import gtk3reactor
gtk3reactor.install()

# Import protocol, reactor and LineReceiver
from twisted.internet import protocol,reactor
from twisted.protocols.basic import LineReceiver

#import PyGobject
from gi.repository import Gtk


#----------------------GUI-------------------
def closeAll(*args):
	reactor.stop()

class chatWindow(Gtk.Window):
	def __init__(self):
		Gtk.Window.__init__(self, title="LAN Chat")

		self.button = Gtk.Button(label="Click Here")
		self.button.connect("clicked", self.onButtonClick)
		self.add(self.button)
	def onButtonClick(self, widget):
		self.button.label="Clicked"
		self.button.set_label("Clicked!!")
		print "Clicked!!"
		

win = chatWindow()
win.connect("delete-event", closeAll)
win.show_all()



#------------------CORE--------------------------

class chatClient(LineReceiver):
	def connectionMade(self):
		print "Connected! \n"

	def lineReceived(self, line):
		print line
		

	def sendChat(self, chat):
		self.sendLine(chat)




class clientFactory(protocol.ClientFactory):
	def buildProtocol(self, addr):
		return chatClient()



#-------------run reactor loop-----------------------

reactor.connectTCP("localhost", 55667, clientFactory())
print "running reactor \n"
reactor.run()