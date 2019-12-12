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

# Finding Bests Neural Network values
bestscore_inNeural=np.zeros((4,4,4,4))
for i in range (1,3):
    for j in range (1,3):
        for k in range(1,3):
            for p in range(1,3):
                classsifier = Sequential()
                classsifier.add(Dense(output_dim=(2**k)*10,init ='uniform',activation ='relu', input_dim=7))
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
            

#Finding Bests DecisionTreeClassifier            
from sklearn.tree import DecisionTreeClassifier
bestscore_inDecision = np.zeros((10,10))
for i in range (1,10):
    for k in range(1,10):
        tree = DecisionTreeClassifier(max_depth=i,min_samples_leaf=k)
        tree.fit(X_train, y_train)
        tree_score = tree.score(X_test,y_test) 
        bestscore_inDecision[i-1,k-1]=tree_score


                
#Finding Bests Score in KNeighborsClassification                 
from sklearn.neighbors import KNeighborsClassifier
bestscore_KNN =np.zeros((200))
for i in range (1,200):
    KNN =  KNeighborsClassifier(n_neighbors =i)
    KNN.fit(X_train, y_train)
    bestscore_KNN[i-1]=KNN.score(X_test,y_test)
    

        
            
#THİS PART GOİNG TO FİND İMPORTANT VALUES OF MODELS.
a=np.amax(bestscore_KNN)
KNN_number=0
for i in range(0,len(bestscore_KNN)):
    if (a == bestscore_KNN[i]):
        KNN_number=i

a=np.amax(bestscore_inDecision)
max_depth=0;
min_sample_leaf=0
for i in range(0,len(bestscore_inDecision[:])):
    for j in range(0,len(bestscore_inDecision)):
        if (bestscore_inDecision[i,j]==a):
            max_depth=i
            min_sample_leaf=j

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
                    
                    

   
    
#THİS PART GOİNG TO İMPLEMENT BEST MODELS WİTH BEST PARAMATERS.
#Neural Network Part
classifier = Sequential()
classsifier.add(Dense(output_dim=output_dim1,init ='uniform',activation ='relu', input_dim=7))
classsifier.add(Dense(output_dim=output_dim2,init ='uniform',activation ='relu'))
classsifier.add(Dense(output_dim=4,init ='uniform',activation ='sigmoid'))
classsifier.compile(optimizer = 'adam', loss='binary_crossentropy',metrics =['accuracy'] )
classsifier.fit(X_train, y_train,batch_size=batch_size,nb_epoch=nb_epoch)
y_pred = classsifier.predict(X_test)
yz_pred = (y_pred > 0.5)
y_test1=y_test[:,0]*0+ y_test[:,1]*1 +y_test[:,2]*2+ y_test[:,3]*3
yz_pred=yz_pred[:,0]*0+yz_pred[:,1]*1+yz_pred[:,2]*2+yz_pred[:,3]*3
Correct = y_test1==yz_pred
NeuralScore = sum(Correct)/len(Correct)

#KNN PART
KNN =  KNeighborsClassifier(n_neighbors =KNN_number)
KNN.fit(X_train, y_train)
KNN_score=KNN.score(X_test,y_test)

#Decision TREE
tree = DecisionTreeClassifier(max_depth=max_depth,min_samples_leaf=min_sample_leaf)
tree.fit(X_train,y_train)
tree_score = tree.score(X_test,y_test) 

#Making new dataset from models
X_tra=np.zeros((len(X_train),3))
Y_tra=np.zeros((len(X_train),1)) 
y_pred=classsifier.predict(X_train)
yz_pred = (y_pred > 0.5)
yz_pred=yz_pred[:,0]*0+yz_pred[:,1]*1+yz_pred[:,2]*2+yz_pred[:,3]*3
X_tra[:,0]=yz_pred[:]
y_pred=KNN.predict(X_train)
yz_pred = (y_pred > 0.5)
yz_pred=yz_pred[:,0]*0+yz_pred[:,1]*1+yz_pred[:,2]*2+yz_pred[:,3]*3
X_tra[:,1]=yz_pred[:]
y_pred=tree.predict(X_train)
yz_pred = (y_pred > 0.5)
yz_pred=yz_pred[:,0]*0+yz_pred[:,1]*1+yz_pred[:,2]*2+yz_pred[:,3]*3
X_tra[:,2]=yz_pred[:]
Y_tra=y_train

#Finding Best Tree
tree2 = DecisionTreeClassifier(max_depth=max_depth,min_samples_leaf=min_sample_leaf)               
#evaluating our model
X_t=np.zeros((len(X_test),3))
Y_t=np.zeros((len(X_test),1))
y_pred=classsifier.predict(X_test)
yz_pred = (y_pred > 0.5)
yz_pred=yz_pred[:,0]*0+yz_pred[:,1]*1+yz_pred[:,2]*2+yz_pred[:,3]*3
X_t[:,0]=yz_pred[:]
y_pred=KNN.predict(X_test)
yz_pred = (y_pred > 0.5)
yz_pred=yz_pred[:,0]*0+yz_pred[:,1]*1+yz_pred[:,2]*2+yz_pred[:,3]*3
X_t[:,1]=yz_pred[:]
y_pred=tree.predict(X_test)
yz_pred = (y_pred > 0.5)
yz_pred=yz_pred[:,0]*0+yz_pred[:,1]*1+yz_pred[:,2]*2+yz_pred[:,3]*3
X_t[:,2]=yz_pred[:]
Y_t=y_test             


bestscore_inDecision_last=np.zeros((10,10))
for i in range (1,10):
    for k in range(1,10):
        tree3 = DecisionTreeClassifier(max_depth=i,min_samples_leaf=k)
        tree3.fit(X_tra, Y_tra)
        tree_score = tree3.score(X_t,Y_t) 
        bestscore_inDecision_last[i-1,k-1]=tree_score


BESTSCORE=np.amax(bestscore_inDecision_last)    
# Apply the result of 6 different Maschine learning model to  Random Forest Classificaiton and Decision Tree Classification and find your Enseble Model
# Test your data

from sklearn.metrics import confusion_matrix
cm= confusion_matrix(yz_pred,y_test1)
cm = cm.astype('float') / cm.sum(axis=1)


