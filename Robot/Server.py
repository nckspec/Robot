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


RIGHT_STEP = 23;
RIGHT_DIRECTION = 22;
LEFT_STEP = 6;
LEFT_DIRECTION = 16;
isMotorOn = False;

GPIO.setmode(GPIO.BCM);
GPIO.setup(RIGHT_STEP, GPIO.OUT);
GPIO.setup(RIGHT_DIRECTION, GPIO.OUT);
GPIO.setup(LEFT_STEP, GPIO.OUT);
GPIO.setup(LEFT_DIRECTION, GPIO.OUT);

HOST = '172.20.10.2'
PORT = 2255



def goForward():

    global isMotorOn
    isMotorOn = True;
    
    GPIO.output(RIGHT_DIRECTION, 0)
    GPIO.output(LEFT_DIRECTION, 1)
    
    t1 = threading.Thread(target=start, args=())
    t1.start()
    
    
    
    

def goLeft():

    global isMotorOn
    isMotorOn = True;
    
    GPIO.output(RIGHT_DIRECTION, 0)
    GPIO.output(LEFT_DIRECTION, 0)
    
    t1 = threading.Thread(target=start, args=())
    t1.start()

def goRight():

    global isMotorOn
    isMotorOn = True;
    
    GPIO.output(RIGHT_DIRECTION, 1)
    GPIO.output(LEFT_DIRECTION, 1)
    
    t1 = threading.Thread(target=start, args=())
    t1.start()

def stop():

    global isMotorOn
    isMotorOn = False;
    
    GPIO.output(RIGHT_STEP, 0)
    GPIO.output(LEFT_STEP, 0)
    GPIO.output(RIGHT_DIRECTION, 0)
    GPIO.output(LEFT_DIRECTION, 0)
    
    
def start():
    global isMotorOn
    while isMotorOn == True:
        GPIO.output(RIGHT_STEP, 1)
        GPIO.output(LEFT_STEP, 1)
        time.sleep(250/1000000)
        GPIO.output(RIGHT_STEP, 0)
        GPIO.output(LEFT_STEP, 0)
        time.sleep(250/1000000)

def cam_stream():

    global HOST
    port = 2250
    
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, port))
        s.listen(1)
        conn, addr = s.accept()

        
        while True:

            print(addr)

            #ret, frame = cap.read()

            #result, frame = cv2.imencode('.jpg', frame, encode_param)


            with picamera.PiCamera() as camera:
                with picamera.array.PiRGBArray(camera) as stream:
                    camera.resolution = (720, 720)
                    camera.framerate = 30

                    while True:
                        camera.capture(stream, 'bgr', use_video_port=True) 

                        buff = stream.array

                        
                        
                        result, frame = cv2.imencode('.jpg', buff, encode_param)
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

                        
cam = threading.Thread(target=cam_stream, args=())
cam.start()


try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)
    conn, addr = s.accept()


    print('Connected by', addr)
    while True:
        data = conn.recv(2)
        data = data.decode()
        if not data:
            break

        print(data)

        if data == 'w':
            goForward();


        elif data == 'a':
            goLeft();


        elif data == 'd':
            goRight();

        elif data == 'sw':
            stop();

        elif data == 'sa':
            stop();

        elif data == 'sd':
            stop();

finally:
        # When everything done, release the capture
        s.shutdown(socket.SHUT_RDWR)
        s.close
        print('done')  



    

 
        
        







