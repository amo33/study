import tensorflow as tf 
from flask import Flask, render_template, request,redirect, url_for, session
import pickle , json 
import numpy as np
from sklearn import preprocessing
import pandas as pd
#from flask_cors import CORS
# session use to constantly save form data
app = Flask(__name__)
#CORS(app)
app.config['SECRET_KEY'] = '1234'

@app.route('/')
def initial_page():
    return render_template('wineweb.html')

@app.route('/wine', methods=['POST'])
def wine_select():
    wine = request.form['wine'] #form 예외처리 -> 안 들어오면 에러로 다시 redirect 시캬주기 
    if wine is None:
        print("Need to pick wine option!")
        return render_template('wineweb.html',error = "Error")
    if wine == 'red':
        alcohol = request.form['alcohol']
        pH = request.form['pH']
        sulphates = request.form['sulphates']
    elif wine == 'white':
        alcohol = request.form['alcohol']
        Density = request.form['Density']
        chlorides = request.form['chlorides']
    if (is_number(alcohol) == False or is_number(pH) == False or is_number(sulphates) == False):
        print("Need to type all the right digit inputs!")
        return render_template('wineweb.html',error = "Error")
    elif alcohol[0] == '.' or pH[0] == '.' or sulphates[0] =='.':
        print("Need to type all the right digit inputs!")
        return render_template('wineweb.html',error = "Error")
    elif (alcohol[0] == '0' and alcohol[1] !='.') or (pH[0]=='0' and pH[1]!='.') or (sulphates[0] == '0' and sulphates[1] !='.'):
        print("Need to type all the right digit inputs!")
        return render_template('wineweb.html',error = "Error")
    elif float(alcohol) <=0 or float(pH)<=0 or float(sulphates)<= 0:
        print("Need to type all the right digit inputs!")
        return render_template('wineweb.html',error = "Error")

    if wine == 'red':
        
        session['alcohol'] = alcohol
        session['pH'] = pH
        session['sulphates'] = sulphates
    elif wine == 'white':
        
        session['alcohol'] = alcohol
        session['chlorides'] = chlorides
        session['Density'] = Density
    # don't use json to send it. it occurs error (밑에처럼 값 보내지 말자.)
    # wine = json.dumps({"alcohol":alcohol,"pH":pH,"sulphates":sulphates})
    return redirect(url_for('wine_result', winedata = wine))
    
@app.route('/wine/<winedata>',methods=["GET","POST"])
def wine_result(winedata):
    df = pd.read_csv('winequality-red.csv',';')
    tf.compat.v1.reset_default_graph()
    with tf.compat.v1.Session() as sess:
        if winedata == 'red':
            saver = tf.compat.v1.train.import_meta_graph('redwinemodel/train1-60000.meta')
            #saver = tf.train.Saver()
            saver.restore(sess, tf.train.latest_checkpoint('redwinemodel/./'))
            with open('redwine.pickle', 'rb') as fr:
                wine_scale_loaded = pickle.load(fr)
        elif winedata == 'white':
            saver = tf.compat.v1.train.import_meta_graph('whitewinemodel/train1-184000.meta')
            saver.restore(sess, tf.train.latest_checkpoint('whitewinemodel/./'))
            with open('whitewine.pickle', 'rb') as fr:
                wine_scale_loaded = pickle.load(fr)
    
        sulphates = session['sulphates']
        alcohol = session['alcohol']
        pH = session['pH']
        
        def Standardscaler(col, x):
            #print(col)
            mean_val = wine_scale_loaded[col][0]
            std_val = wine_scale_loaded[col][1]
            #print(std_val, mean_val)
            #print((x - mean_val)/(std_val))
            return (x - mean_val)/(std_val)

        data  = np.float32([sulphates, alcohol, pH]) #데이터는 numpy 형태로 
        data[0] = Standardscaler('sulphates', data[0])
        data[1] = Standardscaler('alcohol',data[1])
        data[2] = Standardscaler('pH',data[2])
        data = data.reshape(1,-1) #한 column에 대한 값들이면 (-1,1) 한 row에 대한 값이라면 (1,-1)

        #graph = tf.compat.v1.get_default_graph() # 저장된 graph가져오기 
        #sess.run(tf.global_variables_initializer())
        #W = graph.get_tensor_by_name("weight:0") # 모델 가져오기 
    
        ##### 모델 다시 개선해야한다.

        #b = graph.get_tensor_by_name("bias:0") #모델 가져오기 
        
        df = pd.DataFrame(df)
        df.drop_duplicates(subset=None, inplace=True)
        result = df[["quality"]]
        x = df[['sulphates','alcohol','pH']]
        
          
        size= 3
        #X = tf.placeholder(tf.float32, shape=[None, size])
        #W = tf.Variable(tf.random_normal([size, 1]), name='weight')
        #b = tf.Variable(tf.random_normal([1]), name='bias')
        #sess = tf.Session()
        #sess.run(tf.global_variables_initializer())
        #hypothesis = tf.add(tf.matmul(X,W),b)
        #prediction = tf.round(hypothesis)
        res = 0
        
        #saver.restore(sess, model_filepath)
        
        for i in range(x.shape[0]):
            data = np.float32([x.iloc[i]['sulphates'],x.iloc[i]['alcohol'],x.iloc[i]['pH']]) #데이터는 numpy 형태로 
            data[0] = Standardscaler('sulphates', data[0])
            data[1] = Standardscaler('alcohol',data[1])
            data[2] = Standardscaler('pH',data[2])
            data = data.reshape(1,-1)
            
            #acc = sess.run(prediction, feed_dict={X: data})
            #print(acc+1, result.iloc[i])
            hypothesis = tf.add(tf.matmul(data,sess.run("weight:0")),sess.run("bias:0")) 
            if (np.round(hypothesis.eval())+1)== result.iloc[i].values: # add_1:0 값이라고 뜨는건 형태를 add_1:0의 값을 사용했다라고 표현. 이건 결과 값이 아니다. eval()을 써야 값이 나온다. in order to change tensor to scalar
                print(np.round(hypothesis.eval())+1)
                #print(acc+1)
                res +=1
        print(res)
        print(x.shape[0])                
        #prediction =sess.run(hypothesis ,feed_dict={X:data})
        return render_template('wineweb.html',data = acc)
    
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

#https://mangastorytelling.tistory.com/entry/K-ICT-%EB%B9%85%EB%8D%B0%EC%9D%B4%ED%84%B0%EC%84%BC%ED%84%B0-Ch8-%EC%99%80%EC%9D%B8-%ED%92%88%EC%A7%88-%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%A5%BC-%ED%99%9C%EC%9A%A9%ED%95%9C-%EB%B6%84%EC%84%9D-%EB%AA%A8%EB%8D%B8%EB%A7%81-%EC%84%A0%ED%98%95%ED%9A%8C%EA%B7%80%EB%AA%A8%EB%8D%B8-%EA%B7%9C%EC%A0%9C%EC%84%A0%ED%98%95%ED%9A%8C%EA%B7%80%EB%AA%A8%EB%8D%B8-%EC%9E%84%EC%A0%95%ED%99%98%EA%B5%90%EC%88%98

    '''
        if winedata == 'red':
            model = pickle.load(open('models/Redwine.pkl','rb')) #pickle 사용을 추천합니다 instead of sklearn.joblib
        elif winedata == 'white':
            model = pickle.load(open('models/Whitewine.pkl','rb'))
        
        #prediction = model.predict(data) -> data 활용해서 구하면 된다.
        #print(prediction)
        #print(model.best_estimator_.coef_) 
        '''