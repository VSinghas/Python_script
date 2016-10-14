import numpy as np
import pandas as pd
import csv

def clean(string1):
    Scan_dtime = []
    for j in range(len(string1)):
        s0 = string1[j][13:36]
        Scan_dtime.append(s0)

    return(Scan_dtime)

def Create_date(list1):
    Scan_date = []
    for j in range(len(list1)):
        s0 = list1[j][:10]
        Scan_date.append(s0)

    return(Scan_date)

def Create_time(list1):
    Scan_time = []
    for j in range(len(list1)):
        s0 = list1[j][11:23]
        Scan_time.append(s0)

    return(Scan_time)


if __name__ == "__main__":
        # Reading of large csv files
        full_scan  = pd.read_csv("/disk1/vishwa_work/full_scan31.csv")

        # Improving the format of Datetime
        full_scan['s.sd'] = clean(full_scan['s.sd'])
        #print(full_scan)

        # Extracting the date values
        full_scan['date'] = Create_date(full_scan['s.sd'])

        # Extracting time values
        full_scan['time'] = Create_time(full_scan['s.sd'])

        # Dropping of datetime column
        full_scan.drop('s.sd', axis=1, inplace=True)

        # Saving the database in csv file
        full_scan.to_csv("scan31.csv")


