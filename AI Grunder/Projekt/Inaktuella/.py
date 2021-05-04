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

# Get image label
print('The image label is:', y_train[index])

# Get the image classification
classification = ['airplane', 'automobile', 'bird', 'cat',
                  'deer', 'dog', 'frog', 'horse', 'ship', 'truck']
print('The image class is:', classification[y_train[index][0]])

# Convert the labels into a set of 10 numbers to input into the neural network
y_train_one_hot = to_categorical(y_train)
y_test_one_hot = to_categorical(y_test)

# Print the new labels
print(y_train_one_hot)

# Print the new label of the image/picture above
print('The one hot label is:', y_train_one_hot[index])

# Normalize the pixels to be values between 0 and 1
x_train = x_train / 100
x_test = x_test / 100

# Create the model's architecture
model = Sequential()
# Add the first layer
model.add(Conv2D(32, (5, 5), activation='relu', input_shape=(32, 32, 3)))
# Add a pooling layer
model.add(MaxPooling2D(pool_size=(2, 2)))
# Add another convolution layer
model.add(Conv2D(32, (5, 5), activation='relu'))
# Add another pooling layer
model.add(MaxPooling2D(pool_size=(2, 2)))
# Add a flattetning layer
model.add(Flatten())
# Add a layer with 1000 neurons
model.add(Dense(1000, activation='relu'))
# Add a dropout layer
model.add(Dropout(0.5))
# Add a layer with 500 neurons
model.add(Dense(500, activation='relu'))
# Add a dropout layer
model.add(Dropout(0.5))
# Add a layer with 250 neurons
model.add(Dense(250, activation='relu'))
# Add a layer with 10 neurons
model.add(Dense(10, activation='softmax'))

# Compile the model
model.compile(loss='categorical_crossentropy',
              optimizer='adam', metrics=['accuracy'])

# Train the model
hist = model.fit(x_train, y_train_one_hot, batch_size=256,
                 epochs=10, validation_split=0.2)

# Evaluate the model using the test data set
model.evaluate(x_test, y_test_one_hot)[1]
