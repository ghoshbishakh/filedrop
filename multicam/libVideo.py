import socket
import pygame
import Image
import threading
import sys


class videoListenerThread(threading.Thread):

    """listens video (process runs in a separate thread of control)"""

    def __init__(self, displayFunc, PORT=50607, address='192.168.43.17', threadName=None, ):
        threading.Thread.__init__(self)
        self.name = threadName
        self.PORT = PORT
        self.ADDRESS = address
        self.exitFlag = 0
        self.displayFunc = displayFunc

    def recv_all(sock, length):
        data = ''
        while len(data) < length:
            more = sock.recv(length - len(data))
            if not more:
                raise EOFError('socket closed %d bytes into a %d-byte message'% (len(data), length))
            data += more
        return data


    def run(self):
        pygame.init()
        clock = pygame.time.Clock()
        timer = 0
        previousImage = ""
        image = ""
        # Main thread loop:
        while(self.exitFlag == 0):

            # Check if the exit button has been pressed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            # timer to limit how many images we request from the server each
            # second:
            if timer < 1:
                # Create a socket connection for connecting to the server:
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect((str(self.ADDRESS), self.PORT))

                # Recieve data from the server:
                data = self.recv_all(client_socket, 1024000)
                print data

                # Set the timer back to 30:
                timer = 30

            else:

                # Count down the timer:
                timer -= 1

            # We store the previous recieved image incase the client fails to recive
            # all of the data for the new image:
            previousImage = image

            # We use a try clause to the program will not abort if there is an error:
            try:

            # We turn the data we revieved into a 120x90 PIL image:
                image = Image.fromstring("RGB", (80, 60), data)

            # We resize the image to 640x480:
                image = image.resize((640, 480))

            # We turn the PIL image into a surface that PyGame can display:
                image = pygame.image.frombuffer(image.tostring(), (640, 480), "RGB")

            except:

            # If we failed to recieve a new image we display the last image we revieved:
                image = previousImage

            # Set the var output to our image:
            output = image

            # We use PyGame to blit the output image to the screen:
            self.displayFunc(output)

            # We set our clock to tick 60 times a second, which limits the frame rate
            # to that amount:
            clock.tick(60)

    def startListener(self):
        self.exitFlag = 0
        self.start()

    def stopListener(self):
        self.exitFlag = 1