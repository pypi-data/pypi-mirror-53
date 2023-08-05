#! /usr/bin/python3

import socket
from eyespy.camera import PlayStationEye
import argparse

def init_server(host, port, dst):
    """
    """
    
    eye = PlayStationEye()
    
    if dst == 'auto':
        dst = '/Users/jbhunt/Desktop/test.avi'
    
    # network communication
    
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind((host,port))
    s.listen()
    
    while True:
        
        print('Waiting for connection ...')
        conn, (addr,port) = s.accept()
        print('Connection with {}'.format(addr))
        
        # wait for command to start video recording
        while conn.recv(1024).decode() != 'start':
            continue
        
        eye.start_video_capture(dst)
        print('Video capture started')
        
        # wait for command to stop vide0 recording
        while conn.recv(1024).decode() != 'stop': 
            continue
        
        eye.stop_video_capture()
        print('Video capture stopped')
        mean_frame_interval = 1/(sum(eye.intervals)/len(eye.intervals))
        print('Mean frame rate was {0:.2f}fps'.format(mean_frame_interval))
        break
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, default='169.254.203.219')
    parser.add_argument('--port', type=int, default=9001)
    parser.add_argument('--dst', type=str, default='auto')
    results = parser.parse_args()
    init_server(results.host, results.port, results.dst)