import pandas as pd
import ast
import csv

d1 = pd.read_csv('opinio1.csv')

ca = d1.cust_address
m_add = d1.merchant_address
olat = d1.order_delivered_lat
olong = d1.order_delivered_long
print len(ca)

output = open('v1_1.csv', 'wb')
writer = csv.writer(output)
writer.writerow(['wbn', 'add', 'pin', 'city', 'lat', 'long'])

for i in xrange(len(ca)):
    try:
        ca_dict = ast.literal_eval(ca[i])
        if type(ca_dict) is not dict:
            print "NOT A DICTIONARY"
            continue
        else:
            if (ca_dict["city"].lower() == "delhi ncr" and "gurgaon" in m_add[i].lower()):
                city_identified = "Gurgaon"
                print "GURGAON IN NCR ", city_identified
	        if ca_dict["city"].lower() == "gurgaon":
	            print "ORIGINAL GURGAON"
	            if ca_dict["city"].lower() not in ca_dict["address"].lower():
	                city_identified = ca_dict["city"]
	                print "city identified is gurgaon"
	            else:
	                city_identified = ""
	                print "city identified is null"
	        if (ca_dict["city"].lower() == "gurgaon") or (city_identified.lower() == "gurgaon"):
	        	print "EVEN DEEPER"
                if ca_dict["locality"] and ca_dict["locality"].lower() not in ca_dict["address"].lower():
                    locality_identified = ca_dict["locality"]
                else:
                    locality_identified = ""
                address = ca_dict["address"] + ", " + \
                    locality_identified + ", " + city_identified
                print address
                writer.writerow([i + 1, address, 122002, city_identified.lower()
                                 if city_identified is not "" else ca_dict["city"].lower(), olat[i], olong[i]])
    except ValueError:
        pass

output.close()
