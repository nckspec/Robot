import time
import RPi.GPIO as GPIO;
import socket
import threading

from CameraCapture import CameraCapture

class Robot:




    def __init__(self, conn, rightStep, rightDirection, leftStep, leftDirection):

        self.__conn = conn

        self.__rightStep = rightStep
        self.__rightDirection = rightDirection
        self.__leftStep = leftStep
        self.__leftDirection = leftDirection
        self.camera = CameraCapture(conn)

        #  Setup the output pins that will be used
        GPIO.setmode(GPIO.BCM);
        GPIO.setup(rightStep, GPIO.OUT);
        GPIO.setup(rightDirection, GPIO.OUT);
        GPIO.setup(leftStep, GPIO.OUT);
        GPIO.setup(leftDirection, GPIO.OUT);

    def goForward(self):

        # Set the bool to true so that the start function will loop
        self.__isMotorOn = True

        # Set the direction of each motor so that they both move the robot forward
        GPIO.output(self.__rightDirection, 0)
        GPIO.output(self.__leftDirection, 1)

        # Launch the thread that will ultimately tell the motors to turn on
        t1 = threading.Thread(target=self.start, args=())
        t1.start()

    def goLeft(self):


        # Set the bool to true so that the start function will loop
        self.__isMotorOn = True

        # Set the direction of each motor - the left motor needs to go backwards and the right
        # needs to go forward
        GPIO.output(self.__rightDirection, 0)
        GPIO.output(self.__leftDirection, 0)

        # Launch the thread that will ultimately tell the motors to turn on
        t1 = threading.Thread(target=self.start, args=())
        t1.start()

    def goRight(self):

        # Set the bool to true so that the start function will loop
        self.__isMotorOn = True;

        # Set the direction of each motor - the right motor needs to go backwards and the keft
        # needs to go forward
        GPIO.output(self.__rightDirection, 1)
        GPIO.output(self.__leftDirection, 1)

        # Launch the thread that will ultimately tell the motors to turn on
        t1 = threading.Thread(target=self.start, args=())
        t1.start()

    def stop(self):

        # Set the bool to false so that the start() function will stop looping
        self.__isMotorOn = False;

        # Turn of the motors and reset the direction to 0
        GPIO.output(self.__rightStep, 0)
        GPIO.output(self.__leftStep, 0)
        GPIO.output(self.__rightDirection, 0)
        GPIO.output(self.__leftDirection, 0)

    def start(self):

        #  Loop until one of the other functions set self.isMotorOn to false
        while self.__isMotorOn:
            print("test")
            #  Simulate PWM by turning on the motors for 250 microseconds and then turn them
            #  off for 250 microseconds
            GPIO.output(self.__rightStep, 1)
            GPIO.output(self.__leftStep, 1)
            time.sleep(250 / 1000000)
            GPIO.output(self.__rightStep, 0)
            GPIO.output(self.__leftStep, 0)
            time.sleep(250 / 1000000)
