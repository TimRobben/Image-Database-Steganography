import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#read data
data = pd.read_csv('/media/tim/Backup Plus/Scriptie/methods/Github Labels/admin/labels/1c-DB.csv')

# mean complexity per method
mean_complexity = data.groupby(['method'])['complexity'].mean()
box = mean_complexity.plot.box(title = 'Distribution of complexity across methods', xlabel = 'Methods', ylabel = 'Complexity')
box.set(xticklabels=['Methods'])
plt.show()

# mean_images = data.groupby(['phone']).size()
# print(mean_images)
# mean_images.plot.bar(title = 'Amount of images on each phone', xlabel = 'Phones', ylabel = 'Amount of images')


# data = pd.DataFrame({'Phone': ['APPLE Ipod touch', 'ASUS Zenfone 8', 'HUAWEI EML-L09', 'ONEPLUS Nord CE 5G','OPPO Find X3 Lite',
#                     'OPPO Find X3 Neo', 'SAMSUNG Galaxy A32', 'SAMSUNG Xcover Pro', 'SONY Xperia 1 III', 'XIAOMI Mi 11i', 'XIAOMI Poco F3'],
#         'Images': [1001, 1012, 1001, 1012, 990, 1001, 1001, 1012, 1023, 1001, 1012]}).set_index('Phone')
#
#
#
# #print(data)
# data.plot.bar(by = 'Phone', title = 'Amount of images on each phone', xlabel = 'Phones', ylabel = 'Amount of images', legend = None)
# plt.axhline(y = 1006, c = 'red')
# plt.show()
