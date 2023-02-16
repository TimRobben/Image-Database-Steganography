import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

Sample = pd.read_excel("E:\Scriptie\Methods\Sampledata.xlsx")
mean_PSNR = Sample.groupby(['Methode'])['PSNR'].mean()

df_new = mean_PSNR.rename(index={'DCT1': 'DCT', 'DCT2': 'NS-F5', 'DCT3' : 'J-UNIWARD', 'DCT4' : 'UERD', 'DCT5' : 'PQ-UNIWARD'})
print(df_new)
df_new.plot.bar(title = 'Average PSNR of each method', xlabel = 'Methods', ylabel = 'Average PSNR (dB)')
# plt.yticks(np.arange(0, 60, 5))
# plt.xticks(rotation=45)
# plt.show()