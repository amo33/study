from curses.ascii import US
import os
from sqlalchemy.exc import IntegrityError
from matplotlib.font_manager import json_dump
from models import db, User
from flask import send_from_directory, Flask, request, render_template, jsonify
from werkzeug.utils import secure_filename
import uuid
from PIL import Image
from pathlib import Path
import json
app = Flask(__name__) # 사용할 flask 앱을 가져온다. 
# thumb = Thumbnail(app)
base_dir = os.path.abspath(os.path.dirname(__file__)) # absolute path 지정

img_format = ['jpg','png','peg','jpe']
db_file = os.path.join(base_dir, 'User.sqlite')
file_path = "study/Term1/sample.json" 
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///' +db_file # 사용할 DB
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True # 비즈니스 로직이 끝날때 commit 실행(DB 반영) - 다 처리후 결과 DB에 저장
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # track은 안한다.

app.config['THUMBNAIL_MEDIA_ROOT'] = '/home/www/media'
app.config['THUMBNAIL_MEDIA_URL'] = '/media/'

app.config['THUMBNAIL_MEDIA_THUMBNAIL_ROOT'] = '/Term1/Image/cache'
app.config['THUMBNAIL_MEDIA_THUMBNAIL_URL'] = '/Image/cache/'
app.config['THUMBNAIL_STORAGE_BACKEND'] = 'flask_thumbnails.storage_backends.FilesystemStorageBackend'
app.config['THUMBNAIL_DEFAUL_FORMAT'] = 'JPEG'

# sercet_file = os.path.join(base_dir, 'secrets.json') # json 파일 위치 
app.config['SECRET_KEY'] ='1234'
db.init_app(app)
db.app = app
db.create_all()

@app.route('/') # flask의 데코레이터로 특정 url에 접속하면 바로 다음 줄에 있는 함수를 호출한다. -> form() 호출
def form():
    data = {}
    return render_template('form_submit.html', types = 'default', data = data)

@app.route('/hello',methods=['GET','POST']) # Use post & Get 
def action():
    ##### Things to do #### 
    ### DB 예외처리!!! - 만약 하나라도 없다면 새로운 페이지로 가서 어느 데이터를 안 넣었는지 알려주고 다시 등록 페이지로 가게 한다. 
    # action.counter +=1
    if(request.method == 'GET'):
        argu = request.args.get('value')
        print(argu)
        if argu != None: # if we get some parameter after /hello than use the other function
            names = argu 
            user_info = User.query.filter(User.username==names).all()
            print(user_info[0])
            return render_template('form_submit.html', types = 'detail',data = user_info[0])
            
        else:
            data = {}
            return render_template('form_submit.html', types = 'default', data= data) # if db내에 없는 오류가 발생한다면 다시 연결 
    elif(request.method == "POST"):
        data = {}
        
        k = request.files['file'] 
        rand_form = uuid.uuid1() # 이미지마다 unique명 유지 
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        age = request.form['age']
        img_dir = str(rand_form)+secure_filename(k.filename)
        try: #이미지 오류는 성공 나머지 값들 오류도 내일 넣어주기 
            if (secure_filename(k.filename[-3:]) not in img_format):
                raise Exception
            if(firstname+lastname == '' or age == ''):
                raise Exception
        except Exception:
            return render_template('Error_Handling.html')
       
        k.save('study/Term1/Image/'+img_dir) 
        path = Path('study/Term1/Image/'+img_dir) #thumbnail 시키기 위한 과정 
        image = Image.open(path)
        size = (128,128)
        image.thumbnail(size)
        image.save(Path('study/Term1/static/ThumbedImg/'+img_dir))
        user = User(username = firstname+ " " +lastname, age = age,Image = 'ThumbedImg/'+ img_dir) 
        db.session.add(user)
        try: # used for unique integrity error 
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return render_template('Error_Handling.html')
        f = open('study/Term1/data.txt', "a") # 파일에 내용을 write 한다.
        
        lines = [firstname + lastname,', ' ,age, ', ' ,'study/Term1/static/ThumbedImg/'+img_dir,', ']
        f.writelines(lines) 
        f.close()
        return render_template('form_submit.html', types = 'default', data = data)
        #return render_template('form_action.html', firstname=firstname, lastname= lastname, age = age)
                #Renders template from the templte folder with the given context 

@app.route('/responsed', methods = ["GET"]) # for ajax & json response between form_submit.html
def responsed():
    #argu = json.loads(request.data)
    #names = argu.get('id')
    names = request.args.get('value')
    user_info = User.query.filter(User.username == names).all()
    
    user = {
        "Name":names, 
        "Age":user_info[0].age, 
        "Image":user_info[0].Image
        }
    print(1)
    with open(file_path, 'w') as outfile:
        json.dump(user, outfile)
    return jsonify(user)        
    

#db파일과 text 파일은 서로 같은 filepath에 있으면 내 코드상 충돌이 일어날거 같아서 filepath를 애초에 다른것으로 함
''' 바로 위 주석은 get parameters를 사용하지 않았을때 겪는다. 그럼 내 질문은 get parameters에 들어갈 값을 내가 선택해서 넣어줄 수 있는 방법이 왜 안떠오르지? 
@app.route('/db/<tag>')
def showdb(tag):
    
    return render_template('db_show.html', values = User.query.all())

@app.route('/text/<tag>')
def submit(tag):
    return render_template('txt_list.html')
'''
@app.route('/detail')
def show_detail():
    return render_template('detail.html')

@app.route('/list', methods= ['GET','POST'])
def list_show():
    argu = request.args.get('tag', 'default')
    argu = argu.lower()
    if argu == 'db' :
        return render_template('list.html',types= argu,values = User.query.all())
    elif argu == 'text':
        f = open('study/Term1/data.txt', "r")
        lines = f.read()
        new_list = lines.split(', ')
        names = new_list[0::3]
        ages = new_list[1::3]
        images = new_list[2::3]
        # lines_list = [line.rstrip('\n') for line in lines] -> 이런 식으로 값을 넘기면 문제 발생한다. 
        #print(lines_list)
        return render_template('list.html', types= argu, Name = names, Age = ages, Image = images) # 데이터들 넘기기
    else:
        f = open('study/Term1/data.txt', "r")
        lines = f.read()
        print(type(lines))
        print(lines)
        new_list = lines.split(', ')
        print(new_list)
        names = new_list[0::3]
        return render_template('list.html', types = 'default', values = names)

#@app.route('/Image/<regex("([\w\d_/-]+)?.(?:jpe?g|gif|png)"):filename>')
#def media_file(filename):
#    return send_from_directory(app.config['THUMBNAIL_MEDIA_THUMBNAIL_ROOT'], filename)
if __name__ == '__main__':
    #action.counter = 0
    app.run(host='0.0.0.0', debug = True)
'''
            f = open('study/Term1/data.txt', "r") 
            lines = f.read()
            new_list = lines.split(', ')
            idx = new_list.index(names)
            ages = new_list[idx+1]
            
            img_dir = new_list[idx+2]
            path = Path('study/Term1/Image/'+img_dir)
            image = Image.open(path)
            size = (128,128)
            image.thumbnail(size)
            image.save(Path('study/Term1/ThumbedImg/'+img_dir))
            
            import matplotlib.pyplot as plt
            import matplotlib.image as img
            rt = json.dumps(user_info).Image
            image = img.imread(rt)
            plt.imshow(image)
            plt.show()
            '''