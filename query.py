#!/usr/bin/python
import subprocess, os, sys, re, datetime, iso8601
from influxdb import InfluxDBClient


def create():
	client = InfluxDBClient('localhost', 8086, 'root', 'root')
	currdb = [x['name'] for x in client.get_list_database()]
	print "Your current databases are: "
	print ", ".join(str(x) for x in currdb)	
	dbName = raw_input("Enter db name: ")
	client.create_database(dbName)
	print "Database " + dbName + " created"
	oneOrMultiple = raw_input("Create one table: 1, Create multiple tables: 2: ")
	if oneOrMultiple == "1":		
		createOne(dbName)
	else:
		createMultiple(dbName)

def createOne(dbName):	
	importPath = pathExist()
	writeDb(importPath, client, 1, dbName)

def createMultiple(dbName):
	importPath = pathExist()
	writeDb(importPath, client, 2, dbName)


def writeDb(importPath, client, singleOrBatch, dbName):
	# sample post request
	# curl -i -XPOST 'http://localhost:8086/write?db=mydb' --data-binary @cpu_data.txt
	if singleOrBatch == 1:
		# dbName = importPath.split('/')[-1][:-4] #segment the path and grab the filename
		# print "The db name is: " + dbName
		importData(dbName, importPath)
	else:
		# batch import. import files in dir 
		if importPath[-1] != '/':
			importPath += '/'
		fileList = os.listdir(importPath)
		for f in fileList:
			if '.txt' in f:
				importData(dbName, importPath + f)
				print "Table " + f[:-4] + " imported"


def importData(dbName, importPath):
	url = "http://localhost:8086/write?db=" + str(dbName) + "&precision=ms"
	queryStr = "curl -i -XPOST " + "'%s'" % url + "  --data-binary @" + importPath
	subprocess.call(queryStr, shell=True)

def pathExist():
	print "================== Writing Data ==================="
	importPath = raw_input("Enter full path to your import file: ")
	if not os.path.exists(str(importPath)):
		print "File path doesn't exist"
		pathRetype = raw_input("Retry: 1, Exit: 2: ")
		if pathRetype == 1:
			pathExist()
		else:
			sys.exit()
	else:
		return importPath

def query():
	# aggregation every four minutes 	
	client = InfluxDBClient('localhost', 8086, 'root', 'root')
	currdb = [x['name'] for x in client.get_list_database()]
	print "Your current databases are: "
	print ", ".join(str(x) for x in currdb)	
	queryDb = raw_input("Enter the database that you're querying from: ")
	client = InfluxDBClient('localhost', 8086, 'root', 'root', queryDb)

	#get the time range
	minTime = client.query('SELECT TEMP FROM /.*/ LIMIT 1')
	minTime = minTime.raw['series'][0]['values'][0][0]

	maxTime = client.query('SELECT TEMP FROM /.*/ ORDER BY time DESC LIMIT 1')
	maxTime = maxTime.raw['series'][0]['values'][0][0]
	print "Time range of the entire db: " + minTime + ' - ' + maxTime

	# collection of the mininum results in the 4mins windows
	mins = []
	currTime = minTime
	iterator = 1
	while iso8601.parse_date(currTime) < iso8601.parse_date(maxTime):
		# upper bound for the 4mins window
		upperBound = iso8601.parse_date(currTime) + datetime.timedelta(minutes=4)
		if upperBound > iso8601.parse_date(maxTime):
			upperBound = iso8601.parse_date(maxTime)
		upperBound = str(upperBound).replace(' ', 'T')
		print '==============' + ' Window ' + str(iterator) + ' ' + '=============='
		print "Parsing time window: " + currTime + ' - ' + str(upperBound)
		# query MIN only when there are more than one time stamp in the 4mins window
		countQuerymsg = "SELECT COUNT(TEMP) FROM /.*/ WHERE time >= " + "'" + currTime + "'" + ' AND time <= ' + "'" + upperBound + "'" 
		count = client.query(countQuerymsg)


		if count.raw == {}:
			print "No timestamp in range"
			currMin = 0
		else:
			count = count.raw['series'][0]['values'][0][1]
			print "Num of timestamps: " + str(count)

			if count > 1:
				print "More than 1 timestamp in this window"
				querymsg = 'SELECT MIN(TEMP) FROM /.*/ WHERE time >= ' + "'" + currTime + "'" + ' AND time<= ' + "'" + upperBound + "'"  
				currMin = client.query(querymsg)
				currMin = currMin.raw['series'][0]['values'][0][1]
				print "curr min is: " + str(currMin)
			elif count <= 1:
				currMin = 0

		mins.append(currMin)
		currTime = upperBound
		iterator += 1

	print mins
	print "Num of time windows parsed: " + str(iterator)
	
if __name__ == "__main__":
	# ================ Connecting to db ===========================
	print "Are you creating a database or querying?"
	writeOrQuery = raw_input("Creating: 1, Quering: 2: ")
	if writeOrQuery == "1":
		create()
	else:
		query()




















