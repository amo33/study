from configparser import Interpolation
from curses import meta
import cv2
import argparse
import numpy as np 
print(cv2.__version__)
''' # 폴더 접근과 destroyallwindows 해결이 아직 안됨 
img1 = cv2.imread('opencvtutorial/resource/-1.jpeg')
print(type(img1))

if img1 is not None:
    cv2.imshow('image1', img1)
    cv2.waitKey()
    cv2.destroyAllWindows()
else:
    print("no image file")
'''

method_options = {}
#1. 크롭
method_options['resize'] = 'dsize=(640, 480), interpolation=cv2.INTER_AREA'
#2. 리사이즈
#3. grayscale
#4. rotation(각도 지정 가능)
#5. merge
#6. vstack, hstack


def handle_image(resource, modes, output): 
    path = resource+'/-1.jpeg' #opencvtutorial 폴더에서 실행했으므로 path도 그 안에 맞는 경로여야한다.
    img1 = cv2.imread(path)
    print(type(resource))
    print(modes)

    if img1 is not None:
       
       for mode in modes:
           
           if mode == 1:
               height , width = map(int, input("How much resize? Enter width and Height:").split())
               img1 = cv2.resize(img1,dsize=(height, width), interpolation=cv2.INTER_AREA )
           elif mode==2:
               x, w, y, h = map(int, input("Enter Crop territory starting with width part.(x,w,y,h)").split())
               img1 = img1[y:y+h, x:x+w]
           elif mode == 3:
               img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
           elif mode == 4:
               angle, scale = map(float, input("Type rotation angle in (90, 180, 270, 360) and Type scale (type 1 if you don't want to change scale):").split())
               height, width, channel = img1.shape
               print(height, width)
               matrix = cv2.getRotationMatrix2D((width/2, height/2), int(angle), scale)
               img1 = cv2.warpAffine(img1, matrix, (width, height))
           elif mode == 5:
               print(1)
           elif mode ==6:
               img1 = np.vstack(())
           elif mode == 7:
               img1 = np.hstack(())
       cv2.imwrite(output+'/'+'2.jpeg', img1)
       cv2.imshow('image1', img1)
       cv2.waitKey(1)
       cv2.destroyAllWindows()
       
    else:
        print("no image file")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Echo openc --img-dir IMG_DIR --mode MODE --result-dir RESULT_DIR") #Idir : input dir, Rdir: result dir
    parser.add_argument('--img-dir', help="Image_resource_dir",required=True)
    parser.add_argument('--mode', type = int ,help="Image_change_option", nargs='+', required=True)
    parser.add_argument('--result-dir', help="Image_output_dir" ,required=True)

    args = parser.parse_args()
    handle_image(resource = args.img_dir, modes = args.mode, output = args.result_dir) # No dictionary 형태 접근! args['mode'] -> Namespace is not subscriptable
                    # 근데 img-dir 인데 어떻게 img_dir로 접근할 수 있는거지? 이건 질문해야겠다... 
    '''
                args 네임 스페이스를 후 처리하고 값을 수동으로 분할 / 파싱
                사용자 정의 action를 정의하고 값을 수동으로 분할 / 파싱
                사용자 정의 type를 정의하고 값을 수동으로 분할 / 파싱
                하위 클래스 ArgumentParser 및 ArgumentParser.convert_arg_line_to_args 사용자 정의
                이 질문에 대해 Stack Overflow에서 비슷한 토론을 찾았습니다: https://stackoverflow.com/questions/48714523/


    '''