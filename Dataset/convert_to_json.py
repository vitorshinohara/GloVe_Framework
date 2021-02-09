import csv, json, sys, re

csvFilePath = 'dirty data high res audio player.csv'
jsonFilePath = 'dirty data high res audio player.json'
data = {}


#maxInt = sys.maxsize
#while True:
#    # decrease the maxInt value by factor 10 
#    # as long as the OverflowError occurs.
#
#    try:
#        csv.field_size_limit(maxInt)
#        break
#    except OverflowError:
#        maxInt = int(maxInt/10)
		
with open(csvFilePath, 'r', encoding='utf-8') as csvFile:
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
			
