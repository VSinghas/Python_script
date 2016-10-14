import pandas as pd
import numpy as np


def sum_rec(list1, list2, list3):
    #############################################################
    #@ Function will estimate the sum of product of first jth and 
    #  n-jth value in the list
    # --------------------------------------------
    # Input  : list1,list2,list3:- lists of nth size, array-type
    # Output : N:- float type
    #############################################################   
    n = len(list1)                          
    j = 0                                           
    N = list1[0]*list2[n-1]             # initialize the sum
    while j < n-1:
        if len(list1)==1:
            return N
        elif len(list1)>1:
            if (list2[n-2-j]-((j+1)*list3[n-2-j]))>0:
                return(N + list1[j+1]*(list2[n-2-j]-((j+1)*list3[n-2-j])))
            j+=1           
    return N                              


def elemt_wise(list1, list2, list3):
    #############################################################
    #@ Function will call the two list whose size are
    # reducing recurisively and storing output in list
    # --------------------------------------------
    # Input  : list1,list2 & list3:- lists of nth size, array-type
    # Output : Scan_cnt:-list-type 
    #############################################################
    Scan_cnt = []                       # creates an empty array
    n = len(list1)                      
    for i in range(n):
        Sum = sum_rec(list1[:n-i], list2[:n-i], list3[:n-i])
        Scan_cnt.append(Sum)            
    Scan_cnt.reverse()                  # reversing the list   
    return Scan_cnt                     


def per_count(df):
    #############################################################
    #@ Function will estimate total counts at specific hrs
    # at certain facility
    # ----------------------------------------------
    # Input : df :-dataframe.type, n = int.type
    # Output : df_cn :- dataframe.type
    #############################################################
    df_to = pd.Timestamp('2016-06-01 00:00:00.000')                    
                                        # starting datetime
    df['sd'] = [pd.Timestamp(df['sd'][i]) for i in range(len(df['sd']))]
                                        # convert the datetime string to datetime
    df['Diff'] = (df.sd-df_to).astype('timedelta64[h]')                
                                        # estimate the difference between starting
                                        # & scan datetime & storing in column
    #print(df)
    df_cn = pd.DataFrame({"Freq":df['Diff'].value_counts(          
                sort=False, ascending=True)})
                                        # estimate the counts of value in the
                                        # specific column
    df_cn = df_cn.reindex(np.arange(96), fill_value= 0)
                                        # fill the missing index with 0 value
    #print(df_cn)   
    return df_cn


def inbound_cn(df):
    #############################################################
    #@ Function will estimate the number shipments inbounded at 
    # certain time interval
    # -------------------------------------------------
    # Input : df :-dataframe.type
    # Output : inship_cn: dataframe.type
    #############################################################
    full_sn = df.drop_duplicates(subset='wbn', keep='first')         
                                        # inbound shipments by waybill_no
    full_sn.reset_index(drop=True, inplace=True)                       
                                        # reset the index of the dataframe
    #print '{full_sn}:\n', full_sn      # prints the dataframe
    inship_cn = per_count(full_sn)      
                                        # counts inbound shipments
    return inship_cn


def outbound_cn(df):
    #############################################################
    #@ Function will estimate the number shipments outbounded at 
    # certain time interval
    # -------------------------------------------------
    #Input : df :-dataframe.type
    # Output : outship_cn: dataframe.type    
    #############################################################
    full_sn = df.drop_duplicates(subset='wbn', keep='last')
    full_sn = full_sn[(full_sn.ss == "Delivered") | (full_sn.ss == "In Transit")]
                                        # outbound shipments by wbn
    #full_sn = full_sn[full_sn.act.notnull()]
    full_sn.reset_index(drop=True, inplace=True)                       
                                        # reset the index of the dataframe
    #print '{full_sn}:\n', full_sn      # prints the dataframe
    outship_cn = per_count(full_sn)
                                        # counts outbound shipments
    return outship_cn

        
if __name__ == "__main__":
    Center = pd.read_csv("/disk1/vishwa_work/Pjt2/facility.csv")
    # Importing the hdf format file
    all_scan = pd.HDFStore('/disk1/hdf_data/june_16_scans.h5')
        
    for centre in Center['HQ_Name']:
        try:
            scan = all_scan.select(centre)
            in_path = '/disk1/vishwa_work/Pjt2/Facility/%s_means.csv' % centre
            scan_mean = pd.read_csv(in_path)
            
            scan_mean = scan_mean[:96]
                                        # selecting 4-days scan mean
            scan.sort_values(by='sd',ascending=True, inplace=True)             
                                        # sort by scan datetime  
            scan.reset_index(drop=True, inplace=True)
                                        # reset the index of the dataframe
            in_ship = inbound_cn(scan); out_ship = outbound_cn(scan)
                                        # no of shipments inbounded & outbounded
            actual_scan = per_count(scan)
                                        # actual no of scans at any facility
            in_ship['Scan_count'] = elemt_wise(scan_mean['mean'],in_ship['Freq'],out_ship['Freq'])
                                        # store the list in dataframe
            #Exptd_outpath = '/disk1/vishwa_work/Pjt2/data2/exptd_%s.csv' % centre
            #Actual_outpath = '/disk1/vishwa_work/Pjt2/data2/actual_%s.csv' % centre
            #in_ship.to_csv(Exptd_outpath)
            #actual_scan.to_csv(Actual_outpath)
                                        # writing the output dataframes in the csv file
            print '{expected scan count}:\n',len(in_ship); print '{actual scan count}:\n', len(actual_scan)
                                        # prints the dataframe
        except (KeyError, IOError):
            pass
        

