import pandas as pd
import numpy as np

df = pd.read_csv("/disk1/vishwa_work/Pjt3/dispatch_loc.csv");df

df_a = df.groupby(['dwbn','lat-lon']).agg({'Count':'sum'});df_a

dwbn = df.groupby(['dwbn']).agg({'Count':'sum'});dwbn
pct = df_a.div(dwbn, level='dwbn') * 100
print(pct)
#pct.to_csv('/disk1/pct_loc.csv')

reset_pct = pct.unstack('lat-lon')
new_dd = reset_pct.sort_index(axis=1)
print(new_dd)
new_dd.to_csv("/disk1/dispatch_pct.csv")
