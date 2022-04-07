
 ### These codes below are my own savings in order to remember model calling in tensorflow 1.15
 '''python
    this example is when I use pickle to save model(I didn't use this method)
    if winedata == 'red':
        model = pickle.load(open('models/Redwine.pkl','rb')) #pickle 사용을 추천합니다 instead of sklearn.joblib
        # but this time, I used ckpt for tensorflow 1.15 (please use ckpt to save model)
    elif winedata == 'white':
        model = pickle.load(open('models/Whitewine.pkl','rb'))
        
    #prediction = model.predict(data) -> data 활용해서 구하면 된다.
    #print(prediction)
    #print(model.best_estimator_.coef_) 
'''

'''python 
        size= 3
        X = tf.placeholder(tf.float32, shape=[None, size])
        W = tf.Variable(tf.random_normal([size, 1]), name='weight')
        b = tf.Variable(tf.random_normal([1]), name='bias')
        sess = tf.Session()
        sess.run(tf.global_variables_initializer())
        hypothesis = tf.add(tf.matmul(X,W),b)
        prediction = tf.round(hypothesis)
        #If I use this method after calling the model, there is an error on using weight and bias.(It doesn't call the right trained one.) 
'''

#### This code is using Sklearn Scaler and GRIDSEARCHCV. Because of using GRIDCV it was too slow. (So I didn't use it.)
'''python
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


 model = svm.SVR(kernel='linear') #,validation_split = 0.33 , callbacks=[model_callback]
 for i in range(10):
   start = i*139
   end = start + 139
   model.fit(red_df_x_train.loc[[i not in range(start,end)], :], red_df_y_train)
 model.fit(red_df_x_train, red_df_x_test) # 왜 cross validation 구현을 못하겠지?

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

##### For Tensorflow 1.x - We use sess(tf.session 's) to train. And we find out the predcition rate. 
##### This example, I used test data for model's accuarcy but, normally we use validation data to prevent overfitting.
'''python 
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