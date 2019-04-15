#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import pygame
import sys
import os
import pygame.display
import time
import pygame
from pygame.locals import *
import cv2
import numpy as np
import pickle
import socket
import struct
import threading

#  PROCESSING: Initialize pygame
pygame.init()


HOST = '172.20.10.2'    # The server's hostname or IP address
PORT = 2255             # The port used by the Robot Control Server

CAM_PORT = 2250

key = ' '

#  PROCESSING: Creates a window to display the cam stream and take input
pygame.display.set_caption("Roger")
screen = pygame.display.set_mode([720,720])



#  PROCESSING: Receives data from a socket
def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data

#  PROCESSING: Returns an integer that represents the number of buttons pressed
def keysPressed():

    #  PROCESSING: Initialize Variable
    buttonsPressed = 0

    #  PROCESSING: Store the pressed keys in the keys array
    keys = pygame.key.get_pressed()

    #  PROCESSING: Loops through pressed keys and increments buttons
    #  pressed by one
    for x in keys:
        if x == True:
            buttonsPressed += 1

    #  PROCESSING: Returns the amount of buttons pressed    
    return buttonsPressed

def cam_stream():

    #  PROCESSING: Allows the function to access the window that was
    #  delcared
    global screen

    #  PROCESSING: Allows the function to access the Host ip address
    #  of the server
    global HOST

    #  PROCESSING: Access to the CAM_PORT global variable
    global CAM_PORT      # The port used by the cam server

    #  PROCESSING: parameters for encoding the frame as a jpeg
    #  sets the quality to 90 percent
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

    #  PROCESSING: Opens a socket and connects to the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, CAM_PORT))

    
    
    try:
        #  PROCESSING: Continues showing each frame of the stream
        while True:

            # Read message length and unpack it into an integer
            raw_msglen = recvall(s, 4)
            
            msglen = struct.unpack('>I', raw_msglen)[0]
         
            # Read the message data
            data =  recvall(s, msglen)
            
        
           

           
            
            
            #  Deserialize the frame
            frame6 = pickle.loads(data, fix_imports=True, encoding="bytes")

            #  Decode the jpeg frame into a stream array
            frame6 = cv2.imdecode(frame6, 1)
 
            #  Fill the screen with white
            screen.fill([0,0,0])

            #  Set the color of the frame
            frame6 = cv2.cvtColor(frame6, cv2.COLOR_BGR2RGB)

            #  Flip the frame 
            frame6 = cv2.flip(frame6, 0)

            #  Rotate the frame by 90 degrees
            frame6 = np.rot90(frame6)

            #  Turn the frame into a pygame surface
            frame6 = pygame.surfarray.make_surface(frame6)

            #  Put the pygame surface to cover stream
            screen.blit(frame6, (0,0))

            #  Update the screen
            pygame.display.update()

    
    finally:

        #  Shutdown the socket
        s.shutdown(socket.SHUT_RDWR)
        s.close


#  Launch the cam stream
cam = threading.Thread(target=cam_stream, args=())
cam.start()


try:

    #  Create a socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))


    while True:


        #  Run this code when any key is pressed
        for event in pygame.event.get():

                #  Store all of the pressed keys
                keys = pygame.key.get_pressed()

                #  If you exit the pywindow, exit the program
                if event.type == pygame.QUIT:
                    sys.exit()
                
                #  If 'w' is pressed, send a 'w' to the server
                if keys[pygame.K_w] == True and keysPressed() == 1:
                    s.sendall('w'.encode())
                    
                #  If 'a' is pressed, send a 'a' to the server
                if keys[pygame.K_a] == True and keysPressed() == 1:
                    s.sendall('a'.encode())

                #  If 'd' is pressed, send a 'd' to the server
                if keys[pygame.K_d] == True and keysPressed() == 1:
                    s.sendall('d'.encode())

                #  If any key is released
                if event.type == pygame.KEYUP:

                    #  if 'w' was released, then send 'sw' to the server
                    if keys[pygame.K_w] == False:
                        s.sendall('sw'.encode())

                    #  if 'a' was released, then send 'sa' to the server
                    if keys[pygame.K_a] == False:
                        s.sendall('sa'.encode())

                    #  if 'd' was released, then send 'sd' to the server
                    if keys[pygame.K_d] == False: 
                        s.sendall('sd'.encode())

#  Shutdown the socket and close the socket, also close the pygame window
finally:
    s.shutdown(SHUT_RDWR)
    s.close()
    pygame.close()



                


                











#                elif event.key == pygame.K_d:
#                    GPIO.output(RIGHT, 1)
#                elif event.key == pygame.K_a:
#                    GPIO.output(LEFT, 1)
#            if event.type == pygame.KEYUP:

#                if event.key == pygame.K_w:

#                elif event.key == pygame.K_d:

#                elif event.key == pygame.K_a:


