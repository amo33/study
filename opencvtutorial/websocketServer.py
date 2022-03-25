import asyncio
from opcode import hasfree
import websockets
import argparse
import cv2
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