#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import pygame
import sys
import os
import pygame.display
import time

pygame.init()

HOST = '172.20.10.2'  # The server's hostname or IP address
PORT = 2255        # The port used by the server

key = ' '

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))


def keysPressed():

    buttonsPressed = 0
    
    keys = pygame.key.get_pressed()
    for x in keys:
        if x == True:
            buttonsPressed += 1

    print(buttonsPressed)
    
    return buttonsPressed


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



                


                












#                elif event.key == pygame.K_d:
#                    GPIO.output(RIGHT, 1)
#                elif event.key == pygame.K_a:
#                    GPIO.output(LEFT, 1)
#            if event.type == pygame.KEYUP:

#                if event.key == pygame.K_w:

#                elif event.key == pygame.K_d:

#                elif event.key == pygame.K_a:


