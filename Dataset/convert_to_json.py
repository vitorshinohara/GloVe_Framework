import csv, json, sys, re

csvFilePath = 'dirty data high res audio player.csv'
jsonFilePath = 'dirty data high res audio player.json'
maxInt = sys.maxsize
data = {}

while True:
    # decrease the maxInt value by factor 10 
    # as long as the OverflowError occurs.

    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt/10)

with open(csvFilePath, 'r', encoding='utf-8') as csvFile:
    csvReader = csv.DictReader(csvFile)

    for row in csvReader:
        for key, value in row.items():
            data[key] = re.sub(r'[^\w\s]','',value)
        

        with open(jsonFilePath, 'a', encoding='utf-8') as jsonFile:
            jsonFile.write(json.dumps(data))
            jsonFile.write('\n')
        
        data = {}
        