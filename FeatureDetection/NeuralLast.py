import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split

def decode(datum):
    return np.argmax(datum)


dataset = pd.read_csv('succes.csv')

dataset = shuffle(dataset)

from sklearn.preprocessing import StandardScaler

    
X = dataset.iloc[:,1:8].values
y = dataset.iloc[:,8].values
p=0
#I made some noises on dataset.
for i in range(0,len(dataset)-1):
    if  y[i] == 0:
        p=p+1
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

X = StandardScaler().fit_transform(X)

from sklearn.decomposition import PCA
pca = PCA(n_components=7)
X = pca.fit_transform(X)


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

classsifier = Sequential()
classsifier.add(Dense(output_dim=60,init ='uniform',activation ='relu', input_dim=7))
classsifier.add(Dense(output_dim=60,init ='uniform',activation ='sigmoid'))
classsifier.add(Dense(output_dim=4,init ='uniform',activation ='sigmoid'))
y_pred = bestNeural.predict(X_test)
yz_pred = (y_pred > 0.5)

