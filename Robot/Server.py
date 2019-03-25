import socket
import RPi.GPIO as GPIO;
import sys
import threading
import time

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

HOST = '192.168.1.73'
PORT = 2256

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()

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

    

print('Connected by', addr)
while True:
    data = conn.recv(2)
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

    
        
        
        
        





