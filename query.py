#!/usr/bin/python
import subprocess, os, sys, re
from influxdb import InfluxDBClient

client = InfluxDBClient('localhost', 8086, 'root', 'root')

def create():
	currdb = [x['name'] for x in client.get_list_database()]
	print "Your current tables are: "
	print ", ".join(str(x) for x in currdb)
	
	oneOrMultiple = raw_input("Create one table: 1, Create multiple tables: 2: ")
	if oneOrMultiple == "1":		
		createOne()
	else:
		createMultiple()

def createOne():	
	importPath = pathExist()
	writeDb(importPath, client, 1)

def createMultiple():
	importPath = pathExist()
	writeDb(importPath, client, 2)


def writeDb(importPath, client, singleOrBatch):
	# sample post request
	# curl -i -XPOST 'http://localhost:8086/write?db=mydb' --data-binary @cpu_data.txt
	if singleOrBatch == 1:
		print "import path is: " + importPath
		dbName = importPath.split('/')[-1][:-4] #segment the path and grab the filename
		print "The db name is: " + dbName
		client.create_database(dbName)
		print "Database " + dbName + " created"
		importData(dbName, importPath)
	else:
		# batch import. import files in dir 
		if importPath[-1] != '/':
			importPath += '/'
		fileList = []
		for fFileObj in os.walk(importPath): 
			fileList = fFileObj[2]
			break
		for f in fileList:
			if f != '.Dstore':
				client.create_database(f)
				print "Database " + f + "created"
				importData(f, importPath + f)


def importData(dbName, importPath):
	url = "http://localhost:8086/write?db=" + str(dbName)
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
	return None



# result = client.query('SELECT TEMP FROM /.*/ LIMIT 1')
# print result.raw['series'][0]['values'][0][1]


if __name__ == "__main__":
	# ================ Connecting to db ===========================
	print "Are you creating a database or querying?"
	writeOrQuery = raw_input("Creating: 1, Quering: 2: ")
	if writeOrQuery == "1":
		create()
	else:
		query()
