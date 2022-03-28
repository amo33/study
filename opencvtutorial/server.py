import asyncio
from http import server
from simple_websocket_server import WebSocketServer, WebSocket
import websockets
import argparse
import base64 ,cv2
import numpy as np
import warnings
import struct 
import pickle

warnings.simplefilter("ignore", DeprecationWarning)

def show_video(video):
        # 카메라 또는 동영상
        if video == 'default':
            capture = cv2.VideoCapture(0)
        else:
            path = 'videosrc/'+ video # video 파일경로 접근
            capture = cv2.VideoCapture(path)
        return capture

class SimpleShow(WebSocket):
    

    def handle(self, video):
        print(2)
        camera = show_video(video)
        while True:
            success, frame = camera.read()
            if not success:
                break
            else:
                #img = cv2.imdecode(np.fromstring(base64.b64decode(frame), np.uint8), cv2.IMREAD_COLOR)
                cv2.imshow('img',frame)
                cv2.waitKey(1)
                yield(b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Echo websocketClient --movie MOVIE")
    parser.add_argument('--movie', help = "video-directory", default= 'default')
    args = parser.parse_args()
    server = WebSocketServer('localhost', 5000, SimpleShow)
    server.serve_forever()


















'''
ip = '127.0.0.1'
port = 5000

server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

# 소켓 주소 정보 할당
server_socket.bind((ip, port))
server_socket.listen(5) # listen으로 할당 
client_socket , address = server_socket.accept()

data_buffer = b""

data_size = struct.calcsize('L')
print(1)
while True:
    while len(data_buffer) < data_size:
        data_buffer += client_socket.recv(4096)
    
    packed_data_size = data_buffer[:data_size]
    data_buffer = data_buffer[data_size:]

    frame_size = struct.unpack(">L",packed_data_size)[0]

    while len(data_buffer) < frame_size:
        data_buffer += client_socket.recv(4096)

    frame_data = data_buffer[:frame_size]
    data_buffer = data_buffer[frame_size:]

    frame_data = data_buffer[:frame_size]
    data_buffer = data_buffer[frame_size:]
    print(1)
    frame = pickle.loads(frame_data)

    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

    cv2.imshow('Frame', frame)
        
    if cv2.waitKey(1) & 0xFF == 27:
        break
client_socket.close()
server_socket.close()
print("done")
'''
# https://blog.naver.com/PostView.nhn?blogId=dldudcks1779&logNo=222024824853
#https://mandloh.tistory.com/7
#https://85chong.tistory.com/79
