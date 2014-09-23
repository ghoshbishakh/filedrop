#IMPORT PGOBJECT
from gi.repository import Gtk


#GUI ------------


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
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()





