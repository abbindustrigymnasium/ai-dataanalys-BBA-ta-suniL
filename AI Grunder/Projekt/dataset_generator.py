import matplotlib.pyplot as plt
import numpy as np
from cv2 import cv2
import os
# %matplotlib inline

path = './images'

training_data = []
for img in os.listdir(path):
    pic = cv2.imread(os.path.join(path, img))
    pic = cv2.cvtColor(pic, cv2.COLOR_BGR2RGB)
    pic = cv2.resize(pic, (80, 80))
    training_data.append([pic])

np.save(os.path.join(path, 'features'), np.array(training_data))
saved = np.load(os.path.join(path, 'features.npy'))

plt.imshow(saved[0].reshape(80, 80, 3))
plt.imshow(np.array(training_data[0]).reshape(80, 80, 3))
