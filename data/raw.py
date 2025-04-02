import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from pymongo import MongoClient
import requests

client = MongoClient("mongodb://admin:adminpassword@localhost:27017/")
db = client["F1_raw"]  # Create or access the database

"""token = '14mLPwcIwHE861WIohzUtybyZ0Zr3TseXFf_9ienONawrWZRQhEdR8lzbAbIa7bgXpEaPdcDGTogT2RDAn0ghA=='
org = "self"
url = "http://localhost:8086"

client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

bucket = "laps"

write_api = client.write_api(write_options=SYNCHRONOUS)

for value in range(5):
    point = (
        Point("measurement1")
        .tag("tagname1", "tagvalue1")
        .field("field1", value)
    )
    write_api.write(bucket=bucket, org="self", record=point)
    time.sleep(1)  # separate points by 1 second


query_api = client.query_api()

query = from(bucket: "laps")
 |> range(start: -10m)
 |> filter(fn: (r) => r._measurement == "measurement1")
tables = query_api.query(query, org="self")

for table in tables:
  for record in table.records:
    print(record)"""

def lastSessionEndTime():

    collection = db['last_session']
    last_session = collection.find()
    return last_session[0]['time']

def getNewSessions(last_session):
    url = "https://api.openf1.org/v1/sessions?&year=2025&date_end>" + last_session
    collection = db['sessions']
    response = requests.get(url)

    if response.status_code == 200:
        line = response.json()
        collection.insert_many(line)
        return line

    else:
        print(f"Error: {response.status_code}")

#def getLapsOfSession(session):


#def speedVsTimePlotGenerator():



collection = db['sessions']
last_session = collection.find()
for lap in last_session:
    print(lap)




