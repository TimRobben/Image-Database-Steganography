#!/usr/bin/python3
# 3D Heatmap in Python using matplotlib



# importing required libraries
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pylab import *

# reading a dummy dataset
# dataset = pd.read_csv("E:\Scriptie\Methods\RGB.csv")
# x = dataset["red"].tolist()
# y = dataset["green"].tolist()
# z = dataset["blue"].tolist()

all_data = pd.read_csv("E:\Scriptie\Methods\RGB.csv")
lst = all_data.values.tolist()
tuple_data = [tuple(x) for x in lst]


# Data points from the list of tuples
x, y, z = zip(*tuple_data)

# colo = dataset.values.tolist()
plt.contourf(x,y) #reshape Z too!
plt.colorbar()

# # creating 3d figures
# fig = plt.figure(figsize=(8, 5))
# ax = fig.add_subplot(111, projection='3d')

# # configuring colorbar
# color_map = cm.ScalarMappable(cmap=cm.gray)
# color_map.set_array(colo)

# # creating the heatmap
# img = ax.scatter(x, y, z,
# 				s=10, color='gray')
# plt.colorbar(color_map)

# # adding title and labels
# ax.set_xlabel('Red')
# ax.set_ylabel('Green')
# ax.set_zlabel('Blue')

# # displaying plot
# plt.show()
