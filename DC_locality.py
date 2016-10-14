import pandas as pd
import numpy as np

def format2decmal(myList):
    return [ '%.2f' % elem for elem in myList ]

def latlong(df):
    poly = []
    for j in xrange(len(df)):
        lat_lon = df.lat[j] + "," + df.lon[j]
        poly.append(lat_lon)
    return poly

if __name__ == "__main__":
    # Package dataset for the month of August
    df = pd.read_csv("/disk1/vishwa_work/Pjt3/Kadipur_DC_loc.csv")
    
    df=df.rename(columns = {'s_sl':'sl','s_ss':'ss','s_st':'st','aseg.pin':'pin','aseg.loc':'loc','aseg.lon':'lon',
                        's_dwbn':'dwbn', 'aseg.lat':'lat','wbn':'Waybill'})
                                    # rename the columns name
        
    # Dispatch dataset from 10th Aug to 31st Aug     
    d_df = pd.read_csv("/disk1/vishwa_work/Pjt3/dispatch_kdp.csv")
    
    d_kdp = d_df[d_df.cn == "Gurgaon_Kadipur (Haryana)"]
                                    # filtering the origin center
    d_kdp.reset_index(drop=True, inplace=True)
                                    # reset the index 
    new_df = pd.merge(df, d_kdp, on='dwbn', how = 'inner')
                                    # merge two dataframe based on dwbn
    new_df.dropna(subset = ['pin'],inplace=True)#;print(len(new_df))
                                    # drop the NaN values in the pin column
    new_df = new_df[new_df['pin'].str.contains("122")]#;print(type(new_df['lat'][0]))
                                    #filtering only Gurgaon locality
    new_df['lon'] = format2decmal(new_df['lon'])
    new_df['lat'] = format2decmal(new_df['lat'])
                                    # Block-wise locality distribution
    df_block = pd.DataFrame({'dwbn':new_df['dwbn'], 'lat':new_df['lat'], 'lon':new_df['lon']})
                                    # new dataframe
    df_block.reset_index(drop=True, inplace=True)
                                    # reset the index 
    df_block['lat-lon'] = latlong(df_block)
    #print(df_block)
    
    #new_df.to_csv("/disk1/dispatch_kadipur.csv")
    dc_loc = pd.DataFrame({'Count':df_block.groupby(by=['dwbn','lat-lon'])['dwbn'].count()})
    print(dc_loc)
    dc_loc.to_csv("/disk1/dispatch_loc.csv")


    #a = new_df['fu.emp_id'].value_counts(dropna=False)
    #print(len(a))
