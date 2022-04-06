import tensorflow as tf 
import pandas as pd 
import numpy as np 
from sklearn.model_selection import train_test_split
import pickle 
import tensorflow_datasets as tfds
df = pd.read_csv('winequality-white.csv',';')
'''
standard_scaler_x = preprocessing.StandardScaler()
standard_scaler_y = preprocessing.StandardScaler()
white_df = pd.DataFrame(df)
white_df_duplicate_dropped = df.copy()
white_df_duplicate_dropped.drop_duplicates(subset=None, inplace=True)
y = white_df_duplicate_dropped[["quality"]]
X = white_df_duplicate_dropped[['sulphates','alcohol','pH']]
#X = standard_scaler_x.fit_transform(X)
#y = standard_scaler_y.fit_transform(y)
white_df_x_train, white_df_x_test,white_df_y_train, white_df_y_test = train_test_split(X,y,test_size=0.3, random_state=100)

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

model = svc_param_selection(white_df_x_train, white_df_y_train.values.ravel(),5)
                                                    # scale안하면 dataframe 상태여서 values붙여야한다.


if os.path.isfile('models/Whitewine.pkl') == False:
    os.makedirs('models/Whitewine.pkl')

with open('models/Whitewine.pkl','wb') as f: 
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
tf.reset_default_graph()
white_df = pd.DataFrame(df)
white_df_duplicate_dropped = df.copy()
white_df_duplicate_dropped.drop_duplicates(subset=None, inplace=True)
y = white_df_duplicate_dropped[["quality"]]
x = white_df_duplicate_dropped[['sulphates','alcohol','pH']]
scaling_value = {}

def min_max_scaler(col,data):
    max_val = np.max(data)
    min_val = np.min(data)
    scaling_value[col]=[max_val,min_val]

    return data.apply(lambda x: (x - min_val)/(max_val-min_val))

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
x_clean['sulphates'] = min_max_scaler('sulphates',x_clean['sulphates'])
x_clean['alcohol'] = min_max_scaler('alcohol',x_clean['alcohol'])
x_clean['pH'] = min_max_scaler('pH',x_clean['pH'])

X = tf.compat.v1.placeholder(tf.float32, shape=[None, 3], name= "input")
Y = tf.compat.v1.placeholder(tf.float32, shape = [None, 1], name="output")

W = tf.Variable(tf.compat.v1.random_normal([3,1]), name ="weight")
b = tf.Variable(tf.compat.v1.random_normal([1]), name="bias")

hypothesis = tf.matmul(X, W)+b 
cost = tf.reduce_mean(tf.square(hypothesis - Y))
optimizer = tf.compat.v1.train.GradientDescentOptimizer(learning_rate = 1e-4)
train = optimizer.minimize(cost)

sess = tf.compat.v1.Session()
init = tf.compat.v1.global_variables_initializer()
sess.run(init)

saver = tf.compat.v1.train.Saver([W, b])
print(x_clean.head(10))
for step in range(300001):
    x_train, x_test,y_train,y_test = train_test_split(x_clean,y_clean,test_size=0.3, random_state=100, shuffle=True)
    #x_train, x_test,y_train,y_test = tfds.load(
        #
    #)
    tmp, loss_val = sess.run([train,cost], feed_dict={X:x_train, Y:y_train})
    if step % 1000 == 0:
        print("#",step, "Cost: ",loss_val)
        
        saver.save(sess, 'whitewinemodel/train1',step)

sess.close()

with open('whitewine.pickle','wb') as fw:
    pickle.dump(scaling_value, fw)

#if os.path.isfile('models/Whitewine.pkl') == False:
#    os.makedirs('models/Whitewine.pkl')

#with open('models/Redwine.pkl','wb') as f: 
   # pickle.dump(model, f)
   


