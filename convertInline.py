# convert csv to influx write type
# format: <tableTname> filed1= filed2= ... timestamp
import os, csv
lst=os.listdir("./btds") # get filename -> tablename in db


for f in lst:
	# create a txt file for each csv file
	txt = []
	with open('./btds/' + f, 'rU') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			#parse throguh each row
			line = []
			line.append(f[:-4]) #filename -> tableName
			for key in row.keys()[1:]: #skip timestamp and append at last
				# parse through each column
				line.append(str(key) + '=' + str(row[key]))
			line = ','.join(line)
			line += ' ' + str(row[row.keys()[0]])
			txt.append(line)

	txt = '\n'.join(txt)

	print txt	
	



