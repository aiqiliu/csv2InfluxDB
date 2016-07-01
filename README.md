# csv2InfluxDB

## Description
This is a sample guideline of how to convert the csv files into the influxDB inline format and how to import .txt files into a influxDB datbase and execute aggregation functions.

Through running these two scripts, you can:
* Convert csv files into influxDB inline format for writing in data points
* Create database and import converted csv files into the database
* Query a column based on a 4mins time window*

Note: The column queried from the database is default to the minimum of "TEMP". If there's no or fewer than 2 timestamps in the 4mins time range, MIN(TEMP) is default to 0.

## Installation
### InfluxDB
This script uses InfluxDB python wrapper.

Install, upgrade and uninstall InfluxDB-Python with these commands::

    $ pip install influxdb
    $ pip install --upgrade influxdb
    $ pip uninstall influxdb


## Run Script
Run `git clone https://github.com/aiqiliu/csv2InfluxDB` to clone this project

### convertInLine.py
This script converts csv files into influxDB inline format for writing in data points.
* Move your folder that contains all the csv files that you want to convert under this project directory 
* Rename the folder that contains all the csv files as "btds"
* In the project directory, run `python convertInLine.py`
* All the converted files will be stored at the "/output" folder under the project directory 

### query.py
This script allows you to create datase, import data, and query data.
* Run `python query.py`
* Follow prompt to either create a database or query from a database
Note: For importing data, this script by default writes in all data from the .txt files in the "/output" folder into the same measurement called "allTables". 

However, each datapoint has a tag "tableName" which is set as the .txt file name, in case you want to "GROUP BY" the file names.

The query function won't work as desired unless there's a cloumn with name "TEMP"

### Refenrence links
* Python wrapper, https://github.com/influxdata/influxdb-python
* Python wrapper documentation, http://influxdb-python.readthedocs.org
* InfluxDB Web API or the CLI, https://influxdata.com/downloads/#influxdb
* InfluxDB aggreagation functions, https://docs.influxdata.com/influxdb/v0.8/api/aggregate_functions

### Future Steps
* Ask for input of a list of columns to query from
* Ask for input of a list of aggregation functions (Built in aggregation functions include COUNT, MIN, MAX, MEAN, MODE, MEDIAN, DISTINCT, PERCENTILE, HISTOGRAM, DERIVATIVE, SUM, FIRST/LAST, STDDEV etc.)
* Dump results into a file 

## Contributors
* [Aiqi Liu](http://github.com/aiqiliu)

To contact the contirbutor, send email to: aiqiliu2018@u.northwestern.edu













