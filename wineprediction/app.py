from distutils.log import debug
from flask import Flask, render_template, request
import pickle
import numpy as np
#from flask_cors import CORS

app = Flask(__name__)
#CORS(app)
app.config['SECRET_KEY'] = '1234'

@app.route('/')
def initial_page():
    
    return render_template('wineweb.html')

@app.route('/wine', methods=['POST'])
def model_result():
    model = pickle.load(open('models/model.pkl','rb')) #pickle 사용을 추천합니다. then sklearn.joblib
    alcohol = request.form['alcohol']
    pH = request.form['pH']
    sulphates = request.form['sulphates']
    '''
    if alcohol is None or pH is None or sulphates is None: # 하나라도 안들어오면 
        print("Need to type all the inputs!")
        return render_template('wineweb.html')
    elif alcohol[0] == '.' or pH[0] == '.' or sulphates[0] == '.': #.으로 시작하면 
        print("Need to type all the inputs!")
        return render_template('wineweb.html')
    elif alcohol.isdigit() != True or pH.isdigit() != True or sulphates.isdigit() != True:
        print("Need to type all the inputs!")
        return render_template('wineweb.html')
    '''
    if (is_number(alcohol) == False or is_number(pH) == False or is_number(sulphates) == False):
        print("Need to type all the right digit inputs!")
        return render_template('wineweb.html',error = "Error")
    
    data  = np.array([sulphates, alcohol, pH]) #데이터는 numpy 형태로 
    data = data.reshape(1,-1) #한 column에 대한 값들이면 (-1,1) 한 row에 대한 값이라면 (1,-1)
    prediction = model.predict(data)
    print(prediction)
    print(coef(model))
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