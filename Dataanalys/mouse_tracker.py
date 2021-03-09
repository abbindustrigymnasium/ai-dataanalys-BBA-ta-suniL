import csv
import os
from time import sleep
from ctypes import windll, Structure, c_long, byref


class POINT(Structure):
    _fields_ = [("x", c_long), ("y", c_long)]


def queryMousePosition():
    pt = POINT()
    windll.user32.GetCursorPos(byref(pt))
    return [pt.x, pt.y]


def clear():
    if os.name == 'nt':
        os.system("cls")
    else:
        os.system("clear")


clear()
print('-'*20)
filename = str(input('Vad vill du döpa filen till? '))

while True:
    sleep(0.01)
    with open(filename + '.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(queryMousePosition())
