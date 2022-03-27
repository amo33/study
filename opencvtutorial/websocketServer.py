import asyncio
from opcode import hasfree
from pyrsistent import b
import websockets
import argparse
import base64, cv2
import numpy as np
import socket
import struct 
import pickle

ip = '192.168.1.3'
port = 50001 

server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

# 소켓 주소 정보 할당
server_socket.bind((ip, port))

data_buffer = b""

data_size = struct.calcsize('L')


def show_video(video):
    if video == 'default':
        cam = cv2.VideoCapture(0)
        cam.set(3, 1280)
        cam.set(4, 720)
        while True:
            hasframe, img = cam.read() # 캠 이미지 불러오기
            if hasframe:
                cv2.imshow("Cam Viewer",img) # 불러온 이미지 출력하기
            if cv2.waitKey(1) & 0xFF == 27: # esc 키를 누르면 닫음
                break
        cam.release()
        cv2.destroyAllWindows()
    else:
        path = 'videosrc/'+ video # video 파일경로 접근 

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Echo websocketServer --movie MOVIE")
    parser.add_argument('--movie', help = "video-directory", default= 'default')
    args = parser.parse_args()
    show_video(video = args.movie)
# https://blog.naver.com/PostView.nhn?blogId=dldudcks1779&logNo=222024824853
#https://mandloh.tistory.com/7
#https://85chong.tistory.com/79
