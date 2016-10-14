import csv
import json
import sys

input_file = csv.DictReader(open("/disk1/vishwa_work/Pjt3/data2/sep_scan1-30.csv"))
output_file = csv.writer(open("/disk1/vishwa_work/Pjt3/data2/sep_sn1-30_break.csv", "wb+"))
output_file.writerow(["s_sl","aseg.loc","aseg.lon","aseg.lat"])
csv.field_size_limit(sys.maxsize)
i=0
for row in input_file:
    if row.get("s",None):
        for scan in json.loads(row.get("s",None)):
            try:
                output_file.writerow([scan.get("sl",""),row.get("aseg.loc",""),row.get("aseg.lon",""),row.get("aseg.lat","")])
            except Exception,e:
                i=i+1
    else:
        i=i+1
        pass
print i


