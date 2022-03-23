from curses import meta
import cv2
import argparse
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
def handle_image(resource, modes, output):
    path = resource+'/-1.jpeg' #opencvtutorial 폴더에서 실행했으므로 path도 그 안에 맞는 경로여야한다.
    img1 = cv2.imread(path)
    print(type(resource))
    print(modes)
    print(1)
    options = []
    options =dir(cv2)
    
    if img1 is not None:
       for mode in modes:
           modeoption1 = '_'+mode+'_'
           modeoption2 = '__'+mode+'__'
           if mode in options:
               img2 = getattr(cv2, mode)(img1,dsize=(640, 480), interpolation=cv2.INTER_AREA)
               
           elif modeoption1 in options:
               func = getattr(cv2, modeoption1)(img1,dsize=(640, 480), interpolation=cv2.INTER_AREA)
               img2 = func()
           elif modeoption2 in options:
               func = getattr(cv2, modeoption2)(img1,dsize=(640, 480), interpolation=cv2.INTER_AREA)
               img2 = func()
        
       cv2.imwrite(output+'/'+str(img2), img2)
       cv2.imshow('image1', img2)
       cv2.waitKey()
       cv2.destroyAllWindows()
       cv2.waitKey()
    else:
        print("no image file")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Echo openc --img-dir IMG_DIR --mode MODE --result-dir RESULT_DIR") #Idir : input dir, Rdir: result dir
    parser.add_argument('--img-dir', help="Image_resource_dir",required=True)
    parser.add_argument('--mode', help="Image_change_option", nargs='+', required=True)
    parser.add_argument('--result-dir', help="Image_output_dir" ,required=True)

    args = parser.parse_args()
    handle_image(resource = args.img_dir, modes = args.mode, output = args.result_dir) # No dictionary 형태 접근! args['mode'] -> Namespace is not subscriptable
                    # 근데 img-dir 인데 어떻게 img_dir로 접근할 수 있는거지? 이건 질문해야겠다... 