import cv2
import argparse
import numpy as np 
import os,time, imghdr
#1. 크롭
# 2. 리사이즈 0 
# #3. grayscale 0
# #4. rotation(각도 지정 가능) 0
# #5. merge
# #6. vstack, hstack 0
# 다중 parse 
# drop frame 
def handle_image(resource, modes, output): 
    dir_list = os.listdir(resource)
    print("\nIMAGE LOADING-----------")
    nonimg = 0
    for i in range(len(dir_list)):
        print(dir_list[i])
        if imghdr.what(resource+'/'+dir_list[i]) in ['jpg', 'jpeg','png']:
            print(i+1 - nonimg , '\t\t' , dir_list[i])
        else:
            nonimg +=1
    while True:
        number = int(input("Pick one of the image for stack:"))
        if number > len(dir_list) or number <= 0:#잘못 선택
            print("Wrong select! Try again")
            continue
        else:
            break
    path = resource + '/' +str(dir_list[number-1 + nonimg]) #opencvtutorial 폴더에서 실행했으므로 path도 그 안에 맞는 경로로 지정
    img = cv2.imread(path)
    
    try:
       for mode in modes:
           if mode == '1': # resize ## resize 상대 비율도 옵션 선택 
               while True:
                   flag = int(input("절대비율(1)과 상대비율(2) 중 고르시오."))
                   if flag == 1:
                       width, height= input("How much resize? Enter width and Height:").split()
                       if width.isdigit() == True and height.isdigit() == True:
                           img = cv2.resize(img,dsize=(width, height), interpolation=cv2.INTER_AREA) #dsize = 너비, 높이
                           break
                       else:
                           print("Type numeric value")
                           continue
                   elif flag == 2:
                       f_x , f_y =  input("In what size rate? Enter x-size and y-size:").split()
                       if f_x.replace(".", "", 1).isdigit() == True and f_y.replace(".", "", 1).isdigit() == True:
                           img = cv2.resize(img,dsize=(0,0),fx=f_x, fy=f_y ,interpolation=cv2.INTER_AREA) #dsize = 너비, 높이
                           break
                       else:
                           print("Type numeric value")
                           continue
                   else:
                       print("Wrong choice. Pick Again") # 계속 선택 
                       
           elif mode=='2': #slice(crop) ##보통 x,y,w,h  ## x,y 음수일때.이건 다시 고민해봐야함
               x, y, w, h = map(int, input("Enter Crop territory starting with width part.(x,y,w,h)").split())
               if y < 0:
                   y = 0
                   h += y # h 값 조정: 음수의 영역부터 접근한걸 0에서부터 접근으로 조정했으니 h값을 조정  
               elif y+h > img.shape[0]:
                   h = img.shape[0] - y
               
               if x+w>img.shape[1]: # 자르려는게 넘으면 최대까지만 자르게 지정
                   w = img.shape[1] - x
               img = img[y:y+h, x:x+w]

           elif mode == '3': # change color to gray ## grayscale 후 stack, merge때 오류 
               
               img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
               img = cv2.merge((img,img,img)) # merge로 3차원으로 만들어준다. 
               
           elif mode == '4': #rotation
               while True:
                   angle, scale = input("Type rotation angle in (90, 180, 270, 360) and Type scale (type 1 if you don't want to change scale):").split()
                   if angle.isdigit() == True and scale.isnumeric() == True:
                       break
                   else:
                       print("Type numeric value")   
               height, width = img.shape[0], img.shape[1]
               angle = -angle
               matrix = cv2.getRotationMatrix2D((width/2, height/2), int(angle), scale)
               img = cv2.warpAffine(img, matrix, (width, height))
               
           
           else:
               
               if mode in ['5','6','7']:
                    print("\nIMAGE LIST--------")
                    for i in range(len(dir_list)):
                            print(i+1 , '\t\t' , dir_list[i])
                    while True:
                        number = input("Pick one of the image for stack:")
                        if number.isdigit() != True and (int(number) > len(dir_list) or int(number) <= 0):#잘못 선택
                            print("Wrong select! Try again")
                            continue
                        else:
                            break
                    print(1)
                    
                    path2 = resource + '/' +str(dir_list[number-1]) #opencvtutorial 폴더에서 실행했으므로 path도 그 안에 맞는 경로로 지정
                    print(path2)
                    img_second = cv2.imread(path2)
                    print(2)
                    if mode == '5': # split후 merge # todo merge는 2개를 merge하라는 것이다.
                        b, g, r = cv2.split(img)
                        img = cv2.merge((r,g,b))

                    if mode =='6': # 수직 합성
                        while True:
                            width = input("How much resize? Enter width:")
                            if width.isdigit() == True:
                                break
                            else:
                                print("Type Digit value")
                        img = cv2.resize(img,dsize=(width, img.shape[0]), interpolation=cv2.INTER_AREA ) # 붙이는데 있어서 resize 해준다.
                        img_second = cv2.resize(img_second,dsize=(width, img_second.shape[0]), interpolation=cv2.INTER_AREA )
                        img = np.vstack((img, img_second))
                    elif mode == '7': # 수평 합성
                        while True:
                            height = input("How much resize? Enter Height:")
                            if height.isdigit() == True:
                                break
                            else:
                                print("Type Digit value")
                        img = cv2.resize(img,dsize=(img.shape[1],height), interpolation=cv2.INTER_AREA ) # 붙이는데 있어서 resize 해준다.
                        img_second = cv2.resize(img_second,dsize=(img_second.shape[1],height), interpolation=cv2.INTER_AREA )
                        img = np.hstack((img, img_second))
                    else:
                        print("No option")
    except ValueError as e: # todo 다시 시작으로 수정 ##error 수정 
        print("Handling Error")
        print(e)
        quit()
    except:
        print("Handling Error")
        print("Other Error occured")
        quit()

    timestr = time.strftime("%Y%m%d-%H%M%S")  #이미지 이름 시간날짜로 지정 
    if output == 'default': # 아무것도 안 적혀 있으면 지정 폴더로 (지정폴더도 없을 경우에는 지정폴더 생성)
        print("Nothing was typed for output folder!")
        if not os.path.exists('imgoutput'):
            os.makedirs('imgoutput')
        output = 'imgoutput'
    elif not os.path.exists(output): # 새로운 폴더 
        os.makedirs(output)
    cv2.imwrite(output+'/'+timestr+'.jpeg', img)
       
   
if __name__ == '__main__': # todo argsparse 세팅 시 , or 공백으로 인정할 수 있게 한다.
    parser = argparse.ArgumentParser(description="Echo openc --img-dir IMG_DIR --mode MODE --result-dir RESULT_DIR") #Idir : input dir, Rdir: result dir
    parser.add_argument('--img-dir', help="Image_resource_dir",required=True)
    parser.add_argument('--mode', type = lambda arg: arg.split(',') ,help="Image_change_option", required=True)
    parser.add_argument('--result-dir', help="Image_output_dir", default= 'default')

    args = parser.parse_args()
    handle_image(resource = args.img_dir, modes = args.mode, output = args.result_dir)
                    # img-dir 사용했지만 img_dir로 접근

#https://chrisjune-13837.medium.com/%EC%9D%B8%EC%BD%94%EB%94%A9%EA%B3%BC-%EB%94%94%EC%BD%94%EB%94%A9-87006cf8dee2