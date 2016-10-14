import numpy as np
import pandas as pd
import csv

if __name__ == "__main__":
        # Reading of large csv files
        full_scan1 = pd.read_csv("/disk1/vishwa_work/scan30.csv",names=['id','wbn','dt','time'])
        full_scan1.drop('id',axis=1, inplace=True)
        full_scan1 = full_scan1[1:]
        full_scan1.reset_index(drop=True, inplace=True)

        full_scan2 = pd.read_csv("/disk1/vishwa_work/scan31.csv",names=['id','wbn','dt','time'])
        full_scan2.drop('id',axis=1, inplace=True)
        full_scan2 = full_scan2[1:]
        full_scan2.reset_index(drop=True, inplace=True)

        # Merging two dataframe row-wise
        full_scan = pd.DataFrame(full_scan1.append(full_scan2, ignore_index=True), columns=['wbn','dt', 'time'])
        #print(full_scan)
        full_sn = pd.DataFrame.drop_duplicates(full_scan)
        full_sn.reset_index(drop=True, inplace=True)

        # writing the new dataframe in csv file
        full_sn.to_csv("scan_aug.csv")


