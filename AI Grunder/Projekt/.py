# https://youtu.be/iGWbqhdjf2s?t=540
# https://github.com/abbjoafli/ComputerVision

from keras.datasets import cifar10
import tensorflow as tf
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense, Flatten, Conv2D, MaxPooling2D, Dropout
from tensorflow.keras import layers
from keras.utils import to_categorical
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

# Load data
(x_train, y_train), (x_test, y_test) = cifar10.load_data()

# Look at the data types of the variables
print(type(x_train))
print(type(y_train))
print(type(x_test))
print(type(y_test))

# Get the shapes of the arrays
print('x_train:', x_train.shape)
print('y_train:', y_train.shape)
print('x_test:', x_test.shape)
print('y_test:', y_test.shape)

# Take a look at the first image as an array
index = 0
x_train[index]

# Show the image as a picture
img = plt.imshow(x_train[index])
