# -*- coding: utf-8 -*-
"""cfiar_pred.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1iTK2zg7UYjFT1Otmg-c0FVclz4nCkQMt
"""

from google.colab import drive
 
drive.mount('/content/gdrive/')

import zipfile
from google.colab import drive

drive.mount('/content/drive/')

zip_ref = zipfile.ZipFile("/content/ciafr.zip", 'r')
zip_ref.extractall()
zip_ref.close()

from keras.layers import Conv2D, Activation, GlobalAvgPool2D, MaxPooling2D, Dropout, Dense, Flatten

from keras.models import Sequential

file1 = ("/content/CIFAR100/TEST")

file2 = ("/content/CIFAR100/VALID")

from keras.preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(rescale = 1./255,
                                   shear_range = 0.05,
                                   zoom_range = 0.05,
                                   horizontal_flip = True)

train_set = train_datagen.flow_from_directory(file1,
                                                 target_size = (384, 384),
                                                 batch_size = 16,
                                                 subset='training',
                                                 class_mode = 'categorical')

import matplotlib.pyplot as plt



test_datagen = ImageDataGenerator(rescale = 1./255)

test_set = test_datagen.flow_from_directory(file2,
                                            target_size = (384, 384),
                                            batch_size = 16,
                                            subset='validation',
                                            class_mode = 'categorical')

model = Sequential()
model.add(Dense(100, input_shape=(384,384, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=[3,3], strides=2, padding='valid'))
model.add(Dropout(.20))
model.add(Dense(100, activation='relu'))
model.add(MaxPooling2D(pool_size=[3,3], strides=2, padding='valid'))
model.add(Dense(100, activation='relu'))
model.add(MaxPooling2D(pool_size=[3,3], strides=2, padding='valid'))
model.add(Dropout(.20))

model.add(Dense(64, activation='relu'))
model.add(MaxPooling2D(pool_size=[3,3], strides=2, padding='valid'))
model.add(Flatten())

model.add(Dense(100, activation='sigmoid'))
model.summary()

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['categorical_accuracy'])

history = model.fit(train_set, validation_data =test_set, epochs=30, verbose=2)

history.history['categorical_accuracy']

plt.figure(figsize =(6,4))
plt.plot(history.history['categorical_accuracy'])
plt.title("Accuracy after I used  more dropouts and of maxpooling")
plt.show()

history.history['loss']

plt.figure(figsize =(6,4))
plt.plot(history.history['loss'])
plt.title('Loss after I used more dropouts and maxpooling')
plt.show()

model.save("cfiar_pred.h5")

import cv2

import matplotlib.pyplot as plt

import numpy as np


x = plt.imread('/content/python3.jpg')
plt.imshow(x)

x = x/255

x = np.resize(x,(1,384,384,3))

x.shape

classes = list(train_set.class_indices)

print(classes[np.argmax(model.predict(x))])