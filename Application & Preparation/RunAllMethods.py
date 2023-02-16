


# import packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#read data
data = pd.read_csv('/media/tim/Backup Plus/Scriptie/methods/Github Labels/admin/labels/1c-DB.csv')

# initiate lists
DCT1, DCT2, DCT3, DCT4, DCT5 = [], [], [], [], []

# create commands
for name, row in data.iterrows():
    image_name=row.imageID[0:-4]
    path = f"/media/tim/Backup Plus/Scriptie/Methods/data/jpg/{row.phone}/{row.imageID}"
    png_path = f"/media/tim/Backup Plus/Scriptie/Methods/data/png/{row.phone}/{image_name}.png"
    dest_path = f'/media/tim/Backup Plus/Scriptie/Methods/stegDB/{row.phone}/{image_name}'
    png_dest_path = f'/media/tim/Backup Plus/Scriptie/Methods/stegDB/{row.phone}/{image_name}.png'
    secret_path = f'/media/tim/Backup Plus/Scriptie/Methods/Github Labels/code/2 - applying methods/messages/{row.message}'

    if row.method == 6:
        DCT1.append(f"python3 DCT_hide.py {png_path} {secret_path}")
    elif row.method ==7:
        DCT2.append(f"nsf5_simulation('{path}','{dest_path}.JPG',{row.embeddingRate},99)")
    elif row.method == 8:
        DCT3.append(f"run_j_uniward('{path}','{dest_path}.JPG',{row.embeddingRate})")
    elif row.method == 9:
        DCT4.append(f"uerd_run('{path}','{dest_path}.JPG',{row.embeddingRate})")
    elif row.method == 10:
        DCT5.append(f"PQ_UNIWARD_ccm('{path}', '/media/tim/Backup Plus/Scriptie/Methods/stegDB/Cover_PQ_UNIWARD/{row.phone}/{image_name}.JPG', '{dest_path}.JPG', '{row.embeddingRate}', 50)")


# store commands as one string
DCT1_commands = ""
for command in DCT1:
    DCT1_commands += ";"
    DCT1_commands += command

DCT2_commands = ""
for command in DCT2:
    DCT2_commands += ";"
    DCT2_commands += command

DCT3_commands = ""
for command in DCT3:
    DCT3_commands += ";"
    DCT3_commands += command

DCT4_commands = ""
for command in DCT4:
    DCT4_commands += ";"
    DCT4_commands += command

DCT5_commands = ""
for command in DCT5:
    DCT5_commands += ";"
    DCT5_commands += command

# write commands to text files
text_file = open("/media/tim/Backup Plus/Scriptie/Methods/stegDB/commands/DCT1.txt", "w")
text_file.write(DCT1_commands[1:])
text_file.close()

text_file = open("/media/tim/Backup Plus/Scriptie/Methods/stegDB/commands/DCT2.txt", "w")
text_file.write(DCT2_commands[1:])
text_file.close()

text_file = open("/media/tim/Backup Plus/Scriptie/Methods/stegDB/commands/DCT3.txt", "w")
text_file.write(DCT3_commands[1:])
text_file.close()

text_file = open("/media/tim/Backup Plus/Scriptie/Methods/stegDB/commands/DCT4.txt", "w")
text_file.write(DCT4_commands[1:])
text_file.close()

text_file = open("/media/tim/Backup Plus/Scriptie/Methods/stegDB/commands/DCT5.txt", "w")
text_file.write(DCT5_commands[1:])
text_file.close()
