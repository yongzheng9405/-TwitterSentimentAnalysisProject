#!/usr/bin/env

import sys, json, csv

# try:
#     data = json.loads(sys.argv[1])
# except:
#     print "ERROR"
#     sys.exit(1)

print sys.argv[1]

# print json.dumps(result)

with open('../data/currentSearch.csv', 'wb') as csvFile:
    csvWriter = csv.writer(csvFile)
    csvWriter.writerow(["topics"])
    csvWriter.writerow([sys.argv[1]])