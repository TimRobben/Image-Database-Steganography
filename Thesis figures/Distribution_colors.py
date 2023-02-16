from PIL import Image
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_csv("E:\Scriptie\Methods\Github Labels\Admin\labels\\1c-DB.csv")

all_image_color = []
count_r = 0
count_g = 0
count_b = 0
for name, row in data.iterrows():
    image_name=row.imageID[0:-4]
    img = Image.open(f"E:\Scriptie\Methods\data\jpg\{row.phone}\{row.imageID}")
    dom_color = sorted(img.getcolors(2 ** 24), reverse=True)[0][1]
    all_image_color.append(dom_color)
    if max(dom_color) == dom_color[0]:
        count_r += 1
    elif max(dom_color) == dom_color[1]:
        count_g += 1
    else:
        count_b += 1
print("red",count_r)
print("green",count_g)
print("blue",count_b)
dict = {'rgb': all_image_color}
df = pd.DataFrame(dict)
df.to_csv("E:\Scriptie\Methods\RGB.csv")

