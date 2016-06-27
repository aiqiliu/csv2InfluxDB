#!/usr/bin/python
import subprocess
from influxdb import InfluxDBClient


def create():
	currdb = [x['name'] for x in client.get_list_database()]
	print "Your current tables are: "
	print ", ".join(str(x) for x in currdb)
	
	oneOrMultiple = raw_input("Create one table: 1, Create multiple tables: 2. ")
	if oneOrMultiple == 1:		
		createOne()
	else:
		createMultiple()

def createOne():
	dbName = raw_input("Please enter the table name you're creating: ")
	client = InfluxDBClient('localhost', 8086, 'root', 'root', dbName)
	if dbName not in currdb:
		# create databse if it doesn't exist
		client.create_database(dbName)
		print "Database " + dbName + "created"
		print "================== Writing Data ==================="
		importPath = raw_input("Enter full path to your import file: ")

	else:
		print "This table name exists already"
		retryOrQuery = raw_input("Retry: 1, Query from this table: 2. ")
		if retryOrQuery == 1:
			create()
		else:
			query(dbName)

def createMultiple():
	importPath = raw_input("Enter full path to your import files folder: ")




def query(dbName):
	



result = client.query('SELECT TEMP FROM /.*/ LIMIT 1')
print result.raw['series'][0]['values'][0][1]


if __name__ == "__main__":
	# ================ Connecting to db ===========================
	print "Are you creating a database or querying?"
	writeOrQuery = raw_input("Creating: 1, Quering: 2")
	if writeOrQuery == 1:
		create()
	else:
		query()
