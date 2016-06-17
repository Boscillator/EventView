from tkinter import *
from tkinter.ttk import *
from ParticalTree import ParticalTree
import csv
import pandas as pd

print("Event Display Program Loaded!")
print("Writen by Fred Buchanan (oscillator.b@gmail.com)")

print("Reading Data")
df = pd.read_csv('input/event_0.csv')
df = df[df["id"]>50]

print("Inizilizing Graphics")
root = Tk()

w = Label(root, text="Event Viewer!")
w.pack()
pt = ParticalTree(root,df)
sg = Sizegrip()
sg.pack()

print("Staring Graphics")
root.mainloop()

print("Running...")