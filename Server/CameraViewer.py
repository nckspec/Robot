import threading
import pickle
import struct
import cv2
import numpy as np
import pygame
from pygame.locals import *
import pygame.display
from functions import recvall

class CameraViewer:

    #  PROCESSING: Initialize object with the PyGame screen object and the socket object that it will be communicating
    #  through
    def __init__(self, screen, s):
        self.__screen = screen
        self.__s = s

    def start(self):

        #  Launch the cam stream as a separate thread
        t = threading.Thread(target=self.cam_stream, args=())
        t.start()


    def cam_stream(self):

        #  PROCESSING: parameters for encoding the frame as a jpeg
        #  sets the quality to 90 percent
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

        try:
            #  PROCESSING: Continues showing each frame of the stream
            while True:
                # Read message length and unpack it into an integer
                raw_msglen = recvall(self.__s, 4)

                msglen = struct.unpack('>I', raw_msglen)[0]

                # Read the message data
                data = recvall(self.__s, msglen)

                #  Deserialize the frame
                frame6 = pickle.loads(data, fix_imports=True, encoding="bytes")

                #  Decode the jpeg frame into a stream array
                frame6 = cv2.imdecode(frame6, 1)

                #  Fill the screen with white
                self.__screen.fill([0, 0, 0])

                #  Set the color of the frame
                frame6 = cv2.cvtColor(frame6, cv2.COLOR_BGR2RGB)

                #  Flip the frame
                frame6 = cv2.flip(frame6, 0)

                #  Rotate the frame by 90 degrees
                frame6 = np.rot90(frame6)

                #  Turn the frame into a pygame surface
                frame6 = pygame.surfarray.make_surface(frame6)

                #  Put the pygame surface to cover stream
                self.__screen.blit(frame6, (0, 0))

                #  Update the screen
                pygame.display.update()

        finally:
            print("done")