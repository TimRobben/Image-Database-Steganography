
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import csv

all_data = pd.read_csv("E:\Scriptie\Methods\RGB.csv") # can also index sheet by name or fetch all sheets


# DataFrame to List of Lists
lst = all_data.values.tolist()
# List of Lists to List of Tuples:
tuple_data = [tuple(x) for x in lst]


# Data points from the list of tuples
x, y, z = zip(*tuple_data)
RGB =[]
for tuple in tuple_data:
    value = [x/255 for x in tuple]
    RGB.append(value)

# red = all_data['red'].tolist()
# green = all_data['green'].tolist()
# blue = all_data['blue'].tolist()

fig = plt.figure()
ax = plt.axes(projection ='3d')

# Data for three-dimensional scattered points
# zdata = blue
# xdata = red
# ydata = green
# list_data = all_data.values.tolist()

# ax.scatter3D(x,y,z, c=RGB)
ax.scatter3D(x,y,z, c= x, cmap = 'Greens')
ax.set_zlabel('Blue')
ax.set_ylabel('Green')
ax.set_xlabel('Red')
plt.show()