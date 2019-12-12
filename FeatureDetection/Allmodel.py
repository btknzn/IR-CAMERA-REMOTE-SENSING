import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split

def decode(datum):
    return np.argmax(datum)


dataset = pd.read_csv('succes.csv')

dataset = shuffle(dataset)


    
X = dataset.iloc[:,1:8].values
y = dataset.iloc[:,8].values


for i in range(0,len(dataset)-1):
    if  y[i] == 0:
        X[i,1]=0
        X[i,2]=0
        X[i,3]=0
        X[i,4]=0
        X[i,5]=0
        X[i,6]=0
        X[i,0]=0
        
    
    


from sklearn.preprocessing import OneHotEncoder
onehotencoder = OneHotEncoder()
Y = onehotencoder.fit_transform(y.reshape(-1,1)).toarray()   


from keras.models import Sequential

from keras.layers import Convolution2D

from keras.layers import MaxPooling2D

from keras.layers import Flatten

from keras.layers import Dense

classifier = Sequential()

from sklearn.model_selection import train_test_split


X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size = 0.2, random_state = 0)
import keras 

from keras.models import Sequential

from keras.layers import Dense

# initialising the ANN



classsifier = Sequential()

#adding Laters 

classsifier.add(Dense(output_dim=800,init ='uniform',activation ='relu', input_dim=7))

classsifier.add(Dense(output_dim=800,init ='uniform',activation ='relu'))

classsifier.add(Dense(output_dim=4,init ='uniform',activation ='sigmoid'))



#compling the ANN

classsifier.compile(optimizer = 'adam', loss='binary_crossentropy',metrics =['accuracy'] )



classsifier.fit(X_train, y_train,batch_size=10,nb_epoch=100)



y_pred = classsifier.predict(X_test)

yz_pred = (y_pred > 0.5)

y_test1=y_test[:,0]*0+ y_test[:,1]*1 +y_test[:,2]*2+ y_test[:,3]*3

yz_pred=yz_pred[:,0]*0+yz_pred[:,1]*1+yz_pred[:,2]*2+yz_pred[:,3]*3

Correct = y_test1==yz_pred

NeuralScore = sum(Correct)/len(Correct)
   

dataset = pd.read_csv('succes.csv')

dataset = shuffle(dataset)


 
X = dataset.iloc[:,1:8].values
y = dataset.iloc[:,8].values


for i in range(0,len(dataset)-1):
    if  y[i] == 0:
        X[i,1]=0
        X[i,2]=0
        X[i,3]=0
        X[i,4]=0
        X[i,5]=0
        X[i,6]=0
        X[i,0]=0
        




X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

from sklearn import neighbors

clf = neighbors.KNeighborsClassifier()

clf.fit(X_train, y_train)

KNN_score=clf.score(X_test,y_test)

import sklearn.linear_model as lm

lr = lm.LinearRegression()
lr.fit(X_train, y_train)
LinearRegression_score = lr.score(X_test, y_test)


from sklearn.tree import DecisionTreeClassifier

tree = DecisionTreeClassifier(max_depth=5,max_leaf_nodes=8)
tree.fit(X_train, y_train)
tree_score = tree.score(X_test,y_test)

from sklearn.ensemble import AdaBoostClassifier
bdt = AdaBoostClassifier()
bdt.fit(X_train,y_train)
adaboostscore=bdt.score(X_test,y_test)