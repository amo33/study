import cv2
import argparse
import numpy as np 
import os,time, imghdr
#1. 크롭 o
# 2. 리사이즈 o
# #3. grayscale o
# #4. rotation(각도 지정 가능) o
# #5. merge o
# #6. vstack, hstack o
# 다중 parse o 
# drop frame o
# img file 만 사용 o
def handle_image(resource, modes, output): 
    dir_list = os.listdir(resource)
    print("\nIMAGE LOADING---FIRST--------")
    nonimg = 0
    for i in range(len(dir_list)):
        if imghdr.what(resource+'/'+dir_list[i]) in ['jpg', 'jpeg','png']: #이미지 파일만 읽기
            print(i+1 - nonimg , '\t\t' , dir_list[i])
        else:
            nonimg +=1 #전처리용으로 사용
    while True:
        number = int(input("Pick one of the image for stack:"))
        if number > len(dir_list) or number <= 0:#잘못 선택
            print("Wrong select! Try again")
            continue
        else:
            break
    path = resource + '/' +str(dir_list[number-1 + nonimg]) #opencvtutorial 폴더에서 실행했으므로 path도 그 안에 맞는 경로로 지정
    img = cv2.imread(path)
    flag = 1 # 모든 모드를 잘 돌았으면 이미지 저장을 할 때 판별하기 위해 사용 1이면 저장, 0이면 저장 X
    flat_modes = []
    for mode in modes:
        if "," in mode:
            mode = mode.split(",")
            flat_modes.extend(mode)
        else:
            flat_modes.append(mode)
    if len(flat_modes) == 0: # 잘못된 옵션들만 있으면 저장 X
        flag= 0
    while(flag == 1):
       for mode in flat_modes:
           print(mode)
           if mode == '1': 
               while True:
                   option = int(input("절대비율(1)과 상대비율(2) 중 고르시오."))
                   if option == 1:
                       width, height= input("How much resize? Enter width and Height:").split()
                       if width.isdigit() == True and height.isdigit() == True:
                           width = int(width)
                           height = int(height)
                           img = cv2.resize(img,dsize=(width, height), interpolation=cv2.INTER_AREA) #dsize = (너비, 높이) shape = (높이 , 너비)!
                           break
                       else:
                           print("Type numeric value")
                           continue
                   elif option == 2:
                       f_x , f_y =  input("In what size rate? Enter x-size and y-size:").split()
                       x_check = f_x.partition('.')
                       y_check = f_y.partition('.')

                       if (x_check[0] == '0' and x_check[1] == '.' and x_check[2].isdigit()) and (y_check[0] == '0' and y_check[1] == '.' and y_check[2].isdigit()):
                           f_x = float(f_x)
                           f_y = float(f_y)
                           img = cv2.resize(img,dsize=(0,0),fx=f_x, fy=f_y ,interpolation=cv2.INTER_AREA) #dsize = 너비, 높이
                           break
                       else:
                           print("Type numeric value")
                           continue
                   else:
                       print("Wrong choice. Pick Again") # 계속 선택 
                       
           elif mode=='2': #slice(crop)  ## x,y 음수일때.이건 다시 고민해봐야함
               x, y, w, h = map(int, input("Enter Crop territory starting with width part.(x,y,w,h)").split())
               if y + h < 0: 
                   if y > 0: # 시작점이 더 큰데 음수쪽으로 slice해버리면 0에서부터 slice 한다고 생각 
                       h = y
                       y = 0
                   elif h > 0:
                       y = 0
                       h += y 
                   elif y<=0 and h <=0:
                       flag = 0
                       print("Nothing to slice")
                       continue
                   
               elif y+h > img.shape[0]:
                   if y<=0:
                       y = 0
                       h = img.shape[0]
                   elif h >0 and y<img.shape[0]: 
                       h = img.shape[0] - y
                   elif h>0 and y>=img.shape[0]:
                       flag = 0
                       print("Nothing to slice")
                       continue    
                       
               if x+w>img.shape[1]: # 자르려는게 넘으면 최대까지만 자르게 지정
                   if x <=0:
                       x = 0
                       w = img.shape[1]
                   elif w > 0 and x<img.shape[1]:  #todo 고쳐 초과
                       w = img.shape[1] - x
                   elif w > 0 and x>=img.shape[1]:
                       flag = 0
                       print("Nothing to slice")
                       continue  
               elif x + w < 0:
                   if x > 0:
                       w = x 
                       x = 0
                   elif w > 0:
                       x = 0
                       w += x
                   elif x<=0 and w<=0:
                       flag = 0
                       print("Nothing to slice")
                       continue
               img = img[y:y+h, x:x+w]

           elif mode == '3': # change color to gray  
               
               img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
               img = cv2.merge((img,img,img)) # merge로 3차원으로 만들어준다. #stack이나 merge할때 오류가 안나기 위해 channel을 3개로 확장 
               
           elif mode == '4': #rotation
               while True:
                   angle, scale = input("Type rotation angle in (90, 180, 270, 360) and Type scale (type 1 if you don't want to change scale):").split()
                   if angle.isdigit() == True and scale.isnumeric() == True:
                       break
                   else:
                       print("Type numeric value")   
               height, width = img.shape[0], img.shape[1]
               angle = -int(angle)

               matrix = cv2.getRotationMatrix2D((width/2, height/2), angle, int(scale))
               img = cv2.warpAffine(img, matrix, (width, height))
               
           
           else:
               
               if mode in ['5','6','7']:
                    print("\nIMAGE LOADING---SECOND-----")
                    nonimg = 0
                    for i in range(len(dir_list)):
                        if imghdr.what(resource+'/'+dir_list[i]) in ['jpg', 'jpeg','png']: #이미지 파일만 읽기
                            print(i+1 - nonimg , '\t\t' , dir_list[i])
                        else:
                            nonimg +=1
                    while True:
                        number = input("Pick one of the image for stack:")
                        if number.isdigit() != True and (int(number) > len(dir_list) or int(number) <= 0):#잘못 선택
                            print("Wrong select! Try again")
                            continue
                        else:
                            break
                    
                    path2 = resource + '/' +dir_list[int(number)-1+nonimg] #opencvtutorial 폴더에서 실행했으므로 path도 그 안에 맞는 경로로 지정
                    print(path2)
                    img_second = cv2.imread(path2)
                    print(2)
                    if mode == '5': # todo merge는 2개를 merge하라는 것이다.
                        while True: 
                            alpha, beta = input("In what rate to merge both?:").split()
                            alpha_check = alpha.partition('.')
                            beta_check = beta.partition('.')
                            if(alpha_check[0]== '0' and alpha_check[1] == '.' and alpha_check[2].isdigit()) and (beta_check[0] == '0' and beta_check[1] == '.' and beta_check[2].isdigit()):
                                alpha = float(alpha)
                                beta = float(beta)
                                if alpha + beta == 1.0:
                                    break 
                                else: 
                                    print('alpha and beta sum has to 1')
                        while True:
                            print("For exact shape, we don't use relative resize.")
                            width, height= input("How much resize? Enter width and Height:").split()
                            if width.isdigit() == True and height.isdigit() == True:
                                width = int(width)
                                height = int(height)
                                img = cv2.resize(img,dsize=(width, height), interpolation=cv2.INTER_AREA) #dsize = 너비, 높이
                                img_second= cv2.resize(img_second,dsize=(width, height), interpolation=cv2.INTER_AREA) #dsize = 너비, 높이
                                break
                            else:
                                print("Type numeric value")
                                continue
                        img = cv2.addWeighted(img, alpha, img_second, beta, 0) #merge

                    elif mode =='6': # 수직 합성
                        while True:
                            width = input("How much resize? Enter width:")
                            if width.isdigit() == True:
                                width = int(width)
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
                                height = int(height)
                                break
                            else:
                                print("Type Digit value")
                        img = cv2.resize(img,dsize=(img.shape[1],height), interpolation=cv2.INTER_AREA ) # 붙이는데 있어서 resize 해준다.
                        img_second = cv2.resize(img_second,dsize=(img_second.shape[1],height), interpolation=cv2.INTER_AREA )
                        img = np.hstack((img, img_second))
                    else:
                        print("No option")
       if flag == 1:
           timestr = time.strftime("%Y%m%d-%H%M%S")  #이미지 이름 시간날짜로 지정 
           if output == 'default': # 아무것도 안 적혀 있으면 지정 폴더로 (지정폴더도 없을 경우에는 지정폴더 생성)
               print("Nothing was typed for output folder!")
               if not os.path.exists('imgoutput'):
                   os.makedirs('imgoutput')
               output = 'imgoutput'
           elif not os.path.exists(output): # 새로운 폴더로 지정된다면 
               os.makedirs(output)
           cv2.imwrite(output+'/'+timestr+'.jpeg', img)
           break
       elif flag == 0: #저장할게 없는 경우에는 그냥 종료 
           print("No image to store")
           break
        
   
