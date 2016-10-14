import json
import pandas as pd
import numpy as np

df  = pd.read_csv("/disk1/vishwa_work/Pjt1/waybills.csv")
df1 = []
print(type(df['updated_data'][0]))
for j in range(len(df['updated_data'])):
    updated_df = json.loads(df['updated_data'][j].read())
    df1.append(updated_df)

#print(type(json.loads(df['updated_data'][0])))
#print(len(updated_df))
df2 =[]
for row in df1:
    data1 = pd.DataFrame.from_dict(row)
    df2.append(data1)

df3 = pd.concat(df2, ignore_index = True)
print(df3)
#df2.to_csv("/disk1/vishwa_work/Pjt1/uptd.csv")



#pd.DataFrame.from_dict(
#data1 = pd.DataFrame(updated_df.items())
#data1.to_csv("/disk1/vishwa_work/Pjt1/updated_data.csv")


