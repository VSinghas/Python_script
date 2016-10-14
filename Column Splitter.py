import pandas as pd
import numpy as np

df = pd.read_csv('/disk1/kdp_block_latlon.csv')
df.reset_index(level=0, inplace=True)
df = df.rename(columns = {'index':'id','Unnamed: 0':'lat_lon','lat-lon':'Count'})
df.drop('id', axis=1, inplace=True);df

df['lat'], df['lon'] = zip(*df['lat_lon'].map(lambda x: x.split(',')))
df.lat = df.lat.astype(float);df.lon = df.lon.astype(float)
df.to_csv("/disk1/latlong_load.csv")
