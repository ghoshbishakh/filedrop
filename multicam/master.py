#!/usr/bin/python
import os
import sys
import ConfigParser
#import PyGobject
from gi.repository import Gtk, GLib, Gdk, GdkX11
from libchat import *

# import pygame library for retrieving webcam image
import pygame.camera
import pygame.image
from pygame import Surface

import socket

#CONFIG----------------------------------
Config = ConfigParser.ConfigParser()
Config.read("master.conf")
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
print name


# GUI -------------------------------
# loading XML from glade file
GUIbuilder = Gtk.Builder()
GUIbuilder.add_from_file("sender-layout.glade")

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
        GLib.timeout_add_seconds(.1, updateImg)
        print "drawing"

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
#server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#server_socket.bind((socket.gethostname(), 5100))
#server_socket.listen(5)
#print "Your IP address is: ", socket.gethostbyname(socket.gethostname())

'''
# GET WEBCAM DATA BY PYGAME---------------
# Force SDL to write on our drawing area
os.putenv('SDL_WINDOWID', str(canvas.get_property('window').get_xid()))

# We need to flush the XLib event loop otherwise we can't
# access the XWindow which set_mode() requires
Gdk.flush()

pygame.init()
pygame.camera.init()

# get available video sources (cameras) & taking first one
cameras = pygame.camera.list_cameras()

print "available video sources are: \n %s \n" % (cameras)

webcam = pygame.camera.Camera(cameras[0])
print "selecting source: \n %s \n" % (cameras[0])
webcam.start()

# grabbing test image and getting its size
testImg = webcam.get_image()
print Surface.get_size(testImg)
(WINX, WINY) = Surface.get_size(testImg)
# setting screen according to size
pygame.display.set_mode((WINX, WINY), 0, 0)
screen = pygame.display.get_surface()
#screen.blit(testImg, (0, 0))
img = webcam.get_image()
#GLib.idle_add(pygame.display.update)
print "yoyo"
def updateImg():
    img = webcam.get_image()
    screen.blit(img, (0, 0))
    GLib.idle_add(pygame.display.update)
    return True
'''

Gtk.main()
