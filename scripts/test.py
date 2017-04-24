import csv

aFile = open("../data/currentSearch.csv", "r")
csvReader = csv.reader(aFile, delimiter=",")
topic = ""
for row in csvReader:
    topic = row
print(topic[0])