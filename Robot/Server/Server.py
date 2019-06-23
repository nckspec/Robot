import sys
import socket
import io
import time






from Robot import Robot



#  Declare the pins that will be used
LEFT_STEP = 23;
LEFT_DIRECTION = 22;
RIGHT_STEP = 6;
RIGHT_DIRECTION = 16;


#  Set the ip address for the server
HOST = '172.20.10.2'

#  Set the port to be used
PORT = 2255



try:

    #  create the socket for the camera stream
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(1)

    #  Wait for an incoming connection
    conn, addr = s.accept()

    robot = Robot(conn, RIGHT_STEP, RIGHT_DIRECTION, LEFT_STEP, LEFT_DIRECTION)

    robot.camera.run()

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
            print(data)
            robot.goForward();


        #  IF a 'a' was received, then go left
        elif data == 'a':
            robot.goLeft();

        #  IF a 'd' was received, then go right
        elif data == 'd':
            robot.goRight();

        #  IF a 'sw', 'sa', or 'sd' was received then stop robot
        elif data == 'sw' or data == 'sa' or data == 'sd':
            robot.stop();

        #  PROCESSING: If the client sends 'ex' that means it has exited
        elif data == 'ex':
            break




finally:
        # When everything done, release the capture
        robot.camera.stop()
        time.sleep(5)
        s.shutdown(socket.SHUT_RDWR)
        s.close
        print('done')















