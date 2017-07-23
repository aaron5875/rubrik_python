#!/usr/bin/env python
# This script comes with no warranty use at your own risk

# usage examples:
# python restore_report.py -n rubrik_node_ip_address
# python restore_report.py -n rubrik_node_ip_address -afterDate June+20+2017 -beforeDate June+26+2017
# python restore_report.py -n rubrik_node_ip_address -beforeDate June+26+2017
# python restore_report.py -n rubrik_node_ip_address -afterDate June+26+2017

import sys,os,json,requests,getopt
import base64
import getpass
import csv
from time import gmtime, strftime

requests.packages.urllib3.disable_warnings()

beforeDate = ""
afterDate = ""

myopts, args=getopt.getopt(sys.argv[1:],"n:b:a:")

for o, a in myopts:
    if o == '-n':
        node=a
    elif o == '-b':
        beforeDate=a
    elif o == '-a':
	afterDate=a
    else:
        sys.exit("Unsupported Variable, Program exiting ...")


#rk_ver = rubrik_common_v1.get_rubrik_version(node)

#print(rk_ver) 

userId = raw_input("Enter Rubrik Login:")
password = getpass.getpass("Password for " + userId + ":")
#secrets_json_path = './secrets.json'

#with open(secrets_json_path) as data:
#	secret_data = json.load(data)
#	userId = secret_data['userId']
#	password = base64.b64decode(secret_data['password'])
rk_auth = "Basic " + base64.b64encode(userId + ":" + password)



try:
	if beforeDate != "" and afterDate != "":
        	url='https://' + node + '/api/internal/event?limit=5000&after_date='+ afterDate +'&before_date=' + beforeDate + '&event_type=Recovery'
	elif beforeDate == "" and afterDate != "":
        	url='https://' + node + '/api/internal/event?limit=5000&after_date='+ afterDate + '&event_type=Recovery'
	elif beforeDate != "" and afterDate == "":
        	url='https://' + node + '/api/internal/event?limit=5000&before_date='+ beforeDate + '&event_type=Recovery'
	else:
	       	url='https://' + node + '/api/internal/event?limit=1000&event_type=Recovery'	        
	response=requests.get(url, verify=False, headers= {'Content-Type':'application/json', 'Accept':'application/json', 'Authorization':rk_auth}, timeout=360)
	print response.status_code		
	data = response.json()		
	restore_events = []
	time = strftime("%Y%m%d_%H%M%S", gmtime())
	for event in data['data']:
		restore_events.append(event)	
       	restore_report = open('restore_report_' + time + '.csv','w')
	csvwriter = csv.writer(restore_report)
	count = 0
	for event in restore_events: 
		if count ==0:
			header = event.keys()
			csvwriter.writerow(header)
			count += 1
		csvwriter.writerow(event.values())
	restore_report.close()
	print "Created restore_report_" + time + ".csv"
	
except:
	sys.exit("Unsupported Rubrik Code Level for this script, Program Exiting ...")

