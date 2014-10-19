#!/usr/bin/python

# Import protocol, reactor and LineReceiver
from twisted.internet import protocol, reactor
from twisted.protocols.basic import LineReceiver

#Import JSON
import json


# PROTOCOL FUNCTIONS
def shoutCreator(message, fromUser):
    shout = {"usage": "shout", "data": {"from": fromUser, "message": message}}
    return json.dumps(shout)


# Chat Protocol
class chatProtocol(LineReceiver):

    def __init__(self, factory):
        self.factory = factory
        self.name = None
        self.state = "NOT_REGISTERED"

    def connectionMade(self):
        self.sendLine("What's your name?")

    def lineReceived(self, line):
        print line
        if self.state == "NOT_REGISTERED":
            self.registerUser(line)
        else:
            self.handleChat(line)

    def registerUser(self, name):
        if name in self.factory.users:
            self.sendLine("Name already taken, please choose another.")
            return
        else:
            self.factory.users[name] = self
            self.state = "REGISTERED"
            self.name = name
            self.sendLine("Welcome, %s!" % (name))
            self.factory.broadcastLine("%s has joined the chat room" % (name))
            print "%s has joined the chat room \n" % (name)

    def handleChat(self, message):
        self.factory.broadcastLine(message, self.name)

    def connectionLost(self, reason):
        if self.name in self.factory.users:
            del self.factory.users[self.name]
            self.factory.broadcastLine(
                "%s has left the chat room." % (self.name))
            print "%s has left the chat room. \n reason:%s" % (self.name, reason)

# Chat Factory


class chatFactory(protocol.Factory):

    def __init__(self):
        self.users = {}

    def broadcastLine(self, message, fromUser=None):
        shout = shoutCreator(message, fromUser)
        for name, Protocol in self.users.iteritems():
            Protocol.sendLine(shout)

    def buildProtocol(self, addr):
        print "recieved an new connection \n"
        return chatProtocol(self)


# Assign PORT and Start reactor
reactor.listenTCP(55667, chatFactory())
print "running reactor \n"
reactor.run()
