import asyncore
import socket

clients = {}
HOST = "127.0.0.1"
PORT = 50607
class MainServerSocket(asyncore.dispatcher):
    def __init__(self, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind((HOST,PORT))
        self.listen(5)
    def handle_accept(self):
        ClientSock, ClientAddr = self.accept( )
        clients[ClientAddr] = ClientSock
        print "Accepted connection from", ClientSock
        SecondaryServerSocket(ClientSock)

class SecondaryServerSocket(asyncore.dispatcher_with_send):
    def handle_read(self):
        receivedData = self.recv(8192)
        if receivedData:
            every = clients.values()
            for one in every:
                one.send(receivedData+'\n')
        else: self.close()
    def handle_close(self):
        print "Disconnected from", self.getpeername( )
        one = self.getpeername( )
        del clients[one]

MainServerSocket(21567)
asyncore.loop( )