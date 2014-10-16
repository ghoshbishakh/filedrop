from gi.repository import Gtk, GLib
from libdiscovery import *


def updateNodes(listStore, listener):
    nodelist = listener.getNodes()
    listStore.append([str(nodelist)])
    return True


def connect():
    broadcaster.startBroadcast()
    listener.startListener()
    checker.startCheck()


def disconnect():
    broadcaster.stopBroadcast()
    #listener.stopListener()
    #checker.stopCheck()


class Handler():
    """signal handlers for gui"""
    def onDeleteWindow(self, *args):
        Gtk.main_quit(*args)

    def connectButton_clicked(*args):
        nodeList.remove(connectButton)
        nodeList.pack_start(disconnectButton, False, False, 0)
        nodeList.pack_start(spinner, False, False, 0)
        connect()
        listStore = Gtk.ListStore(str)
        nodelist = listener.getNodes()
        listStore.append([str(nodelist)])
        listView = Gtk.TreeView(model=listStore)
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Title", renderer, text=0)
        listView.append_column(column)
        nodeList.remove(spinner)
        nodeList.pack_start(listView, False, False, 0)
        window.show_all()
        GLib.timeout_add_seconds(2, updateNodes, listStore, listener)

    def disconnectButton_clicked(*args):
        disconnect()

guiBuilder = Gtk.Builder()
guiBuilder.add_from_file('discovery.glade')
guiBuilder.connect_signals(Handler())

disconnectButton = guiBuilder.get_object('disconnectButton')
spinner = guiBuilder.get_object('spinner')
connectButton = guiBuilder.get_object('connectButton')
nodeList = guiBuilder.get_object('nodeList')
window = guiBuilder.get_object('nginxDiscovery')

window.show_all()
Gtk.main()
