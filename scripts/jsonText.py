import csv
import json



def read_csv(file):
    csv_rows = []
    with open(file) as csvfile:
        reader = csv.DictReader(csvfile)
        title = reader.fieldnames
        for row in reader:
            csv_rows.extend([{title[i]: row[title[i]] for i in range(len(title))}])
        return csv_rows



def write_json(data, json_file, format=None):
    with open(json_file, "w") as f:
        if format == "good":
            f.write(json.dumps(data, sort_keys=False, indent=4, separators=(',', ': '), encoding="utf-8",
                               ensure_ascii=False))
        else:
            f.write(json.dumps(data))


write_json(read_csv('statedata.csv'), 'student.json', 'good')