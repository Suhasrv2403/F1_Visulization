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






"""

1) See if session data injested if so get all sessions from that date and then
2) Mark session false for the following -> Drivers
3) For every session -> Need Driver,laps,car and car data

Lets map flow to see how we can improve this ?

Benchmark this as V1,V2,V3

V1 -  Api calls and directly send graphs
V2 -  Store data locally(async) and then compute and send graphs
V3 - Send data in api response for consumption.


LapTime -> Get lap data -> For every driver sort by lap number plot as a bar of s1+s2+s3 -> How to store -> Get lap data each session group by each driver and order by lap number
SpeedVsTime -> Speed at each trap per lap, see fluctuations -> Get lap data sort by lap and store speed at check points
Throttle_Brake -> Get all laps in session sort by driver , lap number, get timestamp of each stamp lap_x = start , end = start of next lap, get car data for that and store it



So the flow

For every session get lap data group by driver (change number to name) sort by lap number and store
Car data -> per session for every driver and every lap get car data and store




"""



BASE_LAP_URL = "https://api.openf1.org/v1/laps?"
SESSION_KEY = "9689"  # Replace with actual session key

# Fetch lap data for all drivers
def fetch_lap_data(session_key):
    url = f"{BASE_LAP_URL}session_key={session_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("No data retrieved. Check session key.")
        exit()

# Retrieve data



def raw_storage(SESSSION_KEY):

    session_data = fetch_lap_data(SESSION_KEY)
    collection = db['sessions']
    collection.insert_many(session_data)
    







