import pygame
from pygame.locals import *
import cv2
import numpy as np
import sys
import pickle
import socket
import os
import time
import struct

pygame.init()
pygame.display.set_caption("OpenCV camera stream on Pygame")
screen = pygame.display.set_mode([1040,720])


HOST = '172.20.10.2'  # The server's hostname or IP address
PORT = 2211        # The port used by the server



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data

try:
    while True:

        # Read message length and unpack it into an integer
        raw_msglen = recvall(s, 4)
        
        msglen = struct.unpack('>I', raw_msglen)[0]
     
        # Read the message data
        data =  recvall(s, msglen)
        
    
        print(len(data))

       
        
        
       
        frame6 = pickle.loads(data, fix_imports=True, encoding="bytes")
        frame6 = cv2.imdecode(frame6, 1)

    
        
        screen.fill([0,0,0])
        frame6 = cv2.cvtColor(frame6, cv2.COLOR_BGR2RGB)
        frame6 = np.rot90(frame6)
        frame6 = pygame.surfarray.make_surface(frame6)
        screen.blit(frame6, (0,0))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                sys.exit(0)
except (KeyboardInterrupt,SystemExit):
    pygame.quit()
    cv2.destroyAllWindows()
    s.close()


