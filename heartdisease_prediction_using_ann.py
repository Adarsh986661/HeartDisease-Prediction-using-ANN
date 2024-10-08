# -*- coding: utf-8 -*-
"""Heartdisease prediction using ANN.ipynb
"""

import sys
import pandas as pd
import numpy as np
import sklearn
import matplotlib
import keras
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix
import seaborn as sns
df = pd.read_csv("heart.csv")
df.head()

data = df.dropna(axis=0)
data.loc[0:]

print(data.shape)
print(data.dtypes)

data.describe()

data.hist(figsize = (12,12))
plt.show()
pd.crosstab(data.age,data.target).plot(kind = "bar",figsize=(20,6))
plt.title('Heart Disease Frequency for Ages')
plt.xlabel('Age')
plt.ylabel('Frequency')
plt.show()
plt.figure(figsize=(10,10))
sns.heatmap(data.corr(),annot=True,fmt='.1f')
plt.show()

X = np.array(data.drop(['target'],axis=1))
y = np.array(data['target'])
mean = X.mean(axis=0)
X-=mean
std = X.std(axis=0)
X/=std

from sklearn import model_selection
X_train, X_test, y_train, y_test = model_selection.train_test_split(X,y,stratify=y,random_state=42,test_size = 0.2)
from keras.utils import to_categorical
Y_train = to_categorical(y_train,num_classes=None)
Y_test = to_categorical(y_test, num_classes=None)
print(Y_train.shape)
print(Y_train[:10])
X_train[0]

from keras.models import Sequential
from keras.layers import Dense
from tensorflow.keras.optimizers import Adam
from keras.layers import Dropout
from keras import regularizers
def create_model():
  model = Sequential()
  model.add(Dense(16,input_dim=13,kernel_initializer='normal',kernel_regularizer=regularizers.l2(0.001),activation='relu'))
  model.add(Dropout(0.25))
  model.add(Dense(8, kernel_initializer='normal', kernel_regularizer=regularizers.l2 (0.001), activation='relu'))
  model.add(Dropout(0.25))
  model.add(Dense (2, activation='softmax'))
  adam = Adam (learning_rate=0.001)
  model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
  return model
model = create_model()
print (model.summary())
history=model.fit (X_train, Y_train, validation_data=(X_test, Y_test), epochs=50, batch_size=10)
history=model.fit (X_train, Y_train, validation_data=(X_test, Y_test), epochs=50, batch_size=10)

# Commented out IPython magic to ensure Python compatibility.
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model Loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train','test'])
plt.show()
import matplotlib.pyplot as plot
# %matplotlib inline

plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Model Accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train','test'])
plt.show()

Y_train_binary = y_train.copy()
Y_test_binary = y_test. copy()
Y_train_binary [Y_train_binary > 0] = 1
Y_test_binary [Y_test_binary > 0] = 1
print (Y_train_binary[:20])

def create_binary_model():

   model = Sequential()
   model.add(Dense(16, input_dim=13, kernel_initializer='normal', kernel_regularizer=regularizers.l2(0.001), activation='relu'))
   model.add(Dropout(0.25))
   model.add(Dense(8, kernel_initializer='normal', kernel_regularizer=regularizers.l2(0.001), activation='relu'))
   model.add(Dropout(0.25))
   model.add(Dense(1, activation='sigmoid'))

   adam = Adam (learning_rate=0.001)
   model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
   return model
binary_model = create_binary_model()
print (binary_model.summary())

history=binary_model.fit (X_train, Y_train_binary, validation_data=(X_test, Y_test_binary), epochs=50, batch_size=10)

# Commented out IPython magic to ensure Python compatibility.
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model Loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train','test'])
plt.show()

import matplotlib.pyplot as plot
# %matplotlib inline

plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Model Accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train','test'])
plt.show()

import random
best=-100000
populations = [[1,0,0,0,1],[1,1,1,0,1],[0,1,0,0,0],[1,0,0,1,1]]
parents=[]
new_populations = []
print(populations)

def fitness_score() :
    global populations,best
    fit_value = []
    fit_score = []
    for i in range(4) :
      chromosome_value = 0
      for j in range(4,0,-1) :
        chromosome_value += populations[i][j]*(2**(4-j))
      chromosome_value = -1*chromosome_value if populations[i][0]==1 else chromosome_value
      print(chromosome_value)
      fit_value.append(-(chromosome_value**2) + 5)
    print(fit_value)
    fit_value, populations = zip(*sorted(zip(fit_value,populations),reverse = True))
    best = fit_value[0]
fitness_score()

def selectparent():
    global parents
    parents=populations[0:2]
    print(type(parents))
    print(parents)
selectparent()

def crossover():
    global parents
    cross_point = random.randint(0,5)
    parents = parents + tuple([(parents[0][0:cross_point + 1]+parents[1][cross_point +1:6])])
    parents = parents + tuple([(parents[1][0:cross_point +1] +parents[0][cross_point+1:6])])
    print(parents)
crossover()

def mutation():
    global populations,parents
    mute = random.randint(0,49)
    if mute==20:
      x = random.randint(0,3)
      y = random.randint(0,4)
      parents[x][y]= 1-parents[x][y]
    populations = parents
    print(populations)
mutation()

for i in range(100):
  fitness_score()
  selectparent()
  crossover()
  mutation()
print("best score: ")
print(best)
print("sequence:.......")
print(populations[0])

print("best score: ")
print(best)
print("sequence:.......")
print(populations[0])

from sklearn.metrics import classification_report,accuracy_score

categorical_pred = np.argmax(model.predict(X_test),axis=1)

print('Results for Categorical Model i.e Just ANN model')
print(accuracy_score(y_test,categorical_pred))
print(classification_report(y_test,categorical_pred))

from sklearn.metrics import classification_report,accuracy_score

binary_pred = np.round(binary_model.predict(X_test)).astype(int)

print('Results for Binary Model i.e Optimized ANN with Genetic Algorithm')
print(accuracy_score(Y_test_binary,binary_pred))
print(classification_report(Y_test_binary,binary_pred))