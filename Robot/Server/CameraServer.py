import threading
import pickle
import picamera
import picamera.array
import socket
import struct
import cv2

class CameraServer:

    def __init__(self, conn):
        self.__conn = conn

    def run(self):
        self.__camServerOn = True
        self.__t1 = threading.Thread(target=self.startServer, args=())
        self.__t1.start()

    def stop(self):
        self.__camServerOn = False


    def startServer(self):


        #  Set the quality for the encoding of the jpeg to 90%
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

        try:

            while True:

                #  ret, frame = cap.read()

                #  result, frame = cv2.imencode('.jpg', frame, encode_param)

                #  declare a PiCamera object as camera
                with picamera.PiCamera() as camera:

                    # Create a RGB stream using the camera object
                    with picamera.array.PiRGBArray(camera) as stream:
                        #  Set the resolution as 720 by 720 and framerate at 30
                        camera.resolution = (720, 720)
                        camera.framerate = 30

                        #  Loop indefinitely
                        while self.__camServerOn:
                            #  Capture a frame using the RGB stream that was declared before
                            camera.capture(stream, 'bgr', use_video_port=True)

                            #  Create an an array out of the stream
                            buff = stream.array

                            # encode the camera stream array into a jpeg file
                            result, frame = cv2.imencode('.jpg', buff, encode_param)

                            # serialize the jpeg file
                            data = pickle.dumps(frame, 0)

                            # Prefix each message with a 4-byte length (network byte order)
                            msg = struct.pack('>I', len(data)) + data
                            self.__conn.sendall(msg)

                            # reset the stream before the next capture
                            stream.seek(0)
                            stream.truncate()
        finally:
            # When everything done, release the capture
            print('done')