#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import sys
import os
import pygame.display
import time
import pygame
from pygame.locals import *
import pickle
import struct
import socket

from CameraViewer import CameraViewer
from functions import recvall, keysPressed

#  PROCESSING: Initialize pygame
pygame.init()

#  PROCESSING: Constants holding the host's ip address and it's port number
HOST = '192.168.1.70'    # The server's hostname or IP address
PORT = 2255             # The port used by the Robot Control Server

#  PROCESSING: Creates a window to display the cam stream and take input
pygame.display.set_caption("Roger")
screen = pygame.display.set_mode([720,720])





#  create the socket for the camera stream
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(1)

#  Wait for an incoming connection
conn, addr = s.accept()

#  Create a camStream object that is initialized with the PyGame screen and the socket we just opened
camStream = CameraViewer(screen, conn)

#  PROCESSING: Start the camStream
camStream.start()


try:


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
                    conn.sendall('w'.encode())
                    
                #  If 'a' is pressed, send a 'a' to the server
                if keys[pygame.K_a] == True and keysPressed() == 1:
                    conn.sendall('a'.encode())

                #  If 'd' is pressed, send a 'd' to the server
                if keys[pygame.K_d] == True and keysPressed() == 1:
                    conn.sendall('d'.encode())

                #  If any key is released
                if event.type == pygame.KEYUP:

                    #  if 'w' was released, then send 'sw' to the server
                    if keys[pygame.K_w] == False:
                        conn.sendall('sw'.encode())

                    #  if 'a' was released, then send 'sa' to the server
                    if keys[pygame.K_a] == False:
                        conn.sendall('sa'.encode())

                    #  if 'd' was released, then send 'sd' to the server
                    if keys[pygame.K_d] == False: 
                        conn.sendall('sd'.encode())


finally:

    #  PROCESSING: Close the socket
    s.shutdown(socket.SHUT_WR)
    s.close()

    #  PROCESSING: Exit the Pygame Window
    pygame.quit()
