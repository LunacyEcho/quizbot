#!/usr/bin/env python3

import json
import csv

# Opening JSON file and loading the data
# into the variable data
with open('tus_dickens.json') as json_file:
    data = json.load(json_file)
  
question_data = data['tossups']
  
# now we will open a file for writing
data_file = open('tus_dickens.csv', 'w')
  
# create the csv writer object
csv_writer = csv.writer(data_file)
  
# Counter variable used for writing 
# headers to the CSV file
count = 0
  
for q in question_data:
    if count == 0:
  
        # Writing headers of CSV file
        header = q.keys()
        csv_writer.writerow(header)
        count += 1
  
    # Writing data of CSV file
    csv_writer.writerow(q.values())
  
data_file.close()