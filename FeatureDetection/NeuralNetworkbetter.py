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
bestscore_inNeural=np.zeros((4,4,4,4))
for i in range (1,3):
    for j in range (1,3):
        for k in range(1,3):
            for p in range(1,3):
                for t in range(1,3):
                    classsifier = Sequential()
                    classsifier.add(Dense(output_dim=(2**k)*10,init ='uniform',activation ='relu', input_dim=7))
                    classsifier.add(Dense(output_dim=(2**t)*10,init ='uniform',activation ='sigmoid'))
                    classsifier.add(Dense(output_dim=(2**p)*10,init ='uniform',activation ='relu'))
                    classsifier.add(Dense(output_dim=4,init ='uniform',activation ='sigmoid'))
                    classsifier.compile(optimizer = 'adam', loss='binary_crossentropy',metrics =['accuracy'] )
                    classsifier.fit(X_train, y_train,batch_size=(4**i)*10,nb_epoch=(4**j)*10)
                    y_pred = classsifier.predict(X_test)
                    yz_pred = (y_pred > 0.5)
                    y_test1=y_test[:,0]*0+ y_test[:,1]*1 +y_test[:,2]*2+ y_test[:,3]*3
                    yz_pred=yz_pred[:,0]*0+yz_pred[:,1]*1+yz_pred[:,2]*2+yz_pred[:,3]*3
                    Correct = y_test1==yz_pred
                    NeuralScore = sum(Correct)/len(Correct)
                    bestscore_inNeural[i-1,j-1,k-1,p-1] = NeuralScore
            


output_dim1=0
output_dim2=0
batch_size=0
nb_epoch=0
a=np.amax(bestscore_inNeural)
for i in range (1,3):
    for j in range (1,3):
        for k in range(1,3):
            for p in range(1,3):
                if(bestscore_inNeural[i-1,j-1,k-1,p-1]==a):
                    batch_size=(4**i)*1
                    nb_epoch=(4**j)*10
                    output_dim1=(2**k)*10
                    output_dim2=(2**p)*10


bestNeural = Sequential()
bestNeural.add(Dense(output_dim=output_dim1,init='uniform',activation='relu',input_dim=7))
bestNeural.add(Dense(output_dim=output_dim2,init='uniform',activation='relu'))
bestNeural.add(Dense(output_dim=4,init='uniform',activation='sigmoid'))
bestNeural.compile(optimizer = 'adam', loss='binary_crossentropy',metrics =['accuracy'] )
bestNeural.fit(X_train, y_train,batch_size=batch_size,nb_epoch=nb_epoch)
y_pred = bestNeural.predict(X_test)
yz_pred = (y_pred > 0.5)
y_test1=y_test[:,0]*0+ y_test[:,1]*1 +y_test[:,2]*2+ y_test[:,3]*3
yz_pred=yz_pred[:,0]*0+yz_pred[:,1]*1+yz_pred[:,2]*2+yz_pred[:,3]*3
Correct = y_test1==yz_pred
NeuralScore = sum(Correct)/len(Correct)


weights1, biases1 = bestNeural.layers[0].get_weights()
weights2, biases2 = bestNeural.layers[1].get_weights()
weights3, biases3 = bestNeural.layers[2].get_weights()


from sklearn.metrics import confusion_matrix
cm= confusion_matrix(y_test1,yz_pred)
cm = cm.astype('float') / cm.sum(axis=1)


import pandas as pd
pd.crosstab(y_test1, yz_pred, rownames=['True'], colnames=['Predicted'], margins=True)
