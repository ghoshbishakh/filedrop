#!/usr/bin/python

# Import protocol, reactor and LineReceiver
from twisted.internet import protocol, reactor
from twisted.protocols.basic import LineReceiver

# Import JSON
import json


# PROTOCOL FUNCTIONS
def handleChat(Protocol, line):
    inMessage = json.loads(str(line))
    usage = inMessage["usage"]
    if(usage == "shout"):
        username = Protocol.name
        message = inMessage["data"]
        outMessage = '{"usage":"shout", "data":{"from":"'+username+'", "message":"'+message+'"}'
        print outMessage
        Protocol.factory.sendChat("shout", outMessage)
    elif(usage == "whisper"):
        username = Protocol.name
        message = inMessage["data"]["message"]
        to = inMessage["data"]["to"]
        outMessage = '{"usage":"whisper", "data":{"from":"'+username+'", "message":"'+message+'"}}'
        print outMessage
        Protocol.factory.sendChat("whisper", outMessage, to)
    elif(usage == "getList"):
        List = list(Protocol.factory.users.keys())
        outMessage = '{"usage": "userList","data": '+str(List)+'}'
        Protocol.factory.sendChat("shout", outMessage)
    else:
        pass


def messageCreator(mode, message, fromUser):
    message = {"usage": mode, "data": {
        "from": fromUser, "message": message}}
    return json.dumps(message)


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
            handleChat(self, line)

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

    def sendChat(self, mode, message, to="All"):
        if(mode == "shout"):
            for name, Protocol in self.users.iteritems():
                Protocol.sendLine(str(message))
        if(mode == "whisper"):
            self.users[to].sendLine(str(message))

    def broadcastLine(self, message, fromUser=None):
        mode = "shout"
        shout = messageCreator(mode, message, fromUser)
        for name, Protocol in self.users.iteritems():
            Protocol.sendLine(shout)

    def whisper(self, message, fromUser, toUser):
        mode = "whisper"
        whisper = messageCreator(mode, message, fromUser)
        self.users[toUser].sendLine(whisper)

    def buildProtocol(self, addr):
        print "recieved an new connection \n"
        return chatProtocol(self)


# Assign PORT and Start reactor
reactor.listenTCP(55667, chatFactory())
print "running reactor \n"
reactor.run()
