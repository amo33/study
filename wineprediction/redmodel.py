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
'''tf.reset_default_graph()
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
'''
tf.reset_default_graph()
white_df = pd.DataFrame(df)
white_df_duplicate_dropped = df.copy()
white_df_duplicate_dropped.drop_duplicates(subset=None, inplace=True)
y = white_df_duplicate_dropped[["quality"]]
x = white_df_duplicate_dropped[['sulphates','alcohol','pH']]
scaling_value = {}

def Standardscaler(col,data):
    mean_val = np.mean(data)
    std_val = np.std(data)
    scaling_value[col]=[mean_val,std_val]

    return data.apply(lambda x: (x - mean_val)/(std_val))

def outlier_iqr(data):
    q1, q3 = np.percentile(data, [25,75])
    
    iqr = q3 - q1 
    lower_bound = q1 - (iqr*1.5)
    upper_bound = q3 + (iqr*1.5)
    
    return np.where((data > upper_bound)|(data < lower_bound))


pH_outlier_index = outlier_iqr(x['pH'])[0]
sulphates_outlier_index = outlier_iqr(x['sulphates'])[0]
alcohol_outlier_index = outlier_iqr(x['alcohol'])[0]

total_outlier_index = np.unique(np.concatenate((pH_outlier_index, sulphates_outlier_index, alcohol_outlier_index)), 0)
print(total_outlier_index)
Not_outlier = []
print(x.shape)
for i in x.index:
    if i not in total_outlier_index:
        Not_outlier.append(i)
x_clean = x.loc[Not_outlier]
x_clean = x_clean.reset_index(drop=True)
y_clean = y.loc[Not_outlier]
y_clean = y_clean.reset_index(drop=True)
print(y_clean.shape)
print(x_clean.shape)
x_clean['sulphates'] = Standardscaler('sulphates',x_clean['sulphates'])
x_clean['alcohol'] = Standardscaler('alcohol',x_clean['alcohol'])
x_clean['pH'] = Standardscaler('pH',x_clean['pH'])

X = tf.compat.v1.placeholder(tf.float32, shape=[None, 3], name= "input")
Y = tf.compat.v1.placeholder(tf.float32, shape = [None, 1], name="output")

W = tf.Variable(tf.compat.v1.random_normal([3,1]), name ="weight")
b = tf.Variable(tf.compat.v1.random_normal([1]), name="bias")

hypothesis = tf.matmul(X, W)+b 
cost = tf.reduce_mean(tf.square(hypothesis - Y))
optimizer = tf.compat.v1.train.GradientDescentOptimizer(learning_rate = 1e-4)
train = optimizer.minimize(cost)
acc = tf.equal(tf.round(hypothesis), Y)
acc = tf.reduce_mean(tf.cast(acc, tf.float32))
sess = tf.compat.v1.Session()
init = tf.compat.v1.global_variables_initializer()
sess.run(init)

saver = tf.compat.v1.train.Saver()
print(x_clean.head(10))
print(y_clean.head(10))
for step in range(10001):
    x_train, x_test,y_train,y_test = train_test_split(x_clean,y_clean,test_size=0.3, random_state=100)
    #x_train, x_test,y_train,y_test = tfds.load(
        #
    #)
    
    tmp, loss_val , y_val = sess.run([train,cost,hypothesis], feed_dict={X:x_train, Y:y_train})
    if step % 1000 == 0:

        print("#",step, "Cost: ",loss_val)
        print('# predict:',y_val[step%1000])
        #print('# real value:',y_train[step])
    if step == 10000:
        saver.save(sess, 'redwinemodel/train1',global_step=60000)        

print("예측값", sess.run(hypothesis, feed_dict={X:x_test}))
print("실제값", y_test)
is_correct = tf.equal(tf.round(hypothesis)+1, y_test)
accuracy = tf.reduce_mean(tf.cast(is_correct, tf.float32))
print("정확도: ",sess.run(accuracy*100, feed_dict={X:x_test, Y:y_test}))

'''
for i in range(len(x_train)):
    h_val = sess.run(hypothesis, feed_dict={X: x_train.iloc[i,:].reshape(1,)})
    print("Answer:", y_train[i], " Prediction:", h_val)

cost_val, acc_val = sess.run([cost, acc], feed_dict={X:x_train, Y:y_train})
print("Cost:", cost)
print("Acc:",acc_val)

print("===========prediction===========")
for i in range(x_test.shape[0]):
    pre = sess.run(hypothesis, feed_dict={X: x_test.iloc[i].reshape(1,)})
    print(x_test[i],"=>",pre[0])
'''
sess.close()

with open('redwine.pickle','wb') as fw:
    pickle.dump(scaling_value, fw)

#https://jjeamin.github.io/posts/Checkpoint/ 그래프 따로 저장 
#https://blog.naver.com/PostView.nhn?blogId=rhrkdfus&logNo=221480101170 모델 저장 공부용 . graph랑 헷갈리면 안된다.