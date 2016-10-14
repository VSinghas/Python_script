# Calling-in dplyr package
library(dplyr)
library(data.table)
library(chron)
library(ggplot2)

# Reading of large CSV files
full_s1 <- fread("/disk1/vishwa_work/scan_c31.csv", header = T, sep = ',')

# Calculating the scanning frequency with time 
scan_count<-as.data.frame(table(full_s1$time))

# Aggregating frequency of scans in certain time interval
scan_count$scan.intvl<-trunc(times(scan_count$Var1),times("01:00:00"))
scan_rate<-ddply(scan_count,.(scan.intvl),summarise,sum=sum(Freq))

scan_rate$scan.intvl<-chron(times=scan_rate$scan.intvl)

# Write CSV in R
write.csv(scan_rate, file = "/disk1/vishwa_work/Scan_rt31.csv")

#########################################################

###################################
# Calculating the scanning frequency with time 
scan_count<-as.data.frame(table(full_s1$time))
#View(scan_count)

# Adding the date column in the dataframe
scan_count$Var1 = substr(scan_count$Var1,14,37)
scan_count$dt<-as.POSIXct(scan_count$Var1, "%Y-%m-%d")

# Function used to extract time from string
substrRight <- function(x, n){
  substr(x, nchar(x)-n+1, nchar(x))
}

# Extracting the time data from the string
scan_count$time<-substrRight(scan_count$Var1, 13)
scan_count$time<-substring(scan_count$time,1,12)

# Filtering of scans based on specific date
scan_count<-filter(scan_count,dt=="2016-07-01")

# Aggregating frequency of scans in certain time interval
scan_count$scan.intvl<-trunc(times(scan_count$time),times("00:15:00"))
scan_rate<-ddply(scan_count,.(scan.intvl),summarise,sum=sum(Freq))

# Converting the string into time format
#scan_count$time<-chron(times=scan_count$time)
scan_rate$scan.intvl<-chron(times=scan_rate$scan.intvl)

# Write CSV in R
write.csv(scan_rate, file = "/disk1/vishwa_work/Scan_rate.csv")

# Plotting of scan rate
#ggplot(data=scan_count, aes(x=scan_count$time, y=scan_count$Freq, xlab="Scan time ", ylab="No of Scans ",group=1))+ geom_line()

