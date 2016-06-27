from influxdb import InfluxDBClient
client = InfluxDBClient('localhost', 8086, 'root', 'root', 'db')
result = client.query('SELECT TEMP FROM /.*/ LIMIT 1')
print result.raw['series'][0]['values'][0][1]
