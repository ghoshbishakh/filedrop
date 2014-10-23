from gi.repository import Gtk, GLib


class Handler():

    """Contains the signal handlers"""

    def on_mainWindow_delete_event(self, *args):
        Gtk.main_quit(*args)

    def sendButton_clicked(self, *args):
        pass

guiBuilder = Gtk.Builder()
guiBuilder.add_from_file("client-gui-layout2.glade")
window = guiBuilder.get_object("mainWindow")
guiBuilder.connect_signals(Handler())
window.show_all()
Gtk.main()