if __name__ == '__main__': # todo argsparse 세팅 시 , or 공백으로 인정할 수 있게 한다.
    parser = argparse.ArgumentParser(description="Echo openc --img-dir IMG_DIR --mode MODE --result-dir RESULT_DIR") #Idir : input dir, Rdir: result dir
    parser.add_argument('--img-dir', help="Image_resource_dir",required=True)
    parser.add_argument('--mode','-m',help="Image_change_option", nargs= '+',required=True) # optional한 선언은 mode=A or mode A로 받을 수 있다. 
    parser.add_argument('--result-dir', help="Image_output_dir", default= 'default')

    args = parser.parse_args()
    handle_image(resource = args.img_dir, modes = args.mode, output = args.result_dir)
                    # img-dir 사용했지만 img_dir로 접근 -> -가 인자의 이름에 들어갔으면, args.인자에서는 _로 접근해준다. 
#type = lambda arg: arg.split(',') 
# action='append',
#https://chrisjune-13837.medium.com/%EC%9D%B8%EC%BD%94%EB%94%A9%EA%B3%BC-%EB%94%94%EC%BD%94%EB%94%A9-87006cf8dee2
#https://greeksharifa.github.io/references/2019/02/12/argparse-usage/#action%EC%9D%98-%EC%A2%85%EB%A5%98-%EC%A7%80%EC%A0%95 -> branch study(git)