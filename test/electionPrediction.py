import json
from pprint import pprint
import csv

def load():
    with open('trump.json') as aFile:
        data = json.load(aFile)

        output(process(data))


def process(data):
    aList = []

    for i in range(len(data)):
        aList.append([data[i]['sentiment_fake'] <= 0, data[i]['state']])
    return aList

def output(aList):
    aFile = open("electionPrediction.csv", "w", newline="")
    csvWriter = csv.writer(aFile)
    csvWriter.writerows(aList)
    aFile.close()


def main():
    load()

if __name__ == '__main__':
    main()