import tensorflow as tf 
import pandas as pd 
import numpy as np 
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.linear_model import LinearRegression
from sklearn import svm
import pickle , os
from sklearn import preprocessing 
from sklearn.metrics import classification_report
df = pd.read_csv('winequality-red.csv',';')
'''
standard_scaler_x = preprocessing.StandardScaler()
standard_scaler_y = preprocessing.StandardScaler()
red_df = pd.DataFrame(df)
red_df_duplicate_dropped = df.copy()
red_df_duplicate_dropped.drop_duplicates(subset=None, inplace=True)
y = red_df_duplicate_dropped[["quality"]]
X = red_df_duplicate_dropped[['sulphates','alcohol','pH']]
#X = standard_scaler_x.fit_transform(X)
#y = standard_scaler_y.fit_transform(y)
red_df_x_train, red_df_x_test,red_df_y_train, red_df_y_test = train_test_split(X,y,test_size=0.3, random_state=100)

def svc_param_selection(X,y,nfolds):
    svm_parameters = [ {'kernel' : ['linear'], 
    'gamma' : [0.00001, 0.0001, 0.001, 0.01, 0.1, 1], 
    'C' : [0.01, 0.1, 1, 10, 100, 1000]} ] 
    #사이킷런에서 제공하는 GridSearchCV를 사용해 최적의 파라미터를 구함 
    clf = GridSearchCV(svm.SVR(), svm_parameters, cv=nfolds) 
    clf.fit(X, y) 
    print(clf.best_params_) #최고 점수
    return clf


#1 model = svm.SVR(kernel='linear') #,validation_split = 0.33 , callbacks=[model_callback]
#1 for i in range(10):
#1   start = i*139
#1   end = start + 139
#1   model.fit(red_df_x_train.loc[[i not in range(start,end)], :], red_df_y_train)
#1 model.fit(red_df_x_train, red_df_x_test) # 왜 cross validation 구현을 못하겠지?

model = svc_param_selection(red_df_x_train, red_df_y_train.values.ravel(),5)
                                                    # scale안하면 dataframe 상태여서 values붙여야한다.

if os.path.isfile('models/Redwine.pkl') == False:
    os.makedirs('models/Redwine.pkl')

with open('models/Redwine.pkl','wb') as f: 
    pickle.dump(model, f)

#print('training accuracy:', model.score(red_df_x_train, red_df_y_train))

def my_score(result, answer):
    comparison = pd.DataFrame(answer)
    
    comparison['prediction'] = result
    comparison = round(comparison)
    evaluation = (comparison['quality'] == comparison['prediction'])
    success = (evaluation == True).sum()
    failure = (evaluation == False).sum()
    
    return success / (success+failure)

#print('(category) train set accuracy', my_score(red_df_x_train, red_df_y_train))
#print('(category) test set accuracy', my_score(red_df_x_test, red_df_y_test))
'''
# model = tf.compat.v1.global_variables_initializer()
# sc_x = preprocessing.StandardScaler()
# sc_y = preprocessing.StandardScaler()

tf.reset_default_graph()
red_df = pd.DataFrame(df)
red_df_duplicate_dropped = df.copy()
red_df_duplicate_dropped.drop_duplicates(subset=None, inplace=True)
y = red_df_duplicate_dropped[["quality"]]
x = red_df_duplicate_dropped[['sulphates','alcohol','pH']]

X = tf.compat.v1.placeholder(tf.float32, shape=[None, 3], name= "input")
Y = tf.compat.v1.placeholder(tf.float32, shape = [None, 1], name="output")
W = tf.Variable(tf.compat.v1.random_normal([3,1]), name ="weight")
b = tf.Variable(tf.compat.v1.random_normal([1]), name="bias")

hypothesis = tf.matmul(X, W)+b 
cost = tf.reduce_mean(tf.square(hypothesis - Y))
optimizer = tf.compat.v1.train.GradientDescentOptimizer(learning_rate = 0.000005)
train = optimizer.minimize(cost)

sess = tf.compat.v1.Session()
init = tf.compat.v1.global_variables_initializer()
sess.run(init)

for step in range(10000):
    hypo2, cost2 , third = sess.run([hypothesis, cost, train], feed_dict={X:x, Y:y})
    if step % 500 == 0:
        print("#",step, "Cost: ",cost2)
        print("value: ", hypo2[0])

#if os.path.isfile('models/Redwine.pkl') == False:
#    os.makedirs('models/Redwine.pkl')

#with open('models/Redwine.pkl','wb') as f: 
   # pickle.dump(model, f)
saver = tf.compat.v1.train.Saver()
save_path = saver.save(sess, 'redwinemodel/redwine.ckpt')
