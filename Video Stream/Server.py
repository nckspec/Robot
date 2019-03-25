import io
import numpy as np
import cv2
import socket
import pickle
import picamera
import picamera.array
import time
import struct


HOST = '172.20.10.2'  # The server's hostname or IP address
PORT = 2211      # The port used by the server




encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
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
    cap.release()
    cv2.destroyAllWindows()
    s.close()
    print('done')
