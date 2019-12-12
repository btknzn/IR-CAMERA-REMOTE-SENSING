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


classifier = Sequential()

from sklearn.model_selection import train_test_split


X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size = 0.2, random_state = 0)
import keras 

from keras.models import Sequential

from keras.layers import Dense


classifier.add(Dense(output_dim=60,init ='uniform',activation ='relu', input_dim=7))
classifier.add(Dense(output_dim=60,init ='uniform',activation ='relu'))
classifier.add(Dense(output_dim=4,init ='uniform',activation ='sigmoid'))
classifier.compile(optimizer = 'adam', loss='binary_crossentropy',metrics =['accuracy'] )
classifier.fit(X_train, y_train,batch_size=15,nb_epoch=15)

y_pred = classifier.predict(X_test)
yz_pred = (y_pred > 0.5)
y_test1=y_test[:,0]*0+ y_test[:,1]*1 +y_test[:,2]*2+ y_test[:,3]*3
yz_pred=yz_pred[:,0]*0+yz_pred[:,1]*1+yz_pred[:,2]*2+yz_pred[:,3]*3
Correct = y_test1==yz_pred
NeuralScore = sum(Correct)/len(Correct)

weights1, biases1 = classifier.layers[0].get_weights()
weights2, biases2 = classifier.layers[1].get_weights()
weights3, biases3 = classifier.layers[2].get_weights()

File_object = open("Bias1.txt","a")
for i in range (0,len(biases1)):
    File_object.write(str(round(biases1[i]*1000,2)))
    File_object.write('x')

File_object.close()
File_object = open("Bias2.txt","a")

for i in range (0,len(biases2)):
    File_object.write(str(round(biases2[i]*1000,2)))
    File_object.write('x')

File_object.close()    
File_object = open("Bias3.txt","a")


for i in range (0,len(biases3)):
    File_object.write(str(round(biases3[i]*1000,2)))
    File_object.write('x')

File_object.close()

File_object = open("Weight1.txt","a")   

for i in range(0,len(weights1)):
    for j in range (0,len(weights1[1])):
        File_object.write(str(round(weights1[i,j]*1000,2)))
        File_object.write('x')
    

File_object.close()
File_object = open("Weight2.txt","a") 
for i in range(0,len(weights2)):
    for j in range(0,len(weights2[1])):
        File_object.write(str(round(weights2[i,j]*1000,2)))
        File_object.write('x')
   

File_object.close()
File_object = open("Weight3.txt","a")         
for i in range(0,len(weights3)):
    for j in range(0,len(weights3[1])):
        File_object.write(str(round(weights3[i,j]*1000,2)))
        File_object.write('x')
    
        

File_object.close()