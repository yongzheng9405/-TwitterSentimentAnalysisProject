import csv

def output():
    aFile = open("evaluate.csv", "w", newline="")
    csvWriter = csv.writer(aFile)
    csvWriter.writerows(readFile())
    aFile.close()


def readFile():
    aFile = open("trump.csv", "r", encoding="ISO-8859-1")

    lines = []

    csvReader = csv.reader(aFile, delimiter=",")

    for row in csvReader:
        if (row[6] != "" and "USA" in row[6]):
            lines.append([row[3], process(row[6]), row[8]])
    return lines

def process(location):
    if ("AL" in location):
        return "AL"
    elif ("AK" in location):
        return "AK"
    elif ("AZ" in location):
        return "AZ"
    elif ("AR" in location):
        return "AR"
    elif ("CA" in location):
        return "CA"
    elif ("CO" in location):
        return "CO"
    elif ("CT" in location):
        return "CT"
    elif ("DE" in location):
        return "DE"
    elif ("FL" in location):
        return "FL"
    elif ("GA" in location):
        return "GA"
    elif ("HI" in location):
        return "HI"
    elif ("ID" in location):
        return "ID"
    elif ("IL" in location):
        return "IL"
    elif ("IN" in location):
        return "IN"
    elif ("IA" in location):
        return "IA"
    elif ("KS" in location):
        return "KS"
    elif ("KY" in location):
        return "KY"
    elif ("LA" in location):
        return "LA"
    elif ("ME" in location):
        return "ME"
    elif ("MD" in location):
        return "MD"
    elif ("MA" in location):
        return "MA"
    elif ("MI" in location):
        return "MI"
    elif ("MN" in location):
        return "MN"
    elif ("MS" in location):
        return "MS"
    elif ("MO" in location):
        return "MO"
    elif ("MT" in location):
        return "MT"
    elif ("NE" in location):
        return "NE"
    elif ("NV" in location):
        return "NV"
    elif ("NH" in location):
        return "NH"
    elif ("NJ" in location):
        return "NJ"
    elif ("NM" in location):
        return "NM"
    elif ("NY" in location):
        return "NY"
    elif ("NC" in location):
        return "NC"
    elif ("ND" in location):
        return "ND"
    elif ("OH" in location):
        return "OH"
    elif ("OK" in location):
        return "OK"
    elif ("OR" in location):
        return "OR"
    elif ("PA" in location):
        return "PA"
    elif ("RI" in location):
        return "RI"
    elif ("SC" in location):
        return "SC"
    elif ("SD" in location):
        return "SD"
    elif ("TN" in location):
        return "TN"
    elif ("TX" in location):
        return "TX"
    elif ("UT" in location):
        return "UT"
    elif ("VT" in location):
        return "VT"
    elif ("VA" in location):
        return "VA"
    elif ("WA" in location):
        return "WA"
    elif ("WV" in location):
        return "WV"
    elif ("WI" in location):
        return "WI"
    elif ("WY" in location):
        return "WY"


def main():
    output()

if __name__ == '__main__':
    main()

