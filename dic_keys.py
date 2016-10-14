import json
from pprint import pprint


#for storing all 1st level keys
all_keys = {}
def compute_keys(d):
   all_keys = {}
   for j,obj in d.items():
       for key in obj:
           if key not in all_keys:
               x = str(type(obj[key]))
               y = '_type'
               x = x + y
               all_keys.setdefault(x,[]).append(key)
   for i in all_keys:
       all_keys[i] = set(all_keys[i])
   return all_keys

#Reading file
with open('/disk1/vishwa_work/test2.json',"r") as f:
   dat1 = {}
   j = 0
   for line in f:
       dat = json.loads(line)
       dat1[j]=dat
       j+=1

result = {}
result = compute_keys(dat1)
#pprint(result)

#2nd level keys for list type
level2 = []
for j in range(1000):
   for i in range(len(dat1[j]["ist"])-1):
       for k,v in dat1[j]["ist"][i].items():
           level2.append(k)
lev = set(level2)
print(lev)

