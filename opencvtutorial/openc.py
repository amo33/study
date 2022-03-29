import cv2
import argparse
import numpy as np 
import os,time
''' # 폴더 접근과 destroyallwindows 해결이 아직 안됨 
img1 = cv2.imread('opencvtutorial/resource/-1.jpeg')
print(type(img1))

if img1 is not None:
    cv2.imshow('image1', img1)
    cv2.waitKey()
    cv2.destroyAllWindows()
else:
    print("no image file")
    영상 스트리밍 서버 
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 여러개 인자 받는거 다시 봐야함 = 을 안 붙여야 인식이 된다.. --> 해결함 
    day 2. 
    a. python3 파일명.py --movie=어쩌구 0 
    b. 실행args로영상파일지정 0
        i. 실행 args 없는 경우 default 로 웹캠 영상 전송
        웹소켓
    c. 웹소캣으로 영상 전송 및 웹 서버에서 영상 재생 
       
        i. 스트리밍 프로그램에서 웹서버 컨트롤러까지
        웹소켓으로 프레임 전달
        ii. 웹서버 컨트롤러에서 view 까지 웹소켓으로
        프레임 전달
    day 3.웹서버컨트롤러를이용한영상스트리밍 0 
        a. yield 이용 image tag 에서 지정한 url 로 스트리밍
'''

#1. 크롭
#2. 리사이즈
#3. grayscale
#4. rotation(각도 지정 가능)
#5. merge
#6. vstack, hstack

def handle_image(resource, modes, output): 
    dir_list = os.listdir(resource)
    for i in range(len(dir_list)):
        print(i+1 , '\t\t' , dir_list[i])

    number = int(input("Pick one of the image:"))
    path = resource + '/' +str(dir_list[number-1]) #opencvtutorial 폴더에서 실행했으므로 path도 그 안에 맞는 경로로 지정
    img = cv2.imread(path)
   
    if img is not None:
       for mode in modes[0]:
           if mode == '1': # resize
               height , width = map(int, input("How much resize? Enter width and Height:").split())
               img = cv2.resize(img,dsize=(height, width), interpolation=cv2.INTER_AREA )
           elif mode=='2': #slice(crop)
               x, w, y, h = map(int, input("Enter Crop territory starting with width part.(x,w,y,h)").split())
               img = img[y:y+h, x:x+w]
           elif mode == '3': # change color to gray
               img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
           elif mode == '4': #rotation
               angle, scale = map(float, input("Type rotation angle in (90, 180, 270, 360) and Type scale (type 1 if you don't want to change scale):").split())
               height, width = img.shape[0], img.shape[1]
               matrix = cv2.getRotationMatrix2D((width/2, height/2), int(angle), scale)
               img = cv2.warpAffine(img, matrix, (width, height))
               
           elif mode == '5': # split후 merge
               b, g, r = cv2.split(img)
               img = cv2.merge((r,g,b))
           else:
               if mode == '6' or mode == '7':
                    for i in range(len(dir_list)):
                            print(i+1 , '\t\t' , dir_list[i])

                    number = int(input("Pick one of the image for stack:"))
                    path = resource + '/' +str(dir_list[number-1]) #opencvtutorial 폴더에서 실행했으므로 path도 그 안에 맞는 경로로 지정
                    img_second = cv2.imread(path)
                   

                    if mode =='6': # 수직 합성
                        width = int(input("How much resize? Enter width and Height:"))
                        img = cv2.resize(img,dsize=(img.shape[0], width), interpolation=cv2.INTER_AREA ) # 붙이는데 있어서 resize 해준다.
                        img_second = cv2.resize(img_second,dsize=(img_second.shape[0], width), interpolation=cv2.INTER_AREA )
                        img = np.vstack((img, img_second))
                    elif mode == '7': # 수평 합성
                        height = int(input("How much resize? Enter width and Height:"))
                        img = cv2.resize(img,dsize=(height, img.shape[1]), interpolation=cv2.INTER_AREA ) # 붙이는데 있어서 resize 해준다.
                        img_second = cv2.resize(img_second,dsize=(height, img_second.shape[1]), interpolation=cv2.INTER_AREA )
                        img = np.hstack((img, img_second))
               else:
                   print("Wrong option picked.") 

       timestr = time.strftime("%Y%m%d-%H%M%S")  
       if output == 'default':
           print("Nothing was typed for output folder!")
       output = output if output != 'default' else 'imgoutput'
       cv2.imwrite(output+'/'+timestr+'.jpeg', img)
       cv2.waitKey(1)
       cv2.destroyAllWindows()
       
    else:
        print("no image file")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Echo openc --img-dir IMG_DIR --mode MODE --result-dir RESULT_DIR") #Idir : input dir, Rdir: result dir
    parser.add_argument('--img-dir', help="Image_resource_dir",required=True)
    parser.add_argument('--mode', type = list ,help="Image_change_option", nargs='+', required=True)
    parser.add_argument('--result-dir', help="Image_output_dir", default= 'default')

    args = parser.parse_args()
    handle_image(resource = args.img_dir, modes = args.mode, output = args.result_dir) # No dictionary 형태 접근! args['mode'] -> Namespace is not subscriptable
                    # img-dir 사용했지만 img_dir로 접근

#https://chrisjune-13837.medium.com/%EC%9D%B8%EC%BD%94%EB%94%A9%EA%B3%BC-%EB%94%94%EC%BD%94%EB%94%A9-87006cf8dee2