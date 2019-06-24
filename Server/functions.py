import threading
import pickle
import struct
import cv2
import numpy as np
import pygame
from pygame.locals import *
import pygame.display

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
