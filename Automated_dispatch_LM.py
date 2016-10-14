import os
import time
from datetime import datetime, timedelta
from subprocess import run
import sys
from bson.objectid import ObjectId

#here seven_days_before variable is three months before
today = datetime.today()
day_before = datetime.today() - timedelta(30)
# path of the output file 
file_path = "/disk1/vishwa_work/dispatch_LM.json"
dispatch_type = 'lastmile'
pass_w = 'x[td7R%;,'

old_id = ObjectId.from_datetime(day_before)
recent_id = ObjectId.from_datetime(today)

#applying filters of status in query itself
query = "mongoexport --host 172.0.8.35 --db delhivery_db -c dispatch --query '{_id:{$lt: ObjectId(\"%s\"), $gt:ObjectId(\"%s\")}, t:\"%s\"}' --out %s -u ro_express -p '%s'" % (recent_id, old_id, dispatch_type, file_path, pass_w)
print query
#os.system(query)
run(query).stdout
