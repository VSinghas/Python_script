import os
import time
from datetime import date, timedelta
from subprocess import run
import sys
sys.path.append('/disk1/vishwa_work')
from constant import mongo_ip

#here seven_days_before variable is three months before
today = date.today()
seven_day_before = date.today() - timedelta(40)

print today, seven_day_before
file_path = "/data1/delhivery/ad_hoc_analysis/EOD47_Analysis/monthly_data.csv"

pass_w = 'x[td7R%;,'
pattern = '%d/%m/%Y %H:%M:%S'

#ist_diff = '01/01/1970 05:30:01'
#ist_diff =  int(time.mktime(time.strptime(ist_diff, pattern)))
old_date = '%s/%s/%s 00:00:00' % (seven_day_before.day, seven_day_before.month,seven_day_before.year)
old_date = int(time.mktime(time.strptime(old_date, pattern)))
#old_date -= ist_diff
old_date *= 1000
recent_date = '%s/%s/%s 20:30:01' % (today.day, today.month,today.year)
recent_date = int(time.mktime(time.strptime(recent_date, pattern)))
#recent_date -= ist_diff
recent_date *= 1000

print old_date, recent_date

#applying filters of status in query itself

query = "sudo mongoexport --host %s --db delhivery_db -c packages --type=csv --fields wbn,pd,oc,occ,cn,cnc,pin,pt,cl,cs.st,cs.ss,date.frd,nsl --query '{pd:{$lt: new Date(%s), $gt:new Date(%s)}}' --out %s -u ro_express -p '%s'" % (mongo_ip,recent_date, old_date, file_path, pass_w)
print query
#os.system(query)
run(query).stdout


