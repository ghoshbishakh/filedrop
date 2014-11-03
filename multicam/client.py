#!/usr/bin/python
import os
import sys
import ConfigParser
#import PyGobject
from gi.repository import Gtk, GLib, Gdk, GdkX11
#import my libs
from libchat import *
from libVideo import *
# import pygame library for retrieving webcam image
import pygame.image
from pygame import Surface
import Image

#CONFIG----------------------------------
Config = ConfigParser.ConfigParser()
Config.read("client.conf")
print Config.sections()

def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1

name = ConfigSectionMap("INFO")['name']
ip = ConfigSectionMap("INFO")['ip']
print name
print ip


# GUI -------------------------------
# loading XML from glade file
GUIbuilder = Gtk.Builder()
GUIbuilder.add_from_file("layout.glade")

window = GUIbuilder.get_object("chatWindow")
chatTextBuffer = GUIbuilder.get_object("chatTextBuffer")
chatEntry = GUIbuilder.get_object("chatEntry")
canvas = GUIbuilder.get_object("videoCanvas")
canvas.set_app_paintable(True)


class Handler:

    """Contains the signal handlers"""

    def onDeleteWindow(self, *args):
        Gtk.main_quit(*args)

    def onSendButtonClick(self, *args):
        sendChatRequest()

    def onPressEnter(self, *args):
        sendChatRequest()

    def startVideo(self, *args):
        #setCanvas()
        videoListener.startListener()

    def stopVideo(self, *args):
        videoListener.stopListener()

GUIbuilder.connect_signals(Handler())
window.show_all()

#CORE------------
def displayChat(text):
    endIter = chatTextBuffer.get_end_iter()
    message = "%s \n" % (text)
    chatTextBuffer.insert(endIter, message, length=len(message))


def sendChatRequest():
    endIter = chatTextBuffer.get_end_iter()
    text = chatEntry.get_text()
    text = name+": "+text
    sendSock(text)
    chatEntry.set_text("")

listener = listenerThread(displayFunc=displayChat)
listener.startListener()


##SOCKET INITIALIZE---------------------

client_socket_test = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket_test.connect(("192.168.43.17", 50607))
print "Your IP address is: ", socket.gethostbyname(socket.gethostname())


# GET WEBCAM DATA BY PYGAME---------------
# Force SDL to write on our drawing area
os.putenv('SDL_WINDOWID', str(canvas.get_property('window').get_xid()))

# We need to flush the XLib event loop otherwise we can't
# access the XWindow which set_mode() requires
Gdk.flush()

pygame.init()
data = client_socket_test.recv(1024000)
image = Image.fromstring("RGB", (80, 60), data)
image = image.resize((640, 480))
image = pygame.image.frombuffer(image.tostring(), (640, 480), "RGB")

print Surface.get_size(image)
(WINX, WINY) = Surface.get_size(image)
# setting screen according to size
pygame.display.set_mode((WINX, WINY), 0, 0)
screen = pygame.display.get_surface()
#screen.blit(image, (0, 0))
#GLib.idle_add(pygame.display.update)
print "yoyo"

def updateImg(output):
    screen.blit(output, (0, 0))
    GLib.idle_add(pygame.display.update)
    print "boom"
    return True

videoListener = videoListenerThread(displayFunc=updateImg)



Gtk.main()
