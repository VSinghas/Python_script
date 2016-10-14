import pandas as pd
import csv
import cPickle as pickle
d1 = pd.read_csv('v1_1.csv')
lats = d1.lat
longs = d1.long

d2 = pd.read_csv('output.csv')
localities = d2.locality

locality_id_map = {}
id = 1

lat_long_dict = {}
for i in xrange(len(localities)):
	if localities[i] not in locality_id_map:
		locality_id_map[localities[i]] = id
		id += 1
	if locality_id_map[localities[i]] not in lat_long_dict:
		lat_long_dict[locality_id_map[localities[i]]] = [(lats[i], longs[i])]
	else:
		lat_long_dict[locality_id_map[localities[i]]].append((lats[i], longs[i]))

locality_list = [{'locality_id': locality, 'LatLng': LatLng} for locality, LatLng in lat_long_dict.items()]

with open('locality_list.pickle', 'wb') as f:
	pickle.dump(locality_list, f)

with open('locality_id_map.pickle', 'wb') as f:
	pickle.dump(locality_id_map, f)
