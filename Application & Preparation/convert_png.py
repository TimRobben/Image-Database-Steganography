"""This code converts jpg to png, which is needed for the DCT1 and DCT3 method"""

# importing
from PIL import Image
import os
import pandas as pd

#read the data
data = pd.read_csv('/media/tim/Backup Plus/Scriptie/Methods/Github Labels/admin/labels/1c-DB.csv')

# list of phones
phones = os.listdir("/media/tim/Backup Plus/Scriptie/Methods/data/jpg")

# list of jpg's
# steg = []
# for image in os.listdir(f"/media/tim/Backup Plus/Scriptie/Methods/data/png/HUAWEI EML-L09 - NOHDR"):
#     steg.append(image[0:-4])

# converting to png
# for phone in phones:
#     for image in os.listdir(f"/media/tim/Backup Plus/Scriptie/Methods/data/jpg/{phone}"):
#         image_name = image[0:-4]
#         for name, row in data.iterrows():
#             if row.method == 6:
#                 path = f"/media/tim/Backup Plus/Scriptie/Methods/data/jpg/{phone}/{image}"
#                 dest_path = f"/media/tim/Backup Plus/Scriptie/Methods/data/png/{phone}/{image_name}.png"
#                 im1 = Image.open(path)
#                 im1.save(dest_path)
#                 print(path)
#                 print('saved')

for phone in phones:
    for image in os.listdir(f"/media/tim/Backup Plus/Scriptie/Methods/data/jpg/{phone}"):
        image_name = image[0:-4]
        path = f"/media/tim/Backup Plus/Scriptie/Methods/data/jpg/{phone}/{image}"
        dest_path = f"/media/tim/Backup Plus/Scriptie/Methods/data/png/{phone}/{image_name}.png"
        im1 = Image.open(path)
        im1.save(dest_path)
