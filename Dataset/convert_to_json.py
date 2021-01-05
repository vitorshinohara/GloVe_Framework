import csv, json, sys, re

csvFilePath = 'dirty data wireless headphones.csv'
jsonFilePath = 'dirty data wireless headphones.json'
maxInt = sys.maxsize
data = {}


with open(csvFilePath, 'r') as csvFile:
    csvReader = csv.DictReader(csvFile)

    for row in csvReader:
	try:
          for key, value in row.items():
              data[key] = re.sub(r'[^\w\s]','',value)
              data[key] = data[key].replace('"', '')
        

          with open(jsonFilePath, 'a') as jsonFile:
              jsonFile.write(json.dumps(data))
              jsonFile.write('\n')
        
          data = {}
        except Exception as e: 
          print(e)
          continue
        
