import socket
import sys
import time
import pygame
import pygame.camera
from pygame.locals import *
from PIL import *

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("192.168.43.17", 50607))
server_socket.listen(50)


print "Your IP address is: ", socket.gethostbyname(socket.gethostname())

pygame.init()
pygame.camera.init()
cam = pygame.camera.Camera("/dev/video0", (640, 480))
cam.start()

screen = pygame.display.set_mode((640, 480))
i = 1
while 1:
    # Check if the exit button has been pressed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    client_socket, address = server_socket.accept()
    print i
    i += 1
    image = cam.get_image()
    data = pygame.image.tostring(image, "RGB", False)
    img = pygame.image.fromstring(data, (640, 480), "RGB")
    screen.blit(img, (0, 0))
    img = pygame.transform.scale(img, (80, 60))
    data = pygame.image.tostring(img, "RGB")
    client_socket.sendall(data)
    pygame.display.update()
