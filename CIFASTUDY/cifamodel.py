#http://krasserm.github.io/2018/03/19/gaussian-processes/
#http://krasserm.github.io/2018/03/21/bayesian-optimization/
#https://wooono.tistory.com/102
#https://nittaku.tistory.com/264 -> 발표 준비용 (pooling 사용하는 이유 )
#https://github.com/deep-diver/CIFAR10-img-classification-tensorflow/blob/master/CIFAR10_image_classification.ipynb -deep diver
from flask import Flask, render_template, request,redirect, url_for, session
import pickle
import numpy as np 
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = '1234'

@app.route('/')
def initial_page():
    return render_template('imagepredict.html')

@app.route('/image', methods=['POST'])
def submitImage():
    image = request.files['image']
    error = False
    if image != None:
        print("No issue")
    elif image == None:
        print("Issue occured")
        error = True
    return render_template('imagepredict.html', error= error)