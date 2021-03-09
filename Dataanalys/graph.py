# Mathias, Carl, Linus (190s)

import matplotlib.pyplot as plt
import json

#Läser in fil

while True:
    filename = str(input('Vilken fil vill du öppna? '))
    try:
        with open(filename + ".csv", "r") as f:
            data = f.read()
            dataSplit = data.split('\n')
        break
    except:
        print(filename + ' existerar inte.')
del dataSplit[-1]

x = []                 #
y = []                 #
xDiff = []             #
yDiff = []             #
ti = 0                 #
time = []
average = []

for values in dataSplit:
    value = values.split(',')
    x.append(int(value[0]))
    y.append(int(value[1]))

for q in range(0, len(x)-1):
    Xdifference = x[q]-x[q+1]
    xDiff.append(Xdifference)

for w in range(0, len(y)-1):
    Ydifference = y[w]-y[w+1]
    yDiff.append(Ydifference)

for z in range(0, len(x)-1):
    ti += 10
    time.append(ti)


plt.plot(time, xDiff)
plt.plot(time, yDiff)
plt.ylabel('hastighet')
plt.xlabel('tid')
plt.show()
