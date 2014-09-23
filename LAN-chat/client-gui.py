#IMPORT PGOBJECT
from gi.repository import Gtk


#GUI ------------

#loading XML from glade file
GUIbuilder = Gtk.Builder()
GUIbuilder.add_from_file("client-gui-layout.glade")

window = GUIbuilder.get_object("chatWindow")
chatTextBuffer = GUIbuilder.get_object("chatTextBuffer")


chatTextBuffer.set_text("THIS IS A TEST TEXT")
chatTextBuffer.set_text("THIS IS A TEST TEXT2")


class Handler:
	"""Contains the signal handlers"""
	def onDeleteWindow(self, *args):
		Gtk.main_quit(*args)

	def onSendButtonClick(self, *args):
		sendChat()

def sendChat():
	endIter= chatTextBuffer.get_end_iter()
	text = "\nYOYO"
	chatTextBuffer.insert(endIter, text, length=len(text))


GUIbuilder.connect_signals(Handler())

window.show_all()
Gtk.main()





