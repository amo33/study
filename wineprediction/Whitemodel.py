import tensorflow as tf 
import pandas as pd 
import numpy as np 
import pickle 
import tensorflow_datasets as tfds
from customfunction import *
while True:
    wineoption = input("What kind of wine?")

    if wineoption == 'white':
        df = pd.read_csv('winequality-white.csv',';')
        options = ['density','alcohol','residual sugar','volatile acidity','chlorides']
        break

    elif wineoption == 'red':
        df = pd.read_csv('winequality-red.csv',';')
        options = ['sulphates','alcohol','citric acid',"volatile acidity"]
        break 
    print("Type red or white")

tf.reset_default_graph()
wine_df = pd.DataFrame(df)
wine_df_duplicate_dropped = df.copy()
wine_df_duplicate_dropped.drop_duplicates(subset=None, inplace=True)
y = wine_df_duplicate_dropped[["quality"]]

x = wine_df_duplicate_dropped[options]
scaling_value = {}

parsed_index = [0 for i in range(len(options))]
i = 0
for attr in options:
    parsed_index[i] = outlier_iqr(x[attr])[0]
    i +=1
total_outlier_index = np.unique(np.concatenate((parsed_index)), 0)
print(x.shape)
Not_outlier = []

for i in x.index:
    if i not in total_outlier_index:
        Not_outlier.append(i)
x_clean = x.loc[Not_outlier]
x_clean = x_clean.reset_index(drop=True)
y_clean = y.loc[Not_outlier]
y_clean = y_clean.reset_index(drop=True)
print(x_clean.shape)
for attr in options:
    x_clean[attr] = Standardscaler(scaling_value, attr, x_clean[attr])
'''
#x_clean['density'] = Standardscaler(scaling_value,'density',x_clean['density'])
#x_clean['alcohol'] = Standardscaler('alcohol',x_clean['alcohol'])
#x_clean['residual sugar'] = Standardscaler('residual sugar',x_clean['residual sugar'])
#x_clean['chlorides'] = Standardscaler('chlorides', x_clean['chlorides'])
#x_clean['volatile acidity'] = Standardscaler('volatile acidity', x_clean['volatile acidity'])
'''
size = len(options)
X = tf.compat.v1.placeholder(tf.float32, shape=[None, size], name= "input")
Y = tf.compat.v1.placeholder(tf.float32, shape = [None, 1], name="output")

W = tf.Variable(tf.compat.v1.random_normal([size,1]), name ="weight")
b = tf.Variable(tf.compat.v1.random_normal([1]), name="bias")

hypothesis = tf.matmul(X, W)+b 
cost = tf.reduce_mean(tf.square(hypothesis - Y))
optimizer = tf.compat.v1.train.GradientDescentOptimizer(learning_rate = 1e-3)
train = optimizer.minimize(cost)

sess = tf.compat.v1.Session()
init = tf.compat.v1.global_variables_initializer()
sess.run(init)

saver = tf.compat.v1.train.Saver([W, b])

for step in range(10001):
    x_train, x_test,y_train,y_test = permutation_train_test_split(x_clean,y_clean,test_size=0.3, random_state=100)
    tmp, loss_val = sess.run([train,cost], feed_dict={X:x_train, Y:y_train})
    if step % 1000 == 0:
        print("#",step, "Cost: ",loss_val)
    if step == 10000:
        saver.save(sess, wineoption+'winemodel/train1',global_step=60000)        


print("예측값", sess.run(hypothesis, feed_dict={X:x_test}))
print("실제값", y_test)
is_correct = tf.equal(tf.round(hypothesis), y_test)
accuracy = tf.reduce_mean(tf.cast(is_correct, tf.float32))
print("정확도: ",sess.run(accuracy*100, feed_dict={X:x_test, Y:y_test}))
print(wineoption)

sess.close()

with open(wineoption+'wine.pickle','wb') as fw:
    pickle.dump(scaling_value, fw)

   


