# convert csv to influx write type
# format: <tableTname> filed1= filed2= ... timestamp
import os, csv, sys
lst=os.listdir("../btds") # get filename -> tablename in db


for f in lst:
	if f != '.DS_Store':
		print "Reading into " + f
		# create a txt file for each csv file
		txt = []
		with open('../btds/' + f, 'rb') as csvfile:
			reader = csv.DictReader((line.replace('\0','') for line in csvfile))
			headers = reader.fieldnames
			for row in reader:
				#parse throguh each row
				line = []
				line.append("allTables,") #filename -> tableName
				for header in headers[1:]: #skip timestamp and append at last
					# parse through each column
					if row[header] != '':
						#cell not null
						if str(row[header]).lstrip('-').replace('.','',1).isdigit():							
							content = str(row[header])
							line.append(str(header) + '=' + content)
						# elif '"' in row[header]:
						# 	content = str(row[header])
						# else:
						# 	#not numeric and not already wrapped in double quotes
						# 	content = '"'+str(row[header])+'"'
						# line.append(str(header) + '=' + content)
					else:
						#cell is null
						line.append(str(header) + '=' + '"NULL"')

					# print str(header) + '=' + str(row[header])
				line = line[0] + 'tableName=' + f[:-4] + ' ' + ','.join(line[1:])
				line += ' ' + str(row[headers[0]])
				txt.append(line)
		txt = '\n'.join(txt)
		if not os.path.exists('./output'): 
			os.makedirs('./output')
		file = open('./output/' + f[:-4] + '.txt', "w")
		file.write(txt)
		print "file saved at " + './output/' + f[:-4] + '.txt'
		file.close	
		
	



