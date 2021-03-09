# Mathias, Carl, Linus (190s)

import matplotlib.pyplot as plt
import json
import os


def clear():
    if os.name == 'nt':
        os.system("cls")
    else:
        os.system("clear")


while True:

    clear()
    print('-'*20)
    filename = str(input('Vilken fil vill du öppna? '))
    try:
        with open(filename + ".csv", "r") as f:
            data = f.read()
            dataSplit = data.split('\n')
        break
    except:
        print(filename + ' existerar inte.')
del dataSplit[-1]

x = []
y = []
xDiff = []
yDiff = []
ti = 0
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

plt.plot(x, y)
plt.ylabel('rörelse y')
plt.xlabel('rörelse x')
plt.show()
