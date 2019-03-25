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

pygame.init()

HOST = '172.20.10.2'  # The server's hostname or IP address
PORT = 2255        # The port used by the server

key = ' '

pygame.display.set_caption("OpenCV camera stream on Pygame")
screen = pygame.display.set_mode([720,720])




def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data

def keysPressed():

    buttonsPressed = 0
    
    keys = pygame.key.get_pressed()
    for x in keys:
        if x == True:
            buttonsPressed += 1

    print(buttonsPressed)
    
    return buttonsPressed

def cam_stream():

    global screen
    global HOST
    port = 2250        # The port used by the server



    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, port))

    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    
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
            frame6 = cv2.flip(frame6, 1)
            frame6 = np.rot90(frame6)
            
            frame6 = pygame.surfarray.make_surface(frame6)
            screen.blit(frame6, (0,0))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    sys.exit(0)

    finally:
        s.shutdown(socket.SHUT_RDWR)
        s.close



cam = threading.Thread(target=cam_stream, args=())
cam.start()


try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))


    while True:



        for event in pygame.event.get():

                keys = pygame.key.get_pressed()

                if event.type == pygame.QUIT:
                    sys.exit()
                

                if keys[pygame.K_w] == True and keysPressed() == 1:
                    s.sendall('w'.encode())

                if keys[pygame.K_a] == True and keysPressed() == 1:
                    s.sendall('a'.encode())

                if keys[pygame.K_d] == True and keysPressed() == 1:
                    s.sendall('d'.encode())

                if event.type == pygame.KEYUP:
                    print('key up')
                    print
                    if keys[pygame.K_w] == False:
                        print('test1')
                        s.sendall('sw'.encode())


                    if keys[pygame.K_a] == False:
                        print('test2')
                        s.sendall('sa'.encode())

                    if keys[pygame.K_d] == False:
                        print('test2')
                        s.sendall('sd'.encode())

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


