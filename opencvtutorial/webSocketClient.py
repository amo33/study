import argparse
import base64, cv2
import numpy as np
import socketio
def show_video(video):
    sio = socketio.Client()
    sio.connect('http://localhost:5000', wait_timeout=10)
    # 카메라 또는 동영상
    if video == 'default':
        capture = cv2.VideoCapture(0)
    else:
        path = 'videosrc/'+ video # video 파일경로 접근
        capture = cv2.VideoCapture(path)

    # 프레임 크기 지정
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640) # 가로
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480) # 세로
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90] #변환 퀄리티 90프로로 지정

    while True:
        ret, frame = capture.read()
        cv2.imshow('text',frame)
        result, frame = cv2.imencode('.jpg',frame, encode_param)
        # 속도 높이기!!!!!!!!!!!!!!!!!!!!!!!!!
        b64data = base64.b64encode(frame)
        sio.emit('streaming', b64data)
        if cv2.waitKey(1)>0 : break
    sio.disconnect()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Echo websocketClient --movie MOVIE")
    parser.add_argument('--movie', help = "video-directory", default= 'default')
    args = parser.parse_args()
    show_video(video = args.movie)

