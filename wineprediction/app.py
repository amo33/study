import tensorflow as tf 
from flask import Flask, render_template, request,redirect, url_for, session
import pickle , json 
import numpy as np
from sklearn import preprocessing
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
    #print(coef(model)) 
    alcohol = request.form['alcohol']
    pH = request.form['pH']
    sulphates = request.form['sulphates']
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

    session['alcohol'] = alcohol
    session['pH'] = pH
    session['sulphates'] = sulphates
    # don't use json to send it. it occurs error ->->
    # wineoption = json.dumps({"alcohol":alcohol,"pH":pH,"sulphates":sulphates})
    return redirect(url_for('wine_result', winedata = wine))
    
@app.route('/wine/<winedata>',methods=["GET","POST"])
def wine_result(winedata):
    tf.compat.v1.reset_default_graph()
    with tf.compat.v1.Session() as sess:
        if winedata == 'red':
            saver = tf.compat.v1.train.import_meta_graph('redwinemodel/redwine.meta')
            saver.restore(sess, tf.train.latest_checkpoint('redwinemodel/'))
        elif winedata == 'white':
            saver = tf.compat.v1.train.import_meta_graph('whitewinemodel/whitewine.ckpt.meta')
            saver.restore(sess, 'whitewinemodel/whitewine.ckpt')
        '''
        if winedata == 'red':
            model = pickle.load(open('models/Redwine.pkl','rb')) #pickle 사용을 추천합니다 instead of sklearn.joblib
        elif winedata == 'white':
            model = pickle.load(open('models/Whitewine.pkl','rb'))
        
        #prediction = model.predict(data) -> data 활용해서 구하면 된다.
        #print(prediction)
        #print(model.best_estimator_.coef_) 
        '''
        sulphates = session['sulphates']
        alcohol = session['alcohol']
        pH = session['pH']

        data  = np.float32([sulphates, alcohol, pH]) #데이터는 numpy 형태로 
        data = data.reshape(1,-1) #한 column에 대한 값들이면 (-1,1) 한 row에 대한 값이라면 (1,-1)

        sc_x = preprocessing.MinMaxScaler()
        data = sc_x.fit_transform(data)
        graph = tf.compat.v1.get_default_graph()
        

        W = graph.get_tensor_by_name("weight:0") # 모델 가져오기 
        b = graph.get_tensor_by_name("bias:0") #모델 가져오기 
        X = tf.compat.v1.placeholder(tf.float32, shape=[None, 3]) #새로운 input 값이기 때문에 새로 만들어준다.
        hypothesis = tf.matmul(X, W)+b 
        prediction =sess.run(hypothesis ,feed_dict={X:data})
        #prediction = sc_y.fit.inverse_transform(scaled_prediction.reshape(-1,1))
        return render_template('wineweb.html',data = prediction)
    
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

#https://mangastorytelling.tistory.com/entry/K-ICT-%EB%B9%85%EB%8D%B0%EC%9D%B4%ED%84%B0%EC%84%BC%ED%84%B0-Ch8-%EC%99%80%EC%9D%B8-%ED%92%88%EC%A7%88-%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%A5%BC-%ED%99%9C%EC%9A%A9%ED%95%9C-%EB%B6%84%EC%84%9D-%EB%AA%A8%EB%8D%B8%EB%A7%81-%EC%84%A0%ED%98%95%ED%9A%8C%EA%B7%80%EB%AA%A8%EB%8D%B8-%EA%B7%9C%EC%A0%9C%EC%84%A0%ED%98%95%ED%9A%8C%EA%B7%80%EB%AA%A8%EB%8D%B8-%EC%9E%84%EC%A0%95%ED%99%98%EA%B5%90%EC%88%98