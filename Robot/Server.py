import socket
import RPi.GPIO as GPIO;
import sys
import threading
import time
import io
import numpy as np
import cv2
import socket
import pickle
import picamera
import picamera.array
import time
import struct


#  Declare the pins that will be used
LEFT_STEP = 23;
LEFT_DIRECTION = 22;
RIGHT_STEP = 6;
RIGHT_DIRECTION = 16;

#  Initialize this bool to false
isMotorOn = False;

#  Setup the output pins that will be used
GPIO.setmode(GPIO.BCM);
GPIO.setup(RIGHT_STEP, GPIO.OUT);
GPIO.setup(RIGHT_DIRECTION, GPIO.OUT);
GPIO.setup(LEFT_STEP, GPIO.OUT);
GPIO.setup(LEFT_DIRECTION, GPIO.OUT);


#  Set the ip address for the server
HOST = '172.20.10.2'

#  Set the port to be used
PORT = 2255



def goForward():

    #Import the global variable into this function
    global isMotorOn

    #Set the bool to true so that the start function will loop
    isMotorOn = True;

    #Set the direction of each motor so that they both move the robot forward
    GPIO.output(RIGHT_DIRECTION, 0)
    GPIO.output(LEFT_DIRECTION, 1)

    #Launch the thread that will ultimately tell the motors to turn on
    t1 = threading.Thread(target=start, args=())
    t1.start()
    
    
    
    

def goLeft():
    
    #Import the global variable into this function
    global isMotorOn

    #Set the bool to true so that the start function will loop
    isMotorOn = True;

    #Set the direction of each motor - the left motor needs to go backwards and the right
    #needs to go forward
    GPIO.output(RIGHT_DIRECTION, 0)
    GPIO.output(LEFT_DIRECTION, 0)

    #Launch the thread that will ultimately tell the motors to turn on
    t1 = threading.Thread(target=start, args=())
    t1.start()

def goRight():

    #Import the global variable into this function
    global isMotorOn

    #Set the bool to true so that the start function will loop
    isMotorOn = True;

    #Set the direction of each motor - the right motor needs to go backwards and the keft
    #needs to go forward
    GPIO.output(RIGHT_DIRECTION, 1)
    GPIO.output(LEFT_DIRECTION, 1)

    #Launch the thread that will ultimately tell the motors to turn on
    t1 = threading.Thread(target=start, args=())
    t1.start()

def stop():

    #Import the global variable into this function
    global isMotorOn

    #Set the bool to false so that the start() function will stop looping
    isMotorOn = False;

    # Turn of the motors and reset the direction to 0
    GPIO.output(RIGHT_STEP, 0)
    GPIO.output(LEFT_STEP, 0)
    GPIO.output(RIGHT_DIRECTION, 0)
    GPIO.output(LEFT_DIRECTION, 0)
    
    
def start():
    #Import the global variable into this function
    global isMotorOn

    #  Loop until one of the other functions set isMotorOn to false
    while isMotorOn == True:

        #  Simulate PWM by turning on the motors for 250 microseconds and then turn them
        #  off for 250 microseconds
        GPIO.output(RIGHT_STEP, 1)
        GPIO.output(LEFT_STEP, 1)
        time.sleep(250/1000000)
        GPIO.output(RIGHT_STEP, 0)
        GPIO.output(LEFT_STEP, 0)
        time.sleep(250/1000000)

def cam_stream():

    #  Import the globabl variable HOST
    global HOST

    #  Set the port to 2250
    port = 2250

    #  Set the quality for the encoding of the jpeg to 90%
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    

    try:

        #create the socket for the camera stream
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, port))
        s.listen(1)

        #Wait for a connection from the client on the camera stream
        conn, addr = s.accept()

        
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
                    while True:

                        #  Capture a frame using the RGB stream that was declared before
                        camera.capture(stream, 'bgr', use_video_port=True) 

                        #  Create an an array out of the stream
                        buff = stream.array

                        
                        #encode the camera stream array into a jpeg file
                        result, frame = cv2.imencode('.jpg', buff, encode_param)

                        #serialize the jpeg file
                        data = pickle.dumps(frame, 0)
                       
                        # Prefix each message with a 4-byte length (network byte order)
                        msg = struct.pack('>I', len(data)) + data
                        conn.sendall(msg)
                        
                        # reset the stream before the next capture
                        stream.seek(0)
                        stream.truncate()
    finally:
        # When everything done, release the capture
        cv2.destroyAllWindows()
        s.shutdown(socket.SHUT_RDWR)
        s.close
        print('done')  


#  Start the camera stream                     
cam = threading.Thread(target=cam_stream, args=())
cam.start()



try:

    #  create the socket for the camera stream
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)

    #  Wait for an incoming connection
    conn, addr = s.accept()


    print('Connected by', addr)
    while True:

        #  Receive the 2 bytes of data containing the command from the client
        data = conn.recv(2)

        #  Decode the 2 bytes of data
        data = data.decode()
        if not data:
            break

       
        #  IF a 'w' was received, then go forward
        if data == 'w':
            goForward();

        #  IF a 'a' was received, then go left
        elif data == 'a':
            goLeft();

        #  IF a 'd' was received, then go right
        elif data == 'd':
            goRight();

        #  IF a 'sw' was received, then stop
        elif data == 'sw':
            stop();

        #  IF a 'sa' was received, then stop
        elif data == 'sa':
            stop();

        #  IF a 'sd' was received, then stop
        elif data == 'sd':
            stop();

finally:
        # When everything done, release the capture
        s.shutdown(socket.SHUT_RDWR)
        s.close
        print('done')  



    

 
        
        







